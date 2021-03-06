"""Distutils script for cx_Logging.

Windows platforms:
    python setup.py build --compiler=mingw32 install

Unix platforms
    python setup.py build install

"""

import distutils.command.bdist_rpm
import distutils.command.build_ext
import distutils.command.install_data
import distutils.util
import os
import sys

from distutils.core import setup
from distutils.extension import Extension
from distutils import sysconfig

BUILD_VERSION = "2.1"

# define class to ensure the file name given includes the Python version
class bdist_rpm(distutils.command.bdist_rpm.bdist_rpm):

    def run(self):
        distutils.command.bdist_rpm.bdist_rpm.run(self)
        specFile = os.path.join(self.rpm_base, "SPECS",
                "%s.spec" % self.distribution.get_name())
        queryFormat = "%{name}-%{version}-%{release}.%{arch}.rpm"
        command = "rpm -q --qf '%s' --specfile %s" % (queryFormat, specFile)
        origFileName = os.popen(command).read()
        parts = origFileName.split("-")
        parts.insert(2, "py%s%s" % sys.version_info[:2])
        newFileName = "-".join(parts)
        self.move_file(os.path.join("dist", origFileName),
        os.path.join("dist", newFileName))


# define class to ensure that linking against the library works for normal
# C programs while maintaining the name that Python expects
class build_ext(distutils.command.build_ext.build_ext):
    import distutils
    import os
    import sys
    if sys.platform == "win32":
        user_options = distutils.command.build_ext.build_ext.user_options + [
                ('build-implib=', None,
                'directory for import library')
        ]

    def build_extension(self, ext):
        import distutils.command.build_ext
        import os
        import sys
        extraLinkArgs = ext.extra_link_args = []
        if sys.platform == "win32":
            self.mkpath(self.build_implib)
            if self.compiler.compiler_type == "msvc":
                self.importLibraryName = os.path.join(self.build_implib,
                        "%s.lib" % ext.name)
                extraLinkArgs.append("/IMPLIB:%s" % self.importLibraryName)
            else:
                self.importLibraryName = os.path.join(self.build_implib,
                        "lib%s.a" % ext.name)
                extraLinkArgs.append("-Wl,--add-stdcall-alias")
                extraLinkArgs.append("-Wl,--enable-stdcall-fixup")
                extraLinkArgs.append("-Wl,--out-implib=%s" % \
                        self.importLibraryName)
            ext.libraries = ["ole32"]
        else:
            fileName = self.get_ext_filename(ext.name)
            if sys.platform.startswith("aix"):
                extraLinkArgs.append("-Wl,-so%s" % fileName)
            else:
                extraLinkArgs.append("-Wl,-soname,%s" % fileName)
        distutils.command.build_ext.build_ext.build_extension(self, ext)

    def finalize_options(self):
        import distutils.command.build_ext
        distutils.command.build_ext.build_ext.finalize_options(self)
        import os
        import sys
        if sys.platform == "win32" and self.build_implib is None:
            dir = "implib.%s-%s" % \
                    (distutils.util.get_platform(), sys.version[:3])
            self.build_implib = os.path.join("build", dir)

    def initialize_options(self):
        import distutils.command.build_ext
        distutils.command.build_ext.build_ext.initialize_options(self)
        import sys
        if sys.platform == "win32":
            self.build_implib = None


# define class to ensure that the import library (Windows) is installed
# properly; this is not relevant on other platforms
class install_data(distutils.command.install_data.install_data):

    def run(self):
        distutils.command.install_data.install_data.run(self)
        if sys.platform == "win32":
            command = self.get_finalized_command("build_ext")
            dir = os.path.join(self.install_dir, "Libs")
            self.mkpath(dir)
            baseName = os.path.basename(command.importLibraryName)
            targetFileName = os.path.join(dir, baseName)
            self.copy_file(command.importLibraryName, targetFileName)
            self.outfiles.append(targetFileName)


# setup macros
defineMacros = [
        ("CX_LOGGING_CORE",  None),
        ("BUILD_VERSION", BUILD_VERSION)
]

# define the list of files to be included as documentation for Windows
dataFiles = None
if sys.platform in ("win32", "cygwin"):
    baseName = "cx_Logging-doc"
    dataFiles = [(baseName, [ "LICENSE.TXT", "README.TXT", "HISTORY.txt"])]
    for dir in ("html", "html/_static", "test"):
        files = []
        fullDirName = "%s/%s" % (baseName, dir)
        for name in os.listdir(dir):
            if name.startswith("."):
                continue
            fullName = "%s/%s" % (dir, name)
            if os.path.isdir(fullName):
                continue
            files.append(fullName)
        dataFiles.append((fullDirName, files))
docFiles = "LICENSE.txt HISTORY.txt README.txt html test"
options = dict(bdist_rpm = dict(doc_files = docFiles))

# define the classifiers for the project
classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Python Software Foundation License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
]

exportSymbols = [
        "StartLogging",
        "StartLoggingEx",
        "StartLoggingForPythonThread",
        "StartLoggingForPythonThreadEx",
        "StartLoggingStderr",
        "StartLoggingStderrEx",
        "StartLoggingStdout",
        "StartLoggingStdoutEx",
        "StartLoggingFromEnvironment",
        "StopLogging",
        "StopLoggingForPythonThread",
        "LogMessage",
        "LogMessageV",
        "LogMessageVaList",
        "LogMessageForPythonV",
        "WriteMessageForPython",
        "LogDebug",
        "LogInfo",
        "LogWarning",
        "LogError",
        "LogCritical",
        "LogTrace",
        "GetLoggingLevel",
        "SetLoggingLevel",
        "LogPythonObject",
        "LogPythonException",
        "LogPythonExceptionWithTraceback",
        "LogConfiguredException",
        "GetLoggingState",
        "SetLoggingState",
        "IsLoggingStarted",
        "IsLoggingAtLevelForPython"
]

if sys.platform == "win32":
    exportSymbols.extend([
            "LogWin32Error",
            "LogGUID",
            "StartLoggingW",
            "StartLoggingExW",
            "LogMessageW",
            "LogDebugW",
            "LogInfoW",
            "LogWarningW",
            "LogErrorW",
            "LogCriticalW",
            "LogTraceW"
    ])

# setup the extension
extension = Extension(
        name = "cx_Logging",
        define_macros = defineMacros,
        export_symbols = exportSymbols,
        sources = ["cx_Logging.c"],
        depends = ["cx_Logging.h"])

# perform the setup
setup(
        name = "cx_Logging",
        cmdclass = dict(build_ext = build_ext, install_data = install_data,
                bdist_rpm = bdist_rpm),
        version = BUILD_VERSION,
        description = "Python and C interfaces for logging",
        data_files = dataFiles,
        long_description = "Python and C interfaces for logging",
        author = "Anthony Tuininga",
        author_email = "anthony.tuininga@gmail.com",
        maintainer = "Anthony Tuininga",
        maintainer_email = "anthony.tuininga@gmail.com",
        url = "http://cx-logging.sourceforge.net",
        keywords = "logging",
        classifiers = classifiers,
        license = "Python Software Foundation License",
        ext_modules = [extension],
        options = options)

