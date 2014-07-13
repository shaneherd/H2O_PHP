#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from serial import Serial
 
ser = Serial('/dev/ttyUSB0', 9600)

while True:
  x=ser.readline()
  print(x)
  ser.write('9')
