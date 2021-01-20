export SINGULARITY_BINDPATH=/afm02:/afm02
conda activate fatsegnetGPUnipype

python3 tool/run_FatSegNet.py \
-i /scratch/cvl/uqsbollm/2021-01-18-fatsegnet-input-preprocessed/preprocessed \
-outp /afm02/Q2/Q2653/data/2021-01-18-fatsegnet-output \
-loc