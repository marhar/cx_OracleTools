Copied from sourceforge:

fca8e9ee1ae8d2fb7437224a0f071b55 35433 Dec 17 08:59 cx_Logging-2.1.tar.gz
1c2b73f57b1fa8eb169a5ed1be5cb9a8 43926 Dec 10 16:20 cx_OracleTools-8.0.tar.gz
c7515a9b03185c2ad2f08726292f8c5e 70262 Dec 17 09:32 cx_PyGenLib-3.0.tar.gz
bc5dadda1d23ab5fbda7f0c3f149630c 40180 Dec 17 09:32 cx_PyOracleLib-2.5.tar.gz

1. build and install cx_Oracle.

2. build and install cx_Logging, cx_PyGenLib, and cx_PyOracleLib (included here)

- cd cx_Logging
- python setup.py build
- python setup.py install
- cd cx_PyGenLib
- python setup.py build
- python setup.py install
- cd cx_PyOracleLib
- python setup.py build
- python setup.py install

3. Build cx_OracleTools

- copy Options.py to site-packages
- copy programs to bin

wrapped up in junky install.sh script which you will need to modify.
