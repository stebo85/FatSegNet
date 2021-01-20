# module use /scratch/cvl-admin/neurodesk/local/containers/modules/
# ml fsl
# ml singularity
ml ants/2.3.4
# export LD_PRELOAD=''
export SINGULARITY_BINDPATH=/afm02:/afm02
# conda activate fatsegnetGPUnipype

python3 run_nipype_preprocessing.py \
    /scratch/cvl/uqsbollm/raine/2020-10-all-dixon-data \
    /scratch/cvl/uqsbollm/raine/preprocessed\
    --work_dir /scratch/cvl/uqsbollm/raine