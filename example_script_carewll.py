import sys
import numpy as np
from db_config import DBConfig
from metadata_synthesizer import MetadataSynthesizer
from audio_synthesizer import AudioSynthesizer
from audio_mixer import AudioMixer
import pickle
from generation_parameters import get_params

##############
############## THIS IS AN EXEMPLARY SCRIPT GENERATING DATA
############## SIMILAR TO THE DCASE2022 dataset
##############


# use parameter set defined by user
task_id = '4'

params = get_params(task_id)
params['nb_mixtures_per_fold'] = [6, 3]   # todo
### Create database config based on params (e.g. filelist name etc.)
# db_config = DBConfig(params)

# LOAD DB-config which is already done
db_handler = open('db_config_fsd_custom_carewell.obj', 'rb')
db_config = pickle.load(db_handler)
db_handler.close()
# todo: if mixtures are less than the number of samples, to use all samples, it is better to find the start randomly
# create mixture synthesizer class
noiselessSynth = MetadataSynthesizer(db_config, params, 'target_noiseless')

# create mixture targets
mixtures_target, mixture_setup_target, foldlist_target = noiselessSynth.create_mixtures()

# calculate statistics and create metadata structure
metadata, stats = noiselessSynth.prepare_metadata_and_stats()
# todo: should save metadata or class instance for later in case something goes wrong
# write metadata to text files
noiselessSynth.write_metadata()

if not params['audio_format'] == 'both':  # create a dataset of only one data format (FOA or MIC)
    # create audio synthesis class and synthesize audio files for given mixtures
    noiselessAudioSynth = AudioSynthesizer(params, mixtures_target, mixture_setup_target, db_config,
                                           params['audio_format'])
    noiselessAudioSynth.synthesize_mixtures()

    # mix the created audio mixtures with background noise
    audioMixer = AudioMixer(params, db_config, mixtures_target, mixture_setup_target, params['audio_format'],
                            'target_noisy')
    audioMixer.mix_audio()
else:
    # create audio synthesis class and synthesize audio files for given mixtures
    noiselessAudioSynth = AudioSynthesizer(params, mixtures_target, mixture_setup_target, db_config, 'foa')
    noiselessAudioSynth.synthesize_mixtures()
    noiselessAudioSynth2 = AudioSynthesizer(params, mixtures_target, mixture_setup_target, db_config, 'mic')
    noiselessAudioSynth2.synthesize_mixtures()

    # mix the created audio mixtures with background noise
    audioMixer = AudioMixer(params, db_config, mixtures_target, mixture_setup_target, 'foa', 'target_noisy')
    audioMixer.mix_audio()
    audioMixer2 = AudioMixer(params, db_config, mixtures_target, mixture_setup_target, 'mic', 'target_noisy')
    audioMixer2.mix_audio()