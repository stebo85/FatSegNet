# module use /scratch/cvl-admin/neurodesk/local/containers/modules/
# ml fsl
# ml singularity
ml ants/2.3.4
# export LD_PRELOAD=''
export SINGULARITY_BINDPATH=/afm02:/afm02
# conda activate fatsegnetGPUnipype

python3 run_nipype_fatsegnet.py \
    /afm02/Q2/Q2653/data/2021-01-18-dixon-subset \
    /scratch/cvl/uqsbollm/2021-01-18-fatsegnet-input-preprocessed \
    --work_dir /scratch/cvl/uqsbollm