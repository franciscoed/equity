import sys
print("Import ctypes")
from ctypes import *

print("CDLL") 
lib = CDLL("/home/appuser/lib/libta_lib.so.0.0.0")
print(str(lib))
print("Importing talib")
sys.stdout.flush()
# import library
import talib
