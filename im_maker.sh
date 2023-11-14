#!/bin/sh
/opt/bin/wsclean -pol I -multiscale -multiscale-scale-bias 0.9 -size 4096 4096 -scale 0.03 -niter 10000 -mgain 0.85 -weight briggs 0 -name $1 $2