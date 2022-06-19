"""
Bindings for the Skye program loader
"""

import ctypes
from core.SUSMap import SUSMap

lib = ctypes.CDLL("skye/libskye.so")

def StartEngine(config: SUSMap):
    """
    Start the Skye Engine with the given configuration

    Args:
        config: The SUSMap configuration to use
    """
    if not isinstance(config, SUSMap):
        raise TypeError("config must be a SUSMap")
    lib.SkyePy_StartEngine(config.map)
