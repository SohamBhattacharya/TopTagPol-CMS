# ctypes_test.py
import ctypes
import pathlib

if __name__ == "__main__":
    # Load the shared library into ctypes
    libname = "/nfs/dust/cms/user/sobhatta/work/TopTagPol/Analysis/KLFitter/build/lib/libKLFitter.so"
    c_lib = ctypes.CDLL(libname)

