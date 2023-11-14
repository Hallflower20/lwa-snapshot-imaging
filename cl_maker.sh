#!/bin/sh
eval "$(conda shell.bash hook)"
conda activate /opt/devel/pipeline/envs/py38_orca
cd /opt/devel/pipeline/distributed-pipeline
pipenv run python /home/mmanders/scripts/gen_model_ms_stokes.py $1