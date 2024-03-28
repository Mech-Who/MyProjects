#ifndef __DECODER_H__
#define __DECODER_H__

#include <string>

class Decoder{
public:
    virtual bool decode(std::string file_name);
private:
    std::string decoder_standard;
    std::string decoder_type;
};

#endif