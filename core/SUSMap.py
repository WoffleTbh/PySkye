"""
Bindings for the native implementation of SUSMap
"""

import ctypes
import os

lib = ctypes.CDLL("skye/libskye.so")

class SUSMap:
    def __init__(self, src: str):
        """
        Create a SUSMap instance in C++
        this class provides a Python interface to the C++ implementation

        Args:
            src: a string with the SUSMap data to load
        """
        if not isinstance(src, str):
            raise TypeError("src must be a string")
        self.src = src
        self.src_c = ctypes.c_char_p(src.encode("utf-8"))
        self.map = lib.SkyePy_SUSMap_new(self.src_c)

    def getStringOr(self, key: str, fallback: str) -> str:
        """
        Get a string from the SUSMap, or fallback if not found

        Args:
            key: the key to look up
            fallback: the value to return if the key is not found
        """
        key_c = ctypes.c_char_p(key.encode("utf-8"))
        fallback_c = ctypes.c_char_p(fallback.encode("utf-8"))
        result_c = lib.SkyePy_SUSMap_getStringOr(self.map, key_c, fallback_c)
        return result_c.decode("utf-8")

    def getIntOr(self, key: str, fallback: int) -> int:
        """
        Get an int from the SUSMap, or fallback if not found

        Args:
            key: the key to look up
            fallback: the value to return if the key is not found
        """
        key_c = ctypes.c_char_p(key.encode("utf-8"))
        fallback_c = ctypes.c_int(fallback)
        result_c = lib.SkyePy_SUSMap_getIntOr(self.map, key_c, fallback_c)
        return result_c.value

    def getBoolOr(self, key: str, fallback: bool) -> bool:
        """
        Get a bool from the SUSMap, or fallback if not found

        Args:
            key: the key to look up
            fallback: the value to return if the key is not found
        """
        key_c = ctypes.c_char_p(key.encode("utf-8"))
        fallback_c = ctypes.c_bool(fallback)
        result_c = lib.SkyePy_SUSMap_getBoolOr(self.map, key_c, fallback_c)
        return result_c.value

    # Technical garbage
    #def __del__(self):
    #    lib.SkyePy_SUSMap_delete(self.map)

