#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  _settings.py
#
#  Copyright © 2016 Antergos
#
#  This file is part of The Antergos Build Server, (AntBS).
#
#  AntBS is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  AntBS is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  The following additional terms are in effect as per Section 7 of the license:
#
#  The preservation of all legal notices and author attributions in
#  the material or in the Appropriate Legal Notices displayed
#  by works containing it is required.
#
#  You should have received a copy of the GNU General Public License
#  along with AntBS; If not, see <http://www.gnu.org/licenses/>.

""" Classes and data descriptor objects for the storage and retrieval of shared data/settings. """

from threading import RLock

try:
    from config import settings
except Exception:
    pass


class DataObject:
    """
    Generic object used to store data/settings as attributes.

    Args:
        from_dict (dict): Initialize object using dict.

    """

    def __init__(self, from_dict=None):
        _from_dict = from_dict is not None and isinstance(from_dict, dict)
        self._lock = RLock()
        self._initialized = False

        if _from_dict and not self._initialized:
            for key, val in from_dict.items():
                setattr(self, key, val)

            self._initialized = True

    def __getattr__(self, item):
        setattr(self, item, None)

    def __setattr__(self, attr, value):
        if '_lock' == attr:
            super().__setattr__(attr, value)
        with self._lock:
            super().__setattr__(attr, value)


class SharedData:
    """
    Descriptor that facilitates shared data storage/retrieval.

    Attributes:
        name      (str):  The name of the bound attribute.
        from_dict (dict): Initial data to store.

    """

    _data = dict()

    def __init__(self, name, from_dict=None):
        self.name = name

        if name not in self._data:
            self._data[name] = None

        if from_dict is not None:
            self._data[name] = DataObject(from_dict=from_dict)

    def __get__(self, instance, cls):
        val = self if self.name not in self._data else self._data[self.name]
        return val

    def __set__(self, instance, value):
        if self.name not in self._data or self._data[self.name] is None:
            self._data[self.name] = value

    def __getattr__(self, item):
        return None


class NonSharedData:
    """
    Data descriptor that facilitates per-instance data storage/retrieval.

    Attributes:
        name      (str): The name of the bound attribute.
        from_dict (dict): Initial data to store.

    """

    _data = dict()

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        val = self if not self._instance_data_check(instance) else self._data[instance.name]
        return val

    def __getattr__(self, item):
        return None

    def __set__(self, instance, value):
        if not self._instance_data_check(instance):
            return

        self._data[instance.name] = value

    def _instance_data_check(self, instance):
        res = instance is not None

        if res and instance.name not in self._data:
            self._data[instance.name] = None

        return res
