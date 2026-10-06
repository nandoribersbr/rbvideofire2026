cmake_minimum_required(VERSION 3.24)

project(RBVideofire VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Qt6 6.5 REQUIRED COMPONENTS Core Gui Widgets)

set(FFMPEG_ROOT "" CACHE PATH "Root directory of the FFmpeg development package")

find_path(FFMPEG_INCLUDE_DIR
    NAMES libavformat/avformat.h
    HINTS ${FFMPEG_ROOT} ${FFMPEG_ROOT}/include
    PATH_SUFFIXES include
)

foreach(component AVFORMAT AVCODEC AVUTIL SWSCALE)
    string(TOLOWER "${component}" component_lower)
    find_library(FFMPEG_${component}_LIBRARY
        NAMES ${component_lower}
        HINTS ${FFMPEG_ROOT} ${FFMPEG_ROOT}/lib
        PATH_SUFFIXES lib
    )
endforeach()

if(NOT FFMPEG_INCLUDE_DIR OR
   NOT FFMPEG_AVFORMAT_LIBRARY OR
   NOT FFMPEG_AVCODEC_LIBRARY OR
   NOT FFMPEG_AVUTIL_LIBRARY OR
   NOT FFMPEG_SWSCALE_LIBRARY)
    message(FATAL_ERROR
        "FFmpeg development files not found. "
        "Configure with -DFFMPEG_ROOT=C:/path/to/ffmpeg")
endif()

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

target_include_directories(RBVideofire PRIVATE
    src
    ${FFMPEG_INCLUDE_DIR}
)

target_link_libraries(RBVideofire PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Widgets
    ${FFMPEG_AVFORMAT_LIBRARY}
    ${FFMPEG_AVCODEC_LIBRARY}
    ${FFMPEG_AVUTIL_LIBRARY}
    ${FFMPEG_SWSCALE_LIBRARY}
)

if (WIN32)
    set_target_properties(RBVideofire PROPERTIES WIN32_EXECUTABLE TRUE)
endif()
