# -*- coding: utf-8 -*-
from marshmallow import utils

from examples.contract.marshmallow3 import *  # noqa: F401, F403


utils.text_type = str  # We don't want to convert strings to unicode on Python 2.
