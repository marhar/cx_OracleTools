Copied from sourceforge:

1c2b73f57b1fa8eb169a5ed1be5cb9a8 43926 Dec 10 16:20 cx_OracleTools-8.0.tar.gz
37eb470ca0a10e6b61bc4f1e4777cde2 38145 Dec 10 15:15 cx_PyGenLib-2.4.tar.gz
c98bcad8ecf240768c0f83bedc363102 37260 Dec 10 15:15 cx_PyOracleLib-2.4.tar.gz

1. build and install cx_Oracle.

2. build and install cx_PyGenLib and cx_PyOracleLib (included here)

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
