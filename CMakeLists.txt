cmake_minimum_required(VERSION 3.24)

project(RBVideofire VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Qt6 6.5 REQUIRED COMPONENTS Core Gui Widgets)

qt_standard_project_setup()

qt_add_executable(RBVideofire
    src/main.cpp
    src/app/MainWindow.cpp
    src/app/MainWindow.h
    src/core/Project.cpp
    src/core/Project.h
    src/core/Timeline.cpp
    src/core/Timeline.h
    src/media/IMediaEngine.h
    src/media/FfmpegMediaEngine.cpp
    src/media/FfmpegMediaEngine.h
    src/render/RenderJob.h
)

target_include_directories(RBVideofire PRIVATE src)

target_link_libraries(RBVideofire PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Widgets
)

if (WIN32)
    set_target_properties(RBVideofire PROPERTIES WIN32_EXECUTABLE TRUE)
endif()
