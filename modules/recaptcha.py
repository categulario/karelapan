#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sin título.py
#
#  Copyright 2012 Abraham Toriz Cruz <a.wonderful.code@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
import urllib
import urllib2

def verifica(privatekey, remoteip, challenge, response):
    respuesta = urllib2.urlopen('http://www.google.com/recaptcha/api/verify', urllib.urlencode({
        'privatekey': privatekey,
        'remoteip': remoteip,
        'challenge': challenge,
        'response': response
    }))
    res = respuesta.read()
    if res.split('\n')[0] == 'true':
        return True
    else:
        return res.split('\n')[1]

if __name__ == '__main__':
    print verifica('a', 'b', 'c', 'd')

