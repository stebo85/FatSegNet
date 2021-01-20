from __future__ import division
import os
from nipype.interfaces.base import CommandLine, traits, TraitedSpec, File, CommandLineInputSpec, InputMultiPath
from nipype.interfaces.base.traits_extension import isdefined
from nipype.utils.filemanip import fname_presuffix, split_filename

def gen_filename(fname, suffix, newpath, use_ext=True):
    return fname_presuffix(fname, suffix=suffix, newpath=newpath, use_ext=use_ext)


class FatSegNetInputSpec(CommandLineInputSpec):
    phase_file = File(exists=True, desc='Phase image', mandatory=True, argstr="-p %s")
    mask_file = InputMultiPath(exists=True, desc='Image mask', mandatory=True, argstr="-m %s")
    TE = traits.Float(desc='Echo Time [sec]', mandatory=True, argstr="-t %f")
    b0 = traits.Float(desc='Field Strength [Tesla]', mandatory=True, argstr="-f %f")
    # Only support of one alpha here!
    alpha = traits.List([0.0015, 0.0005], minlen=2, maxlen=2, desc='Regularisation alphas', usedefault=True,
                        argstr="--alpha %s")
    # We only support one iteration - easier to handle in nipype
    erosions = traits.Int(5, desc='Number of mask erosions', usedefault=True, argstr="-e %d")
    out_suffix = traits.String("_qsm_recon", desc='Suffix for output files. Will be followed by 000 (reason - see CLI)',
                               usedefault=True, argstr="-o %s")


class FatSegNetOutputSpec(TraitedSpec):
    out_file = File(desc='Computed segmentations)


class FatSegNetInterface(CommandLine):
    input_spec = FatSegNetInputSpec
    output_spec = FatSegNetOutputSpec

    # We use here an interface to the CLI utility
    _cmd = "python3 tool/run_FatSegNet.py"

    def __init__(self, **inputs):
        super(FatSegNetInterface, self).__init__(**inputs)

    def _list_outputs(self):
        outputs = self.output_spec().get()
        pth, _, _ = split_filename(self.inputs.phase_file)
        outputs['out_file'] = gen_filename(self.inputs.phase_file, suffix=self.inputs.out_suffix + "_000",
                                           newpath=pth)
        return outputs