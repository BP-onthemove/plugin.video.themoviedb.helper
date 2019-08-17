# -*- coding: utf-8 -*-
# Module: default
# Author: jurialmunkey
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
# With thanks to Roman V. M. for original simple plugin code
from resources.lib.container import Container
from resources.lib.apis import _cache


if __name__ == '__main__':
    if _cache:
        Container().router()
