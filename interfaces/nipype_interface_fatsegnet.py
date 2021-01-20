from __future__ import division
import os
import re
from nipype.interfaces.base import CommandLine, traits, TraitedSpec, File, CommandLineInputSpec


class FatSegNetInputSpec(CommandLineInputSpec):
    water_file = File(exists=True, desc='water image', mandatory=True, argstr="-water %s")
    fat_file = File(exists=True, desc='fat image', mandatory=True, argstr="-fat %s")
    out_suffix = traits.String(desc='Suffix for output files.)',
                               usedefault=True, argstr="-outp %s")


class FatSegNetOutputSpec(TraitedSpec):
    out_file = File(desc='Computed segmentations')


class FatSegNetInterface(CommandLine):
    input_spec = FatSegNetInputSpec
    output_spec = FatSegNetOutputSpec

    whereAmI=os.path.dirname(os.path.abspath(__file__))
    _cmd = "python3 " + whereAmI + "/../tool/run_FatSegNet.py -loc"

    def __init__(self, **inputs):
        super(FatSegNetInterface, self).__init__(**inputs)

    def _list_outputs(self):
        outputs = self.output_spec().get()
        # id = re.split('_subject_id_',self.inputs.water_file[1])
        # id = re.split('/',id)[0]
        # print('inferred subject id: ', id)
        # outputs['ALL_pred'] = os.path.join(self.inputs.out_suffix,id,'Segmentations','ALL_pred.nii.gz') 
        return outputs