cmake_minimum_required(VERSION 3.10)
project(EncoderDecoderSystem)

# Add your source files here
set(SOURCES
    src/main.cpp
    src/encoder.cpp
    src/decoder.cpp
)

# Add your header files here
set(HEADERS
    include/encoder.h
    include/decoder.h
)

# Add your executable target
add_executable(EncoderDecoder ${SOURCES} ${HEADERS})