cmake_minimum_required(VERSION 3.31)
project(mini-lm VERSION 1.0.0 LANGUAGES CXX)

include(GNUInstallDirs)

option(BUILD_TESTING "Build tests" ON)
if (BUILD_TESTING)
  find_package(GTest CONFIG REQUIRED)
  enable_testing()
endif()

add_subdirectory(modules)

if (BUILD_TESTING)
  add_subdirectory(unit_tests)
endif()

