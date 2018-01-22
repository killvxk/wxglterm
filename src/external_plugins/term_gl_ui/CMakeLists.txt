FIND_PACKAGE(OpenGL REQUIRED)
FIND_PACKAGE(Freetype REQUIRED)
FIND_PACKAGE(glfw3 3.2 REQUIRED)

INCLUDE(ExternalProject)

EXTERNALPROJECT_ADD(
  freetype-gl

  GIT_REPOSITORY "https://github.com/rougier/freetype-gl.git"
  GIT_TAG "master"

  #UPDATE_COMMAND ${GIT_EXECUTABLE} pull
  UPDATE_COMMAND ""
  PATCH_COMMAND ""

  CMAKE_ARGS -Dfreetype-gl_BUILD_APIDOC=OFF -Dfreetype-gl_BUILD_DEMOS=OFF -Dfreetype-gl_BUILD_TESTS=OFF -Dfreetype-gl_BUILD_MAKEFONT=OFF -DCMAKE_C_FLAGS=-fPIC

  TEST_COMMAND ""

  INSTALL_COMMAND ""
)

SET(term_gl_ui_src
  term_gl_ui_plugin.cpp
  term_gl_ui.cpp term_gl_ui.h
  default_term_window.h default_term_window.cpp
  plugin_base.h
  freetype_gl.cpp freetype_gl.h
  shader.cpp shader.h
  mat4.cpp mat4.h
)

EXTERNALPROJECT_GET_PROPERTY(freetype-gl SOURCE_DIR BINARY_DIR)

ADD_LIBRARY(term_gl_ui SHARED ${term_gl_ui_src}
		       text_vert.inc text_frag.inc
		       )

ADD_DEPENDENCIES(term_gl_ui freetype-gl)

SET_TARGET_PROPERTIES( term_gl_ui
    PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/plugins"
)


FIND_PACKAGE(FontConfig REQUIRED)

ADD_CUSTOM_COMMAND(OUTPUT text_vert.inc
  COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/../../../utils/pystmt_generator/pystmt_generator.py -i ${SOURCE_DIR}/shaders/text.vert -o text_vert.inc
  DEPENDS ${SOURCE_DIR}/shaders/text.vert ${CMAKE_CURRENT_SOURCE_DIR}/../../../utils/pystmt_generator/pystmt_generator.py
  )
ADD_CUSTOM_COMMAND(OUTPUT text_frag.inc
  COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/../../../utils/pystmt_generator/pystmt_generator.py -i ${SOURCE_DIR}/shaders/text.frag -o text_frag.inc
  DEPENDS ${SOURCE_DIR}/shaders/text.frag ${CMAKE_CURRENT_SOURCE_DIR}/../../../utils/pystmt_generator/pystmt_generator.py
  )

SET(freetype-gl_INCLUDE_DIR ${SOURCE_DIR})
SET(freetype-gl_LIBRARIES ${BINARY_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}freetype-gl${CMAKE_STATIC_LIBRARY_SUFFIX})

TARGET_INCLUDE_DIRECTORIES(term_gl_ui
    PUBLIC
	$<TARGET_PROPERTY:glfw,INTERFACE_INCLUDE_DIRECTORIES>
    PRIVATE
	"${CMAKE_CURRENT_SRC_DIR}"
	"${CMAKE_CURRENT_BINARY_DIR}"
        "${pybind11_INCLUDE_DIRS}"
	"${PYTHON_INCLUDE_DIRS}"
  	"ui"
  	"../../interface"
  	"../../utils"
  	"../../utils/portable_thread/includes"
	"${freetype-gl_INCLUDE_DIR}"
	"${FONTCONFIG_INCLUDE_DIR}"
)

TARGET_LINK_LIBRARIES(term_gl_ui
  utils
  ${pybind11_LIBRARIES}
  ${PYTHON_LIBRARIES}
  glfw
  ${OPENGL_LIBRARY}
  ${FREETYPE_LIBRARIES}
  ${freetype-gl_LIBRARIES}
  ${FONTCONFIG_LIBRARY}
  )

INSTALL(TARGETS term_gl_ui DESTINATION share/wxglterm/plugins)