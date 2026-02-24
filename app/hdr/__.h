#include <nds.h>
#include <sstream>

#ifndef ___H
#define ___H

#define NOCASHMESSAGE(message) \
    { \
        std::ostringstream stream; \
        stream << message << std::endl; \
        nocashMessage(stream); \
    }
    

void nocashMessage(const std::ostringstream& stream);

#endif