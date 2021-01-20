# module use /scratch/cvl-admin/neurodesk/local/containers/modules/
# ml fsl
# ml singularity
# export LD_PRELOAD=''
export SINGULARITY_BINDPATH=/afm02:/afm02
# conda activate fatsegnetGPUnipype

python3 run_nipype_fatsegnet.py \
    /afm02/Q2/Q2653/data/2021-01-18-dixon-subset \
    /afm02/Q2/Q2653/data/2021-01-18-fatsegnet-output \
    --work_dir /scratch/cvl/uqsbollm

# python3 tool/run_FatSegNet.py \
# -outp /afm02/Q2/Q2653/data/2021-01-18-fatsegnet-output/out \
# -loc \
# -water /afm02/Q2/Q2653/data/2021-01-18-fatsegnet-output/water_scaled/_subject_id_sub-12630/_water_scaled0/sub-12630_t1_vibe_dixon_tra_bh_2_groups_2_20170131180421_14_Eq_1_scaled.nii.gz \
# -fat /afm02/Q2/Q2653/data/2021-01-18-fatsegnet-output/fat_scaled/_subject_id_sub-12630/_fat_scaled0/sub-12630_t1_vibe_dixon_tra_bh_2_groups_2_20170131180421_15_Eq_1_scaled.nii.gz

# python3 tool/run_FatSegNet.py \
# -i /afm02/Q2/Q2653/data/2021-01-18-fatsegnet-output/scaled \
# -outp /afm02/Q2/Q2653/data/2021-01-18-fatsegnet-output/out \
# -loc