import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ICR.helpers.image_process import (
    image_process,
    make_thumbnail
)

from werkzeug.datastructures import FileStorage
from werkzeug.datastructures import MultiDict, ImmutableMultiDict

def mockup_FileStorage():
    # passing images outside the project to simulate an image upload
    images = [
        "/home/fuku/Desktop/Hanae.jpg",
        "/home/fuku/Desktop/Hanae_dibuix.jpg",
        "/home/fuku/Desktop/Serena_dibuix.jpg",
    ]

    container = MultiDict()

    for image in images:
        name = os.path.split(image)[1]

        file = open(image, "rb")
        # print(file)
        file_storage = FileStorage(file, name=name, filename=name, content_type="image/jpeg")
        # print(file_storage)
        container.add("files", file_storage)

    return container


def test_image_process():
    container = mockup_FileStorage()
    print(container)
    image_process([container.getlist("files")])



test_image_process()

"""
ImmutableMultiDict([('files', <FileStorage: 'Serena_dibuix.jpg' ('image/jpeg')>), ('files', <FileStorage: 'Hanae_dibuix.jpg' ('image/jpeg')>)])
In image_process
<FileStorage: 'Hanae_dibuix.jpg' ('image/jpeg')>
"""