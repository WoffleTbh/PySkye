/*
This file is part of the PySkye wrapper
*/

#include "sus/SUSMap.hpp"
#include <string.h>
#include <iostream>

extern "C" {
    void amogus() {
        std::cout << "Hello from C++" << std::endl;
    }
    SUSMap* SkyePy_SUSMap_new(const char* src) {
        return new SUSMap(std::string(src));
    }
    char* SkyePy_SUSMap_getStringOr(SUSMap* self, const char* key, const char* fallback) {
        return strdup(self->getStringOr(std::string(key), std::string(fallback)).c_str());
    }
    int SkyePy_SUSMap_getIntOr(SUSMap* self, const char* key, int fallback) {
        return self->getIntOr(std::string(key), fallback);
    }
    bool SkyePy_SUSMap_getBoolOr(SUSMap* self, const char* key, bool fallback) {
        return self->getBoolOr(std::string(key), fallback);
    }
}

