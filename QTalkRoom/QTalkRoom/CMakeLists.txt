cmake_minimum_required(VERSION 3.16)
project(QTalkRoom LANGUAGES CXX)

include(qt.cmake)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Core)
find_package(Qt${QT_VERSION_MAJOR}
    COMPONENTS
        Core
        Gui
        Widgets
)
qt_standard_project_setup()

set(PROJECT_SOURCES
    main.cpp
    QTalkRoom.ui
    QTalkRoom.h
    QTalkRoom.cpp
    QTalkRoom.rc
)

qt_add_executable(QTalkRoom ${PROJECT_SOURCES})

set_target_properties(QTalkRoom
    PROPERTIES
        WIN32_EXECUTABLE TRUE
)

target_link_libraries(QTalkRoom
    PUBLIC
        Qt::Core
        Qt::Gui
        Qt::Widgets
)
