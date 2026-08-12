from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.build import can_run

class MiniLmConan(ConanFile):
    name = "mini-lm"
    version = "1.0.0"

    license = "MIT"
    author = "mm4cN"
    url = "https://github.com/mm4cN/mini-lm"
    description = "Mini Language Model implementation"
    topics = ("machine-learning", "language-model")

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        if not self.conf.get("tools.build:skip_test"):
            self.test_requires("gtest/1.17.0")

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(
            variables = {
                "BUILD_TESTING": "OFF" if self.conf.get("tools.build:skip_test") else "ON",
            }
        )
        cmake.build()
        if can_run and not self.conf.get("tools.build:skip_test"):
            cmake.test()

