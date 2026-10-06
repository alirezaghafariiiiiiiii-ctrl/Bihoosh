cmake_minimum_required(VERSION 3.31.6)

project("bihoosh" VERSION 1.0.0 LANGUAGES C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED true)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED true)

# ---------------------------------------------------------
# Android ABI configuration
# ---------------------------------------------------------

if(DEFINED ANDROID_ABI)

    message(STATUS "Detected Android ABI: ${ANDROID_ABI}")

    if(ANDROID_ABI STREQUAL "arm64-v8a")

        set(GGML_SYSTEM_ARCH "ARM")
        set(GGML_CPU_KLEIDIAI ON)
        set(GGML_OPENMP ON)

    elseif(ANDROID_ABI STREQUAL "x86_64")

        set(GGML_SYSTEM_ARCH "x86")
        set(GGML_CPU_KLEIDIAI OFF)
        set(GGML_OPENMP OFF)

    else()

        message(
            FATAL_ERROR
            "Unsupported ABI: ${ANDROID_ABI}"
        )

    endif()

endif()

# ---------------------------------------------------------
# llama.cpp source
#
# Repository structure:
#
# Bihoosh/
# ├── llama.cpp/
# └── android/
#     └── lib/
#         └── src/
#             └── main/
#                 └── cpp/
#
# ---------------------------------------------------------

set(
    LLAMA_SRC
    ${CMAKE_CURRENT_LIST_DIR}/../../../../../llama.cpp
)

message(
    STATUS
    "llama.cpp source: ${LLAMA_SRC}"
)

# ---------------------------------------------------------
# Build llama.cpp
# ---------------------------------------------------------

add_subdirectory(
    ${LLAMA_SRC}
    ${CMAKE_CURRENT_BINARY_DIR}/build-llama
)

# ---------------------------------------------------------
# Bihoosh native library
# ---------------------------------------------------------

add_library(
    bihoosh
    SHARED

    ai_chat.cpp
)

# ---------------------------------------------------------
# Compile definitions
# ---------------------------------------------------------

target_compile_definitions(
    bihoosh
    PRIVATE

    GGML_SYSTEM_ARCH=${GGML_SYSTEM_ARCH}

    GGML_CPU_KLEIDIAI=$<BOOL:${GGML_CPU_KLEIDIAI}>

    GGML_OPENMP=$<BOOL:${GGML_OPENMP}>
)

# ---------------------------------------------------------
# Include directories
# ---------------------------------------------------------

target_include_directories(
    bihoosh
    PRIVATE

    ${LLAMA_SRC}

    ${LLAMA_SRC}/common

    ${LLAMA_SRC}/include

    ${LLAMA_SRC}/ggml/include

    ${LLAMA_SRC}/ggml/src
)

# ---------------------------------------------------------
# Libraries
# ---------------------------------------------------------

target_link_libraries(
    bihoosh

    llama

    llama-common

    android

    log
)
