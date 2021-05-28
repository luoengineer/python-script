import ctypes
from ctypes import *
import time

fileName = 'A2.txt'
f = open(fileName, 'a+')




A0 = "08 00 00 1F 05 01 03"
A0 = A0.replace(' ', ',0x')
print(A0)



f.close()