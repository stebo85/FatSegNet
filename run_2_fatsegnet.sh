export SINGULARITY_BINDPATH=/afm02:/afm02
conda activate fatsegnetGPUnipype

python3 tool/run_FatSegNet.py \
-i /scratch/cvl/uqsbollm/2021-01-18-fatsegnet-input-preprocessed/preprocessed \
-outp /scratch/cvl/uqsbollm/2021-01-18-fatsegnet-output \
-loc

#
#for qc in `ls sub*/QC/QC_0.png`; do echo $qc; done
#
:'
for qc in `ls sub*/QC/QC_0.png`; do display $qc; done
'