from conans import ConanFile, CMake, tools
import os


class VolteventConan(ConanFile):
    name = "volt_event"
    version = "0.0.1"
    license = "GPL3"
    author = "SirHall"
    url = "https://www.github.com/SirHall/volt_event"
    description = "Library aimed at handling various events in C++"
    topics = ("C++", "event", "callback")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
    exports_sources = "include/**"
    no_copy_source = True

    def source(self):
        git = tools.Git(folder="volt_event")
        git.clone("https://www.github.com/SirHall/volt_event.git", "master")
        # self.run("git clone ")

        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("volt_event/CMakeLists.txt", "project(volt_ge_event)",
                              '''project(volt_ge_event)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="volt_event")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include/", src="volt_event/volt_event/include")
        self.copy("*.hpp", dst="include/", src="volt_event/volt_event/include")
        self.copy("*volt_event.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    # def package_info(self):
        # self.cpp_info.libs = ["volt_event"]
