import json
from pathlib import Path
from typing import Tuple

import pygame


def get_images(
    sheet: pygame.Surface,
    size: Tuple[int],
):
    """
    Converts a sprite sheet to a list of surfaces

    Parameters:
        sheet: A pygame.Surface that contains the sprite sheet
        size: Size of a sprite in the sprite sheet
    """
    images = []

    width, height = size

    # loop through all sprites in the sprite sheet
    rows = int(sheet.get_height() / height)
    columns = int(sheet.get_width() / width)

    for row in range(rows):
        for col in range(columns):
            image = sheet.subsurface(pygame.Rect((col * width), (row * height), *size))

            images.append(image)

    return images


def load_assets(state: str) -> dict:
    """
    Loads the game assets depending on the game state
    """
    assets = {}
    path = Path("assets/gfx/")

    json_files = path.rglob("*.json")
    for metadata_f in json_files:
        metadata = json.loads(metadata_f.read_text())
        for file, data in metadata.items():
            if state not in data["states"]:
                continue

            complete_path = metadata_f.parent / file
            print(f"Loaded {complete_path}")
            if data["convert_alpha"]:
                image = pygame.image.load(complete_path).convert_alpha()
            else:
                image = pygame.image.load(complete_path).convert()

            if data["sprite_sheet"] is None:
                asset = image
            else:
                asset = get_images(image, *data["sprite_sheet"].values())

            file_extension = file[file.find(".") :]
            assets[file.replace(file_extension, "")] = asset

    return assets
