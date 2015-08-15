#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  vmware.py
#
#  Copyright © 2013-2015 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
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
#  along with Cnchi; If not, see <http://www.gnu.org/licenses/>.


""" Vmware driver installation """

try:
    from hardware.hardware import Hardware
except ImportError:
    from hardware import Hardware

CLASS_NAME = "Vmware"
CLASS_ID = ""
VENDOR_ID = "0x15ad"
DEVICES = ["0x0405", "0x0710"]


class Vmware(Hardware):
    """ Vmware class definition """
    def __init__(self):
        Hardware.__init__(self, CLASS_NAME, CLASS_ID, VENDOR_ID, DEVICES)

    def get_packages(self):
        return ["xf86-video-vmware", "xf86-input-vmmouse", "open-vm-tools"]

    def post_install(self, dest_dir):
        super().chroot(["systemctl", "enable", "vmtoolsd"], dest_dir)
