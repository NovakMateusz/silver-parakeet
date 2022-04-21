from typing import Dict

from app.utils.constans import NAME_CODE_MAPPING


def prepare_single_image_link(name: str) -> str:
    return f'images/logos/{name.lower()}.svg'


def prepare_images_links() -> Dict:
    return {
        name: prepare_single_image_link(name) for name in NAME_CODE_MAPPING.keys()
    }



