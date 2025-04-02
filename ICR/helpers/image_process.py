"""Module for all things image processing."""

import datetime
from flask import current_app
from io import TextIOWrapper
import os
from typing_extensions import LiteralString, Union

from PIL import Image, ImageOps

# from ICR.__app import app
# TODO: check if I really need to import the app or if there is a better way
from ICR.helpers.misc import validate_file_type

# TODO: image deletion

def image_process(containers: "MultiDict") -> tuple:
    # get images if extension is valid
    valid_files: list = []
    for container in containers:
        for file in container:
            if validate_file_type(
                file.filename,
                current_app.config["IMAGE_EXTENSIONS"]
            ):
                valid_files.append(file)

    # build date strings for image and folder names
    formatted_date: str = get_image_date()
    formatted_datetime: str = get_image_datetime()

    # dir names creation
    date_path: Union[LiteralString, str, bytes] = os.path.join(
        current_app.config["ROOT_PATH"],
        current_app.config["IMAGE_ROOT_FOLDER"],
        formatted_date
    )
    image_save_path: Union[LiteralString, str, bytes] = os.path.join(
        current_app.config["ROOT_PATH"],
        current_app.config["IMAGE_UPLOAD_FOLDER"].format(
            yyyy_mm=formatted_date
        )
    )
    thumbnail_save_path: Union[LiteralString, str, bytes] = os.path.join(
        current_app.config["ROOT_PATH"],
        current_app.config[ "IMAGE_THUMBNAIL_UPLOAD_FOLDER"].format(
            yyyy_mm=formatted_date
        )
    )
    # make the dirs
    if not os.path.exists(date_path):
        os.mkdir(date_path)
    if not os.path.exists(image_save_path):
        os.mkdir(image_save_path)
    if not os.path.exists(thumbnail_save_path):
        os.mkdir(thumbnail_save_path)

    post_images: list = []
    if valid_files:
        for i, file in enumerate(valid_files):
            ext: str = os.path.splitext(file.filename)[1].lower()[1:]
            img_name, thmb_name = generate_img_thmb_name(
                formatted_datetime, i, ext
            )

            image_path = os.path.join(image_save_path, img_name)
            file.save(image_path)
            thmb_path: str = os.path.join(thumbnail_save_path, thmb_name)
            make_thumbnail(file, thmb_path)

            img_rel_path = image_path.split("ICR/static")[1]
            thmb_rel_path = thmb_path.split("ICR/static")[1]
            post_images.append((img_rel_path, thmb_rel_path))
    print("post_images", post_images)
    return post_images

def make_thumbnail(file: TextIOWrapper, dest_path: str) -> None:
    """Save a thumbnail of the incoming image.

    Args:
        filename (str): path to an image file

    Returns:
        io.BytesIO
    """
    size: tuple = current_app.config["IMAGE_THUMBNAIL_DIMENSIONS"]

    with Image.open(file) as image:
        image: Image = ImageOps.fit(image, size)
        image.save(dest_path, "png")



def get_image_date() -> str:
    """Build a date string with the specific format needed.

    Returns:
        str
    """
    return datetime.datetime.today().strftime("%Y_%m")

def get_image_datetime() -> str:
    """Build a datetime string with for the image name.

    Returns:
        str
    """
    return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

def generate_img_thmb_name(date, number: int, ext: str) -> tuple:
    """Generate file name based on date, time and an index.

    Args:
        number (int): in case many images are uploaded at once, this index will
                      help determine a unique filename.
        ext (str): the extension of the image file

    Returns:
        str
    """
    img_name: str = f"{date}_{number}.{ext}"
    thmb_name: str = f"{date}_{number}_tmb.png"
    return img_name, thmb_name
