##############################################################################
#
# Copyright (c) 2006-2008 Kapil Thangavelu <kapil.foss@gmail.com>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
zope transaction manager integration for sqlalchemy

$Id: manager.py 380 2009-11-17 12:28:27Z christian.ledermann $
"""

class AlchemistWarning(RuntimeWarning):
    """ Warnings of features that will be removed in next version
    """
    