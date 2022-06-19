/*
This file is part of the PySkye wrapper
*/

#include "shell/shell.hpp"

extern "C" {
    void SkyePy_StartEngine(SUSMap* config) {
        StartEngine(*config);
    }

    void SkyePy_StopEngine() {
        /* placeholder */
    }
}
