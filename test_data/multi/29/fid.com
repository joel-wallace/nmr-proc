#!/bin/csh

bruk2pipe -verb -in ./fid \
  -bad 0.0 -ext -aswap -AMX -decim 213.333333333333 -dspfvs 21 -grpdly 76  \
  -xN             66560  \
  -xT             33280  \
  -xMODE            DQD  \
  -xSW        93750.000  \
  -xOBS         470.611  \
  -xCAR         -60.000  \
  -xLAB             19F  \
  -ndim               1  \
| nmrPipe -fn MULT -c 1.52588e-02 \
  -out ./test.fid -ov

#
# nmrDraw -process -in test.fid -fid test.fid

