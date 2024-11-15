cmake_minimum_required(VERSION 3.16)
project(QTalkRoomServer LANGUAGES CXX)

include(qt.cmake)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Core)
find_package(Qt${QT_VERSION_MAJOR}
    COMPONENTS
        Core
        Gui
        Widgets
        Network
)
qt_standard_project_setup()

set(PROJECT_SOURCES
    main.cpp
    QTalkRoomServer.ui
    QTalkRoomServer.h
    QTalkRoomServer.cpp
    QTalkRoomServer.rc
)

qt_add_executable(QTalkRoomServer ${PROJECT_SOURCES})

set_target_properties(QTalkRoomServer
    PROPERTIES
        WIN32_EXECUTABLE TRUE
)

target_link_libraries(QTalkRoomServer
    PUBLIC
        Qt::Core
        Qt::Gui
        Qt::Widgets
        Qt::Network
)
