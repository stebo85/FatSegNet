export SINGULARITY_BINDPATH=/afm02:/afm02
# conda activate fatsegnetGPUnipype

python3 tool/run_FatSegNet.py \
-i /scratch/cvl/uqsbollm/raine/preprocessed/preprocessed_mul4 \
-outp /scratch/cvl/uqsbollm/raine/fatsegnet-output/mul4 \
-loc

#
#for qc in `ls sub*/QC/QC_0.png`; do echo $qc; done
#
:'
for qc in `ls sub*/QC/QC_0.png`; do display $qc; done

export s='sub-13130' && itksnap -g mul7/$s/MRI/FatImaging_F.nii.gz \
-o n4_mul2/$s/MRI/FatImaging_F.nii.gz \
 n4_mul2/$s/Segmentations/ALL_pred.nii.gz \
 mul2/$s/Segmentations/ALL_pred.nii.gz \
 n4_mul3/$s/Segmentations/ALL_pred.nii.gz \
 mul3/$s/Segmentations/ALL_pred.nii.gz \
 n4_mul4/$s/Segmentations/ALL_pred.nii.gz \
 mul4/$s/Segmentations/ALL_pred.nii.gz




'