#!/usr/bin/env python
# Copyright (c) 2015 Tim Savannah All Rights Rserved under LGPLv3. See LICENSE (https://gnu.org/licenses/lgpl-3.0.txt) for more information.
#
# In general below, all "tag names" (body, div, etc) should be lowercase. The parser will lowercase internally. All attribute names (like `id` in id="123") provided to search functions should be lowercase. Values are not lowercase. This is because doing tons of searches, lowercasing every search can quickly build up. Lowercase it once in your code, not every time you call a function.

from .Parser import AdvancedHTMLParser, IndexedAdvancedHTMLParser
from .Tags import AdvancedTag, TagCollection
from .Formatter import AdvancedHTMLFormatter

__version__ = '6.4.2'
__version_tuple__ = ('6', '4', '2')
__int_version_tuple__ = (6, 4, 2)

__all__ = ['AdvancedHTMLParser', 'IndexedAdvancedHTMLParser', 'AdvancedHTMLFormatter', 'AdvancedTag', 'TagCollection']

#vim: set ts=4 sw=4 expandtab
