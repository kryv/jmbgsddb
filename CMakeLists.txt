cmake_minimum_required(VERSION 2.8.2)

project("uscsi" C CXX)

option(USE_WERROR "Treat warnings as errors")
option(USE_PYTHON "Build python support" ON)
option(NEED_PYTHON "Require python support" OFF)

message(STATUS "Option PYTHON ${USE_PYTHON}")

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE DEBUG) # default to debug build
endif()
if(CMAKE_COMPILER_IS_GNUCC)
  # Turn on extra GCC warnings
  add_definitions(-Wall -Wextra -Wno-unused-parameter -Wno-missing-field-initializers)
  if(USE_WERROR)
    add_definitions(-Werror)
  endif()
endif()
message(STATUS "Build type ${CMAKE_BUILD_TYPE}")

find_package(Boost 1.42.0 REQUIRED COMPONENTS system thread)

# respects -DHDF5_USE_STATIC_LIBRARIES=YES
# and environment variable HDF5_ROOT
find_package(HDF5 REQUIRED COMPONENTS C CXX)

find_program(LEX_EXECUTABLE flex
  DOC "Location of lexer genereator"
)
find_program(YACC_EXECUTABLE bison
  DOC "Location of parser generator"
)
message(STATUS "FLEX ${LEX_EXECUTABLE}")
message(STATUS "BISON ${YACC_EXECUTABLE}")

if(NOT LEX_EXECUTABLE OR NOT YACC_EXECUTABLE)
  message(SEND_ERROR "Missing flex or bison")
endif()

message(STATUS "Boost libs in ${Boost_LIBRARY_DIRS}")

find_package(PythonInterp 2.6)

if(PYTHONINTERP_FOUND)
  # Introspect this interpreter
  execute_process(COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/pyconfig.py ${CMAKE_CURRENT_BINARY_DIR}/pyconfig.cmake
    RESULT_VARIABLE _PY_CONFIG
  )
  if(_PY_CONFIG)
    message(STATUS "Failed to fetch build information for ${PYTHON_EXECUTABLE}")
  else()
    include(${CMAKE_CURRENT_BINARY_DIR}/pyconfig.cmake)
    message(STATUS "Python version ${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}.${Python_VERSION_PATCH}")
    message(STATUS " headers ${Python_INCLUDE_DIRS}")
    message(STATUS " numpy ${Python_NUMPY_FOUND}")
    #message(STATUS " library ${Python_LIBRARY_DIRS}") # not used
  endif()
endif()

if(Python_FOUND)
  # see if nosetests test runner is available
  execute_process(
    COMMAND ${PYTHON_EXECUTABLE} -m nose.core -V
    OUTPUT_QUIET
    ERROR_QUIET
    RESULT_VARIABLE _HAVE_NOSE
  )
  if(_HAVE_NOSE)
    if(NEED_PYTHON)
      message(SEND_ERROR "Unable to build Python support")
    else()
      message(STATUS "Can't find nosetests, not running tests")
    endif()
    set(HAVE_NOSE NO)
  else()
    set(HAVE_NOSE YES)
  endif()
endif()

find_package(Doxygen)

enable_testing()

add_subdirectory(src)

if(USE_PYTHON AND Python_NUMPY_FOUND)
  message(STATUS "Building python support")
  add_subdirectory(python/uscsi)
elseif(NEED_PYTHON)
  message(SEND_ERROR "Unable to build Python support")
else()
  message(STATUS "Omitting python support")
endif()

add_subdirectory(tools)

if(DOXYGEN_FOUND)
  file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/documentation)
  configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/documentation/Doxyfile.in
    ${CMAKE_CURRENT_BINARY_DIR}/documentation/Doxyfile
    @ONLY
  )
  add_custom_target(doc
    COMMAND ${DOXYGEN_EXECUTABLE} Doxyfile
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/documentation
  )
  message(STATUS "Will generate documentation")
else()
  message(STATUS "Skipping documentation generation (missing doxygen)")
endif()
