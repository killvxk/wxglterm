CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

CMAKE_POLICY(
    SET CMP0048 NEW
    )
CMAKE_POLICY(
    SET CMP0058 NEW
)
#CMAKE_POLICY(
#    SET CMP0072 NEW
#)

PROJECT (wxglTerm
	VERSION 1.0.0
	)

INCLUDE(ExternalProject)

IF(APPLE)
  SET(CMAKE_MACOSX_RPATH 1)
  SET(CMAKE_PREFIX_PATH /usr/local)
ENDIF()

IF(NOT CMAKE_BUILD_TYPE)
  SET(CMAKE_BUILD_TYPE "DEBUG")
  #SET(CMAKE_BUILD_TYPE "RELEASE")
  #SET(CMAKE_BUILD_TYPE "RELWITHDEBINFO")
  #SET(CMAKE_BUILD_TYPE "MINSIZEREL")
ENDIF()

OPTION(BUILD_OPENGL_UI "build opengl ui" ON)
OPTION(BUILD_WXWIDGETS_UI "build wxwidgets ui" ON)
OPTION(BUILD_SCINTILLA_EDITOR "build editor buffer using scintilla" OFF)
IF (APPLE)
   OPTION(USE_GLFW_HACK_FIX "use glfw hack fix for macos mojave or upper" OFF)
ENDIF(APPLE)

SET(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_CURRENT_SOURCE_DIR}/cmake/Modules/")

if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
  set(warnings "-Wall -Wextra -Werror -Wno-cast-function-type -Wno-ignored-qualifiers")
  set(no_undefined "-Wl,--no-undefined")
elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
  set(warnings "-Wall -Wextra -Werror -Wno-inconsistent-missing-override")
  set(no_undefined "-Wl,-undefined,error")
elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
    set(warnings "/W4 /WX /EHsc")
    set(no_undefined "")
endif()

SET(CXX_STANDARD_REQUIRED OFF)
SET(CXX_EXTENSION NO)

if (NOT CONFIGURED_ONCE)
    set(CMAKE_C_FLAGS "-fPIC ${warnings}"
        CACHE STRING "Flags used by the compiler during all build types." FORCE)
    set(CMAKE_CXX_FLAGS "-fPIC ${warnings} -std=c++14"
        CACHE STRING "Flags used by the compiler during all build types." FORCE)
    set(CMAKE_LINK_FLAGS "${no_undefined}"
        CACHE STRING "Flags used by the linker during all build types." FORCE)
endif()

EXTERNALPROJECT_ADD(
  pybind11

  GIT_REPOSITORY "https://github.com/pybind/pybind11.git"
  GIT_TAG "master"

  PATCH_COMMAND ""
  UPDATE_DISCONNECTED ON

  CMAKE_ARGS -DCMAKE_BUILD_TYPE=Debug -DPYBIND11_TEST=OFF -DPYBIND11_INSTALL=ON -DCMAKE_INSTALL_PREFIX=${CMAKE_BINARY_DIR}/pybind11_install

  TEST_COMMAND ""
)

ExternalProject_Add_StepTargets(pybind11 update)

SET(pybind11_INCLUDE_DIRS ${CMAKE_BINARY_DIR}/pybind11_install/include)

FIND_PACKAGE(PythonInterp 3 REQUIRED)
FIND_PACKAGE(PythonLibs 3 REQUIRED)

configure_file(wxglterm.json.in wxglterm.json)
configure_file(wxglterm_install.json.in wxglterm_install.json)
configure_file(wxglterm.desktop.in wxglterm.desktop)

ADD_CUSTOM_TARGET(update_external DEPENDS pybind11-update)

IF (APPLE)
   EXEC_PROGRAM(uname ARGS -v  OUTPUT_VARIABLE DARWIN_VERSION)
   STRING(REGEX MATCH "[0-9]+" DARWIN_VERSION ${DARWIN_VERSION})
   MESSAGE(STATUS "DARWIN_VERSION=${DARWIN_VERSION}")
   IF (DARWIN_VERSION GREATER_EQUAL 18)
      SET(USE_GLFW_HACK_FIX ON)
   ENDIF (DARWIN_VERSION GREATER_EQUAL 18)
ENDIF(APPLE)

IF (USE_GLFW_HACK_FIX)
   ADD_SUBDIRECTORY(glfw_fix)
   SET(GLFW_HACK_FIX_LIB glfw_fix "-framework Foundation")
   SET(GLFW_HACK_FIX_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/glfw_fix")
   MESSAGE(STATUS "add glfw hack fix for macos > 10.14")
   MESSAGE(STATUS "include dir:${GLFW_HACK_FIX_INCLUDE_DIR}")
   ADD_DEFINITIONS(-DGLFW_HACK_FIX -DGL_SILENCE_DEPRECATION)
ENDIF()

ADD_SUBDIRECTORY(src/interface)
ADD_SUBDIRECTORY(src/controller)
ADD_SUBDIRECTORY(src/utils)
ADD_SUBDIRECTORY(src/caps)
ADD_SUBDIRECTORY(src/plugins)
ADD_SUBDIRECTORY(src/app)
ADD_SUBDIRECTORY(src/external_plugins)

ADD_CUSTOM_COMMAND(OUTPUT ${CMAKE_BINARY_DIR}/termdata.stamp
  COMMAND
  ${CMAKE_COMMAND} -E copy_directory ${CMAKE_SOURCE_DIR}/data ${CMAKE_BINARY_DIR}/data
  COMMAND
  ${CMAKE_COMMAND} -E copy_directory ${CMAKE_SOURCE_DIR}/pysrc/libs ${CMAKE_BINARY_DIR}/libs
  COMMENT
  "Copying term data..."
  VERBATIM
  )

# uninstall target
if(NOT TARGET uninstall)
    configure_file(
        "${CMAKE_CURRENT_SOURCE_DIR}/cmake_uninstall.cmake.in"
        "${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake"
        IMMEDIATE @ONLY)

    add_custom_target(uninstall
        COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake)
endif()

ADD_CUSTOM_TARGET(copy_term_data ALL DEPENDS ${CMAKE_BINARY_DIR}/termdata.stamp wxglterm)

INSTALL(FILES ${CMAKE_BINARY_DIR}/wxglterm.desktop DESTINATION share/applications)
INSTALL(DIRECTORY ${CMAKE_SOURCE_DIR}/data DESTINATION share/wxglterm)
INSTALL(DIRECTORY ${CMAKE_SOURCE_DIR}/pysrc/libs DESTINATION share/wxglterm)
INSTALL(FILES ${CMAKE_BINARY_DIR}/wxglterm_install.json DESTINATION share/wxglterm/etc RENAME wxglterm.json)

INCLUDE(CPack)
