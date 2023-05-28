#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et

import sys
import kociemba
import argparse
from video import webcam
import i18n
import os
from configs import config
from constants import (
    ROOT_DIR,
    E_INCORRECTLY_SCANNED,
    E_ALREADY_SOLVED
)

# Set default locale.
locale = config.get_setting('locale')
if not locale:
    config.set_setting('locale', 'zh')
    locale = config.get_setting('locale')

# Init i18n.
i18n.load_path.append(os.path.join(ROOT_DIR, 'translations'))
i18n.set('filename_format', '{locale}.{format}')
i18n.set('file_format', 'json')
i18n.set('locale', locale)
i18n.set('fallback', 'zh')


class Qbr:

    def __init__(self, normalize):
        self.normalize = normalize
        self.webcam = webcam
        self.state = None
        self.solution = None

    def run(self):
        """The main function that will run the Qbr program."""
        state = self.webcam.run()

        # If we receive a number then it's an error code.
        if isinstance(state, int) and state > 0:
            print("|-----------------------------|")
            self.print_E_and_exit(state)
            return

        try:
            self.state = None
            self.solution = None
            algorithm = kociemba.solve(state)
            length = len(algorithm.split(' '))
            print(state)
            print(i18n.t('startingPosition'))
            print(i18n.t('moves', moves=length))
            print(i18n.t('solution', algorithm=algorithm))
            if self.normalize:
                for index, notation in enumerate(algorithm.split(' ')):
                    text = i18n.t('solveManual.{}'.format(notation))
                    print('{}. {}'.format(index + 1, text))
            self.state = state
            self.solution = algorithm

        except Exception:
            print("-----------------------------")
            self.print_E_and_exit(E_INCORRECTLY_SCANNED)
            return

    def print_E_and_exit(self, code):
        """Print an error message based on the code and exit the program."""
        if code == E_INCORRECTLY_SCANNED:
            print('\033[0;33m[{}] {}'.format(
                i18n.t('error'), i18n.t('haventScannedAllSides')))
            print('{}\033[0m'.format(i18n.t('pleaseTryAgain')))
        elif code == E_ALREADY_SOLVED:
            print('\033[0;33m[{}] {}'.format(
                i18n.t('error'), i18n.t('cubeAlreadySolved')))
        # sys.exit(code)


# Define the application arguments.
parser = argparse.ArgumentParser()
parser.add_argument(
    '-n',
    '--normalize',
    default=False,
    action='store_true',
    help='Shows the solution normalized. For example "R2" would be: \
            "Turn the right side 180 degrees".'
)
args = parser.parse_args()

# Run Qbr with all arguments.
# Qbr(args.normalize).run()
