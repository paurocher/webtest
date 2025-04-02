"""Generate demo images for testing."""

import os
import shutil



def restore_images():

    # figure out if we are running on pythonanywhere
    PYTHONANYWHERE = os.getenv("PYTHONANYWHERE_DOMAIN")
    if PYTHONANYWHERE:
        path_root = "/home/PauRocher/webtest"
    else:
        path_root = "/home/fuku/PycharmProjects/webtest"
    # passing images outside the project to simulate an image upload
    images = [
        f"{path_root}/tests/mockup_images/2025_03_05_06_29_38_0.jpg",
        f"{path_root}/tests/mockup_images/2025_03_05_06_29_38_1.jpg",
        f"{path_root}/tests/mockup_images/2025_03_05_06_29_38_2.jpg",
        f"{path_root}/tests/mockup_images/2025_03_05_06_29_38_3.jpg",
        f"{path_root}/tests/mockup_images/2025_03_05_06_29_38_4.jpg",
    ]
    thumbs = [
        f"{path_root}/tests/mockup_images/2025_03_05_06_29_38_0_tmb.png",
        f"{path_root}/tests/mockup_images/2025_03_05_06_29_38_1_tmb.png",
        f"{path_root}/tests/mockup_images/2025_03_05_06_29_38_2_tmb.png",
        f"{path_root}/tests/mockup_images/2025_03_05_06_29_38_3_tmb.png",
        f"{path_root}/tests/mockup_images/2025_03_05_06_29_38_4_tmb.png",
    ]

    for image in images:
        shutil.copy(
            image,
            f"{path_root}/ICR/static/images/2025_03/"
            "pictures"
        )
    for thumb in thumbs:
        shutil.copy(
            thumb,
            f"{path_root}/ICR/static/images/2025_03"
            "/thumbnails"
        )

if __name__ == "__main__":
    restore_images()
