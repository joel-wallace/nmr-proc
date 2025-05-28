#!/bin/csh

#
# Basic 2D Phase-Sensitive Processing:
#   Cosine-Bells are used in both dimensions.
#   Use of "ZF -auto" doubles size, then rounds to power of 2.
#   Use of "FT -auto" chooses correct Transform mode.
#   Imaginaries are deleted with "-di" in each dimension.
#   Phase corrections should be inserted by hand.

nmrPipe -in test.fid \
#| nmrPipe  -fn SP -off 0.5 -end 1.00 -pow 1 -c 0.5    \
| nmrPipe -fn EM  -lb 10.0 -c 0.5                               \
| nmrPipe  -fn ZF -auto                               \
| nmrPipe  -fn FT -auto                               \
| nmrPipe  -fn PS -p0 -22 -p1 0.00 -di -verb         \
| nmrPipe -fn BASE -nw 10 -nl -70ppm -50ppm                    \
| nmrPipe -fn EXT -x1 -70ppm -xn -50ppm -sw                                  \
   -ov -out test.ft1

pipe2txt.tcl -index ppm test.ft1>data.txt
