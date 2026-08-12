add_library(tensor)
target_sources(tensor
  PRIVATE
    tensor.cpp
  PUBLIC
  FILE_SET HEADERS
    BASE_DIRS include
    FILES include/tensor.h
)
target_include_directories(tensor PUBLIC include)
