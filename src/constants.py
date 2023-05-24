#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et

import os
import math

# Global
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Colors
COLOR_PLACEHOLDER = (150, 150, 150)

# i18n
LOCALES = {
    'en': 'English',
    'zh': '简体中文',
}

# Camera interface
MINI_STICKER_AREA_TILE_SIZE = 14
MINI_STICKER_AREA_TILE_GAP = 2
MINI_STICKER_AREA_OFFSET = 20

STICKER_AREA_TILE_SIZE = 30
STICKER_AREA_TILE_GAP = 4
STICKER_AREA_OFFSET = 20

STICKER_CONTOUR_COLOR = (36, 255, 12)
CALIBRATE_MODE_KEY = 'c'
SWITCH_LANGUAGE_KEY = 'l'
TEXT_SIZE = 18

# Config
CUBE_PALETTE = 'cube_palette'

# Application errors
E_INCORRECTLY_SCANNED = 1
E_ALREADY_SOLVED = 2

PI = math.acos(-1.0)

# Colors

WHITE = (1.0, 1.0, 1.0)
RED = (1.0, 0.0, 0.0)
GREEN = (0.0, 1.0, 0.0)
ORANGE = (1.0, 0.5, 0.0)
BLUE = (0.0, 0.0, 1.0)
YELLOW = (1.0, 1.0, 0.0)
GREY = (0.5, 0.5, 0.5)
BLEAK = (0.0, 0.0, 0.0)

SELECT_WHITE = (BLEAK, WHITE)
SELECT_RED = (BLEAK, RED)
SELECT_GREEN = (BLEAK, GREEN)
SELECT_ORANGE = (BLEAK, ORANGE)
SELECT_BULE = (BLEAK, BLUE)
SELECT_YELLOW = (BLEAK, YELLOW)
