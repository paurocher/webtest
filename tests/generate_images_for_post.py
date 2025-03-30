""""""

import shutil

def restore_images():
    # passing images outside the project to simulate an image upload
    images = [
"/home/fuku/PycharmProjects/webtest/tests/mockup_images/2025_03_05_06_29_38_0"
".jpg",
"/home/fuku/PycharmProjects/webtest/tests/mockup_images/2025_03_05_06_29_38_1"
".jpg",
"/home/fuku/PycharmProjects/webtest/tests/mockup_images/2025_03_05_06_29_38_2"
".jpg",
"/home/fuku/PycharmProjects/webtest/tests/mockup_images/2025_03_05_06_29_38_3"
".jpg",
"/home/fuku/PycharmProjects/webtest/tests/mockup_images/2025_03_05_06_29_38_4"
".jpg",
    ]
    thumbs = [
"/home/fuku/PycharmProjects/webtest/tests/mockup_images"
"/2025_03_05_06_29_38_4_tmb.png",
"/home/fuku/PycharmProjects/webtest/tests/mockup_images"
"/2025_03_05_06_29_38_3_tmb.png",
"/home/fuku/PycharmProjects/webtest/tests/mockup_images"
"/2025_03_05_06_29_38_2_tmb.png",
"/home/fuku/PycharmProjects/webtest/tests/mockup_images"
"/2025_03_05_06_29_38_1_tmb.png",
"/home/fuku/PycharmProjects/webtest/tests/mockup_images"
"/2025_03_05_06_29_38_0_tmb.png",
    ]

    for image in images:
        shutil.copy(image, "/home/fuku/PycharmProjects/webtest/ICR/static/images/2025_03/pictures")
    for thumb in thumbs:
        shutil.copy(
            thumb,
            "/home/fuku/PycharmProjects/webtest/ICR/static/images/2025_03"
            "/thumbnails"
        )

if __name__ == "__main__":
    restore_images()
