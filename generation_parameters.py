# Parameters used in the data generation process.


def get_params(argv='1'):
    print("SET: {}".format(argv))
    # ########### default parameters (NIGENS data) ##############
    params = dict(
        db_name='nigens',  # name of the audio dataset used for data generation
        rirpath='/scratch/asignal/krauseda/DCASE_data_generator/RIR_DB',
        # path containing Room Impulse Responses (RIRs)
        mixturepath='E:/DCASE2022/TAU_Spatial_RIR_Database_2021/Dataset-NIGENS',
        # output path for the generated dataset
        noisepath='/scratch/asignal/krauseda/DCASE_data_generator/Noise_DB',
        # path containing background noise recordings
        nb_folds=2,  # number of folds (default 2 - training and testing)
        rooms2fold=[[10, 6, 1, 4, 3, 8],  # FOLD 1, rooms assigned to each fold (0's are ignored)
                    [9, 5, 2, 0, 0, 0]],  # FOLD 2
        db_path='E:/DCASE2022/TAU_Spatial_RIR_Database_2021/Code/NIGENS',
        # path containing audio events to be utilized during data generation
        max_polyphony=3,  # maximum number of overlapping sound events
        active_classes=[0, 1, 2, 3, 5, 6, 8, 9, 10, 11, 12, 13],  # list of sound classes to be used for data generation
        nb_mixtures_per_fold=[900, 300],  # if scalar, same number of mixtures for each fold
        mixture_duration=60.,  # in seconds
        event_time_per_layer=40.,  # in seconds (should be less than mixture_duration)
        audio_format='both',  # 'foa' (First Order Ambisonics) or 'mic' (four microphones) or 'both'
    )

    # ########### User defined parameters ##############
    if argv == '1':
        print("USING DEFAULT PARAMETERS FOR NIGENS DATA\n")

    elif argv == '2':  ###### FSD50k DATA
        params['db_name'] = 'fsd50k'
        params['db_path'] = '/scratch/asignal/krauseda/DCASE_data_generator/Code/FSD50k'
        params['mixturepath'] = '/scratch/asignal/krauseda/Data-FSD'
        params['active_classes'] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        params['max_polyphony'] = 2

    elif argv == '3':  ###### NIGENS interference data
        params['active_classes'] = [4, 7, 14]
        params['max_polyphony'] = 1

    elif argv == '4':  #####user defined params
        params['db_name'] = 'Sub_FSDK50K'  # name of the audio dataset used for data generation
        params['rirpath'] = 'E:\SELD_2022\TAU-SRIR_DB'  # path containing Room Impulse Responses (RIRs)
        params['mixturepath'] = 'E:/SELD_2022/Costum_Mixture'  # output path for the generated dataset
        params['noisepath'] = 'E:\SELD_2022\TAU-SNoise_DB'  # path containing background noise recordings
        params['nb_folds'] = 2  # number of folds (default 2 - training and testing)
        params['rooms2fold'] = [[10, 6, 1, 4, 3, 8],  # FOLD 1, rooms assigned to each fold (0's are ignored)
                                [9, 5, 2, 0, 0, 0]]  # FOLD 2
        params[
            "db_path"] = 'E:\SELD_2022\classified_FSD50K'  # path containing audio events to be utilized during data generation
        params['max_polyphony'] = 2  # maximum number of overlapping sound events
        params['active_classes'] = [0, 1, 2, 3, 4]  # , 2, 3, 5, 6, 8, 9, 10, 11, 12, 13]  # todo
        params['nb_mixtures_per_fold'] = [900, 300]  # if scalar, same number of mixtures for each fold
        params['mixture_duration'] = 60.  # in seconds
        params['event_time_per_layer'] = 40.  # in seconds (should be less than mixture_duration)
        params['audio_format'] = 'foa'  # 'both'  # 'foa' (First Order Ambisonics) or 'mic' (four microphones) or
        # 'both'

    else:
        print('ERROR: unknown argument {}'.format(argv))
        exit()

    for key, value in params.items():
        print("\t{}: {}".format(key, value))
    return params
