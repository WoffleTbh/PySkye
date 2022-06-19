"""
Bindings for the native implementation of SUSMap
"""

import ctypes

lib = ctypes.CDLL("skye/libskye.so")

class SUSMap:
    def __init__(self, src):
        self.src = src
        self.src_c = ctypes.c_char_p(src.encode("utf-8"))
        self.map = lib.SkyePy_SUSMap_new(self.src_c)

    def getStringOr(self, key: str, fallback: str) -> str:
        """
        Get a string from the SUSMap, or fallback if not found
        """
        key_c = ctypes.c_char_p(key.encode("utf-8"))
        fallback_c = ctypes.c_char_p(fallback.encode("utf-8"))
        result_c = lib.SkyePy_SUSMap_getStringOr(self.map, key_c, fallback_c)
        return result_c.decode("utf-8")

    def getIntOr(self, key: str, fallback: int) -> int:
        """
        Get an int from the SUSMap, or fallback if not found
        """
        key_c = ctypes.c_char_p(key.encode("utf-8"))
        fallback_c = ctypes.c_int(fallback)
        result_c = lib.SkyePy_SUSMap_getIntOr(self.map, key_c, fallback_c)
        return result_c.value

    def getBoolOr(self, key: str, fallback: bool) -> bool:
        """
        Get a bool from the SUSMap, or fallback if not found
        """
        key_c = ctypes.c_char_p(key.encode("utf-8"))
        fallback_c = ctypes.c_bool(fallback)
        result_c = lib.SkyePy_SUSMap_getBoolOr(self.map, key_c, fallback_c)
        return result_c.value
