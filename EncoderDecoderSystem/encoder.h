#ifndef __ENCODER_H__
#define __ENCODER_H__

#include <string>

class Encoder{
public:
    virtual bool encode(std::string file_name);
private:
    std::string encoder_standard;
    std::string encoder_type;
};

#endif