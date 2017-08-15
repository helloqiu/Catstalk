# -*- coding: utf-8 -*-

import colorlog

logger = colorlog.getLogger('catstalk')
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(message)s'))
logger.addHandler(handler)
logger.setLevel('INFO')
