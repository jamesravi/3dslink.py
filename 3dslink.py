"""
3dslink.py - port of devkitPro's 3dslink to Python 
Copyright (C) 2022 James Ravindran

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import socket
import os
import zlib
import io

HOST = "192.168.1.127"
PORT = 17491
CHUNK_SIZE = 16*1024

filename = "afile.3dsx"

def toInt32LE(n):
    return (n).to_bytes(4, byteorder="little")

def getInt32LE(s):
    return int.from_bytes(s.recv(4), byteorder="little")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    filenameend = filename.split("/")[-1]
    s.sendall(toInt32LE(len(filenameend)))
    s.sendall(filenameend.encode("ascii"))
    s.sendall(toInt32LE(os.path.getsize(filename)))
    assert getInt32LE(s) == 0
    
    with open(filename, "rb") as thefile:
        compressed = io.BytesIO(zlib.compress(thefile.read()))
    while True:
        data = compressed.read(CHUNK_SIZE)
        if not data:
            break
        s.sendall(toInt32LE(len(data)))
        s.sendall(data)
