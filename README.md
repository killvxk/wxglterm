# wxglterm [![Build Status](https://travis-ci.org/stonewell/wxglterm.svg?branch=master)](https://travis-ci.org/stonewell/wxglterm)

A cross platform terminal emulator. Buildin plugin system support python and c/c++ plugin.

## Prerequisites
* [pybind11](https://github.com/pybind/pybind11) for the python plugin system
* Python 3
* FontConfig
* OpenGL
* [wxWidgets](http://www.wxwidgets.org)

## Default Plugins
* UI plugin created using wxWidget
* UI plugin created using OpenGL, [freetype-gl](https://github.com/rougier/freetype-gl), [glfw](http://www.glfw.org/), [glew for linux](http://glew.sourceforge.net/)
* Another UI plugin created using OpenGL, [freetype-direct-gl](https://github.com/stonewell/freetype-direct-gl), [glfw](http://www.glfw.org/), [glew for linux](http://glew.sourceforge.net/), [glm](https://glm.g-truc.net/0.9.8/index.html)
* Terminal Data Handler plugin in both python and c++
* Terminal Pty plugin in both python and c++
* Color Theme plugin in python

## Build
```
mkdir build
cd build
cmake .. -DPYTHON_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") -DBUILD_WXWIDGETS_UI=ON -DBUILD_OPENGL_UI=ON
make
```
