from pathlib import Path
import os
import subprocess
from setuptools import setup, Extension
from Cython.Build import cythonize

conda_prefix = Path(os.environ["CONDA_PREFIX"])
pkg_config = conda_prefix / "share" / "pkgconfig"
os.environ["PKG_CONFIG"] = pkg_config.as_posix()

include_dir = subprocess.check_output(
    ["pkg-config", "--cflags-only-I", "freetype2"]
)
library_dir = subprocess.check_output(
    ["pkg-config", "--libs-only-L", "freetype2"]
)


setup(
    name="freetype",
    version="0.1",
    ext_modules=cythonize(
        Extension(
            "freetype",
            ["freetype.pyx"],
            include_dirs=[
                elt[2:] for elt in include_dir.decode().strip().split()
            ],
            library_dirs=[
                elt[2:] for elt in library_dir.decode().strip().split()
            ],
            libraries=["freetype"],
        )
    ),
)
