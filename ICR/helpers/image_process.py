"""Module for all things image processing."""

import datetime
import os
from io import TextIOWrapper

from PIL import Image, ImageOps

from ICR.__app import app
# TODO: check if I really need to import the app or if there is a better way
from ICR.helpers.misc import validate_file_type

# TODO: image deletion

def image_process(containers: "MultiDict") -> tuple:
    valid_files: list = []
    for container in containers:
        for file in container:
            if validate_file_type(
                file.filename,
                app.config["IMAGE_EXTENSIONS"]
            ):
                valid_files.append(file)

    formatted_date: str = get_image_date()

    # dir creation
    date_path: str = os.path.join(
        app.config["IMAGE_ROOT_FOLDER"],
        formatted_date
    )
    image_save_path: str = app.config["IMAGE_UPLOAD_FOLDER"].format(
        yyyy_mm=formatted_date
    )
    thumbnail_save_path: str = app.config[
        "IMAGE_THUMBNAIL_UPLOAD_FOLDER"
    ].format(
        yyyy_mm=formatted_date
    )
    if not os.path.exists(date_path):
        os.mkdir(date_path)
        os.mkdir(image_save_path)
        os.mkdir(thumbnail_save_path)

    post_images: list = []
    if valid_files:
        for i, file in enumerate(valid_files):
            ext: str = os.path.splitext(file.filename)[1].lower()[1:]
            img_name, thmb_name = generate_img_thmb_name(i, ext)

            image_path = os.path.join(image_save_path, img_name)
            file.save(image_path)
            thmb_path: str = os.path.join(thumbnail_save_path, thmb_name)
            make_thumbnail(file, thmb_path)

            img_rel_path = os.path.sep.join(image_path.split(os.path.sep)[1:])
            thmb_rel_path = os.path.sep.join(thmb_path.split(os.path.sep)[1:])
            post_images.append((img_rel_path, thmb_rel_path))

    return post_images

def make_thumbnail(file: TextIOWrapper, dest_path: str) -> None:
    """Save a thumbnail of the incoming image.

    Args:
        filename (str): path to an image file

    Returns:
        io.BytesIO
    """
    size: tuple = app.config["IMAGE_THUMBNAIL_DIMENSIONS"]

    with Image.open(file) as image:
        image: Image = ImageOps.fit(image, size)
        image.save(dest_path, "png")



def get_image_date() -> str:
    """Build a date string with the specific format needed.

    Returns:
        str
    """
    return datetime.datetime.today().strftime("%Y_%m")


def generate_img_thmb_name(number: int, ext: str) -> tuple:
    """Generate file name based on date, time and an index.

    Args:
        number (int): in case many images are uploaded at once, this index will
                      help determine a unique filename.
        ext (str): the extension of the image file

    Returns:
        str
    """
    date: str = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    img_name: str = f"{date}_{number}.{ext}"
    thmb_name: str = f"{date}_{number}_tmb.png"
    return img_name, thmb_name
