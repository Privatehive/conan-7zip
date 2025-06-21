#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan import ConanFile
from conan.tools.files import download, copy, unzip, rename, rm
from conan.errors import ConanInvalidConfiguration
import json

required_conan_version = ">=2.0"

class NsisConan(ConanFile):

    jsonInfo = json.load(open("info.json", 'r'))
    # ---Package reference---
    name = jsonInfo["projectName"]
    version = jsonInfo["version"]
    user = jsonInfo["domain"]
    channel = "stable"
    # ---Metadata---
    description = jsonInfo["projectDescription"]
    license = jsonInfo["license"]
    author = jsonInfo["vendor"]
    topics = jsonInfo["topics"]
    homepage = jsonInfo["homepage"]
    url = jsonInfo["repository"]
    # ---Requirements---
    requires = []
    tool_requires = []
    # ---Sources---
    exports = ["info.json"]
    exports_sources = []
    # ---Binary model---
    settings = "os", "arch"
    options = {}
    default_options = {}
    # ---Build---
    generators = []
    # ---Folders---
    no_copy_source = True

    def validate(self):
        valid_os = ["Windows", "Linux", "Macos"]
        if str(self.settings.os) not in valid_os:
            raise ConanInvalidConfiguration(f"{self.name} {self.version} is only supported for the following operating systems: {valid_os}")
        valid_arch = ["x86_64"]
        if self.settings.os == "Macos":
            valid_arch = ["x86_64", "armv8"]
        if str(self.settings.arch) not in valid_arch:
            raise ConanInvalidConfiguration(f"{self.name} {self.version} is only supported for the following architectures on {self.settings.os}: {valid_arch}")

    def build(self):
        download(self, **self.conan_data["sources"][self.version][str(self.settings.os)])
        if self.settings.os == "Linux":
            unzip(self, "7z.tar.xz", keep_permissions=True, pattern="7zzs")
            rename(self, "7zzs", "7z")
            rm(self, "7z.tar.xz", self.build_folder)
        if self.settings.os == "Macos":
            unzip(self, "7z.tar.xz", keep_permissions=True, pattern="7zz")
            rename(self, "7zz", "7z")
            rm(self, "7z.tar.xz", self.build_folder)

    def package(self):
        copy(self, pattern="7z*", src=self.build_folder, dst=self.package_folder)

    def package_info(self):
        self.output.info('Prepending to PATH environment variable: %s' % self.package_folder)
        self.buildenv_info.prepend_path("PATH", self.package_folder)
