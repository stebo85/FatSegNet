#!/usr/bin/env python3

import os.path
import os
import glob
from nipype.interfaces.fsl import BET, ImageMaths, ImageStats, MultiImageMaths, CopyGeom, Merge, UnaryMaths
from nipype.interfaces.utility import IdentityInterface, Function
from nipype.interfaces.io import SelectFiles, DataSink
from nipype.pipeline.engine import Workflow, Node, MapNode

import argparse

from interfaces import nipype_interface_fatsegnet as fatsegnet

def create_fatsegnet_workflow(
    subject_list,
    bids_dir,
    work_dir,
    out_dir,
    bids_templates,
):
    # create initial workflow
    wf = Workflow(name='workflow_fatsegnet', base_dir=work_dir)

    # use infosource to iterate workflow across subject list
    n_infosource = Node(
        interface=IdentityInterface(
            fields=['subject_id']
        ),
        name="subject_source"
        # input: 'subject_id'
        # output: 'subject_id'
    )
    # runs the node with subject_id = each element in subject_list
    n_infosource.iterables = ('subject_id', subject_list)

    # select matching files from bids_dir
    n_selectfiles = Node(
        interface=SelectFiles(
            templates=bids_templates,
            base_directory=bids_dir
        ),
        name='get_subject_data'
        # output: ['fat_composed', 'water_composed']
    )
    wf.connect([
        (n_infosource, n_selectfiles, [('subject_id', 'subject_id_p')])
    ])

    # scale data
    def scale(min_and_max):
        min_value = min_and_max[0][0]
        max_value = min_and_max[0][1]
        fsl_cmd = ""

        # set range to [0, 2pi]
        fsl_cmd += "-mul %.10f " % (5)

        return fsl_cmd

    mn_fat_stats = MapNode(
        # -R : <min intensity> <max intensity>
        interface=ImageStats(op_string='-R'),
        iterfield=['in_file'],
        name='get_stats_fat',
        # output: 'out_stat'
    )
    mn_water_stats = MapNode(
        # -R : <min intensity> <max intensity>
        interface=ImageStats(op_string='-R'),
        iterfield=['in_file'],
        name='get_stats_water',
        # output: 'out_stat'
    )
    wf.connect([
        (n_selectfiles, mn_fat_stats, [('fat_composed', 'in_file')]),
        (n_selectfiles, mn_water_stats, [('water_composed', 'in_file')])
    ])

    mn_fat_scaled = MapNode(
        interface=ImageMaths(suffix="_scaled"),
        name='fat_scaled',
        iterfield=['in_file']
        # inputs: 'in_file', 'op_string'
        # output: 'out_file'
    )
    mn_water_scaled = MapNode(
        interface=ImageMaths(suffix="_scaled"),
        name='water_scaled',
        iterfield=['in_file']
        # inputs: 'in_file', 'op_string'
        # output: 'out_file'
    )
    wf.connect([
        (n_selectfiles, mn_fat_scaled, [('fat_composed', 'in_file')]),
        (n_selectfiles, mn_water_scaled, [('water_composed', 'in_file')]),
        (mn_fat_stats, mn_fat_scaled, [(('out_stat', scale), 'op_string')]),
        (mn_water_stats, mn_water_scaled, [(('out_stat', scale), 'op_string')])
    ])


    mn_fatsegnet = MapNode(
            interface=fatsegnet.FatSegNetInterface(
                out_suffix='/afm02/Q2/Q2653/data/2021-01-18-fatsegnet-output/out_5'
            ),
            iterfield=['water_file', 'fat_file'],
            name='fatsegnet'
            # output: 'out_file'
        )

    wf.connect([
            (mn_fat_scaled, mn_fatsegnet, [('out_file', 'fat_file')]),
            (mn_water_scaled, mn_fatsegnet, [('out_file', 'water_file')]),
        ])


    # datasink
    n_datasink = Node(
        interface=DataSink(base_directory=bids_dir, container=out_dir),
        name='datasink'
    )

    wf.connect([
            (mn_fat_scaled, n_datasink, [('out_file', 'fat_scaled')]),
            (mn_water_scaled, n_datasink, [('out_file', 'water_scaled')]),
        ])

    return wf

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="FatSegNet Processing Pipeline",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        'bids_dir',
        help='bids directory'
    )

    parser.add_argument(
        'out_dir',
        help='output directory'
    )

    parser.add_argument(
        '--work_dir',
        default=None,
        const=None,
        help='work directory; defaults to \'work\' within \'out_dir\''
    )

    parser.add_argument(
        '--subjects',
        default=None,
        const=None,
        nargs='*',
        help='list of subjects as seen in bids_dir'
    )

    parser.add_argument(
        '--pbs',
        action='store_true',
        help='use PBS graph'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='debug mode'
    )

    args = parser.parse_args()

    if not args.work_dir: args.work_dir = args.out_dir

    # environment variables
    os.environ["FSLOUTPUTTYPE"] = "NIFTI_GZ"
    os.environ["PATH"] += os.pathsep + os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")

    this_dir = os.path.dirname(os.path.abspath(__file__))
    if "PYTHONPATH" in os.environ: os.environ["PYTHONPATH"] += os.pathsep + this_dir
    else:                          os.environ["PYTHONPATH"]  = this_dir

    if args.debug:
        from nipype import config
        config.enable_debug_mode()
        config.set('execution', 'stop_on_first_crash', 'true')
        config.set('execution', 'remove_unnecessary_outputs', 'false')
        config.set('execution', 'keep_inputs', 'true')
        config.set('logging', 'workflow_level', 'DEBUG')
        config.set('logging', 'interface_level', 'DEBUG')
        config.set('logging', 'utils_level', 'DEBUG')

    if not args.subjects:
        subject_list = [subj for subj in os.listdir(args.bids_dir) if 'sub' in subj]
    else:
        subject_list = args.subjects

    bids_templates = {
        'fat_composed': '{subject_id_p}/*15_Eq_1.nii.gz',
        'water_composed': '{subject_id_p}/*14_Eq_1.nii.gz',
    }

    wf = create_fatsegnet_workflow(
        subject_list=subject_list,
        bids_dir=os.path.abspath(args.bids_dir),
        work_dir=os.path.abspath(args.work_dir),
        out_dir=os.path.abspath(args.out_dir),
        bids_templates=bids_templates,
    )

    os.makedirs(os.path.abspath(args.work_dir), exist_ok=True)
    os.makedirs(os.path.abspath(args.out_dir), exist_ok=True)

    # run workflow
    if args.pbs:
        wf.run(
            plugin='PBSGraph',
            plugin_args={
                'qsub_args': '-A UQ-CAI -q Short -l nodes=1:ppn=1,mem=5GB,vmem=5GB,walltime=00:30:00'
            }
        )
    else:
        wf.run(
            plugin='MultiProc',
            plugin_args={'n_procs': 1}
            # plugin_args={
            #     'n_procs': int(os.environ["NCPUS"]) if "NCPUS" in os.environ else int(os.cpu_count())
            # }
        )