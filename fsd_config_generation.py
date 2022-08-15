import db_config
from generation_parameters import get_params
import os
import json
import shutil
import pandas
import pickle
import numpy as np
import scipy.io
import csv
import librosa

# import pandas as pd

def copy_file(folder_name, source, destination, filename):
    os.makedirs(folder_name, exist_ok=True)
    destt = shutil.copyfile(source, destination)
    print(f'Copied {filename} to {destt}')
    return destt


def sub_id(inp_dic, onto):
    sub_id_lists = [inp_dic['id']]
    if inp_dic['child_ids']:
        for p in onto:
            if p['id'] in inp_dic['child_ids']:
                sub_id_lists = sub_id_lists + sub_id(p, onto)
    # else:
    #     sub_id_lists.append(inp_dic['id'])
    return sub_id_lists


task_id = '4'

params = get_params(task_id)
'''
In the First step we should read the dataset files
and put each file in its corresponding folder class
Hence we need to classify the files based on their ground truth label'''

db_name = params['db_name']  # 'Sub_FSDK50K'
db_dir = 'E:\SELD_2022\FSDK50K'
out_dir = 'E:\SELD_2022\classified_FSD50K'
# required_classes = ('Music', 'Musical_instrument', 'Domestic_sounds_and_home_sounds', 'Shatter,Glass',
#                     'Glass,Boom,Explosion', 'Dishes_and_pots_and_pans', 'Dog', 'Cat', 'Speech,Human_voice', 'Yell',
#                     'Shout', 'Ringtone,Telephone,Alarm', 'Burping_and_eructation', 'Crying_and_sobbing',
#                     'Cutlery_and_silverware', 'Walk_and_footsteps', 'Sneeze', 'Purr', 'Screaming',
#                     'Laughter,Human_voice', 'Human_voice', 'Cough', 'Respiratory_sounds', 'Singing',
#                     'Chewing_and_mastication', 'Breathing', 'Gasp', 'Sigh', 'Run', 'Computer_keyboard,Typing',
#                     'Domestic_sounds_and_home_sounds')
'''(Speech_synthesizer, Whispering,Human_voice, etc) should not be included in the dataset. so we look at the audioset
Ontology to find relative data, from parent to child search direction'''

f = open('ontology.json')
ontology = json.load(f)

Parent_list0 = ['Human sounds', 'Animal', 'Music', 'Sounds of things']
Desired_dic = {}
undesired_dic = {}

sub_id_flag = False

for P1 in ontology:
    if P1['name'] in Parent_list0:
        print(f"This is the subsections for {P1['name']}")  # Human Sounds
        inp1 = input('If you want to add classes from this Parent press 1, else press anything else')
        if inp1 == '1':
            sub_id_flag = False
            for P2 in ontology:
                if P2['id'] in P1['child_ids']:
                    print(P2['name'])  # Human voice, Respiratory sounds
                    inp2 = input('If you want to add classes from this Parent press 1, if all, press 2, else press '
                                 'anything else')
                    if inp2 == '1':
                        sub_id_flag = False
                        for P3 in ontology:
                            if P3['id'] in P2['child_ids']:
                                print(P3['name'])  # Speech, Cough
                                inp3 = input(
                                    'If you want to add classes from this Parent press 1, if all, press 2, else press '
                                    'anything else')
                                if inp3 == '1':
                                    sub_id_flag = False
                                    for P4 in ontology:
                                        if P4['id'] in P3['child_ids']:
                                            print(P4['name'])  # conversation, Throat clearing
                                            inp4 = input(
                                                'If you want to add classes from this Parent press 1, if all, press 2, else press '
                                                'anything else')
                                            if inp4 == '1':
                                                sub_id_flag = False
                                                for P5 in ontology:
                                                    if P5['id'] in P4['child_ids']:
                                                        print(P5['name'])  ###male conversation
                                                        inp5 = input(
                                                            'If you want to add this class from this Parent press 1, else press '
                                                            'anything else')
                                                        if inp5 == '1':
                                                            Desired_dic[P5['name']] = sub_id(P5, ontology)
                                                            sub_id_flag = True
                                                        else:
                                                            undesired_dic[P5['name']] = sub_id(P5, ontology)
                                                if not sub_id_flag:
                                                    Desired_dic[P4['name']] = P4['id']
                                                    sub_id_flag = True
                                            elif inp4 == '2':
                                                Desired_dic[P4['name']] = sub_id(P4, ontology)
                                                sub_id_flag = True
                                            else:
                                                undesired_dic[P4['name']] = sub_id(P4, ontology)
                                    if not sub_id_flag:
                                        Desired_dic[P3['name']] = [P3['id']]
                                        sub_id_flag = True
                                elif inp3 == '2':
                                    Desired_dic[P3['name']] = sub_id(P3, ontology)
                                    sub_id_flag = True
                                else:
                                    undesired_dic[P3['name']] = sub_id(P3, ontology)
                        if not sub_id_flag:
                            Desired_dic[P2['name']] = [P2['id']]
                            sub_id_flag = True
                    elif inp2 == '2':
                        Desired_dic[P2['name']] = sub_id(P2, ontology)
                        sub_id_flag = True
                    else:
                        undesired_dic[P2['name']] = sub_id(P2, ontology)
        else:
            undesired_dic[P1['name']] = sub_id(P1, ontology)

db_label_dir = os.path.join(db_dir, 'FSD50K.ground_truth')
dev_df = pandas.read_csv(os.path.join(db_label_dir, 'dev.csv'))
eval_df = pandas.read_csv(os.path.join(db_label_dir, 'eval.csv'))
print('ontology printed')
# def examp(sam):
#     return True
# [examp(i) for i in dev_df.values]
number_of_sample = 0
mixed_files = 0
undesired_file_num = 0
undesired_mids = [i for y in undesired_dic.keys() for i in undesired_dic[y]]
for sample in dev_df.values:
    mixed_flag = False
    fname = str(sample[0]) + '.wav'
    flabel = sample[1]
    fmids = sample[2].split(',')
    fsplit = sample[3]
    flabel = flabel.replace("_", " ")
    flabels = flabel.split(',')
    tempclass = None
    for fmid in fmids:
        if fmid in undesired_mids:
            undesired_file_num += 1
            tempclass = None
            break
        else:
            for classes in Desired_dic.keys():
                if fmid in Desired_dic[classes]:
                    if tempclass is None:
                        tempclass = classes
                    else:
                        if tempclass != classes:
                            print('mixed file')
                            mixed_flag = True

    if tempclass != None:
        foldname = os.path.join(out_dir, tempclass.replace(' ', '_').replace(',', ''), 'train')
        copy_file(foldname,
                  source=os.path.join(db_dir, 'FSD50K.dev_audio', fname),
                  destination=os.path.join(foldname, fname), filename=fname)
        if mixed_flag:
            mixed_files += 1
        else:
            number_of_sample += 1

print(f'number of samples = {number_of_sample}')
print(f'number of mixed samples = {mixed_files}')
print(f'number of undesired file = {undesired_file_num}')

number_of_sample = 0
mixed_files = 0
undesired_file_num = 0
undesired_mids = [i for y in undesired_dic.keys() for i in undesired_dic[y]]
for sample in eval_df.values:
    mixed_flag = False
    fname = str(sample[0]) + '.wav'
    flabel = sample[1]
    fmids = sample[2].split(',')
    # fsplit = sample[3]
    flabel = flabel.replace("_", " ")
    flabels = flabel.split(',')
    tempclass = None
    for fmid in fmids:
        if fmid in undesired_mids:
            undesired_file_num += 1
            tempclass = None
            break
        else:
            for classes in Desired_dic.keys():
                if fmid in Desired_dic[classes]:
                    if tempclass is None:
                        tempclass = classes
                    else:
                        if tempclass != classes:
                            print('mixed file')
                            mixed_flag = True

    if tempclass != None:
        foldname = os.path.join(out_dir, tempclass.replace(' ', '_').replace(',', ''), 'test')
        copy_file(foldname,
                  source=os.path.join(db_dir, 'FSD50K.eval_audio', fname),
                  destination=os.path.join(foldname, fname), filename=fname)
        if mixed_flag:
            mixed_files += 1
        else:
            number_of_sample += 1

print(f'number of samples = {number_of_sample}')
print(f'number of mixed samples = {mixed_files}')
print(f'number of undesired file = {undesired_file_num}')

params['active_classes'] = [i for i in range(len(os.listdir(params['db_path'])))]

class_mobiliy = []
for fold in os.listdir(params['db_path']):
    print('0 has no mobility, 1 is mobil like walking, and 2 is either static or dynamic')
    inp = input(f'what is the mobility of {fold}')
    class_mobiliy.append(int(inp))


def make_selected_filelist(self):
    folds = []
    folds_names = ['train', 'test']  # TODO: make it more generic
    nb_folds = len(folds_names)
    class_list = self._classes  # list(self._classes.keys())

    for ntc in range(self._nb_classes):
        classpath = os.path.join(self._db_path, class_list[ntc])

        per_fold = []
        for nf in range(nb_folds):
            foldpath = os.path.join(classpath, folds_names[nf])
            foldcont = os.listdir(foldpath)
            nb_subdirs = len(foldcont)
            filelist = os.listdir(foldpath)
            # for ns in range(nb_subdirs):
            #     subfoldcont = os.listdir(os.path.join(foldpath, foldcont[ns]))
            #     for nfl in range(len(subfoldcont)):
            #         if subfoldcont[nfl][0] != '.' and subfoldcont[nfl].endswith('.wav'):
            #             filelist.append(
            #                 os.path.join(class_list[ntc], folds_names[nf], foldcont[ns], subfoldcont[nfl]))
            per_fold.append(filelist)
        folds.append(per_fold)

    return folds
def costumr_load_db_fileinfo_fsd(self):
    samplelist_per_fold = []
    folds = make_selected_filelist(self)
    folds_names = ['train', 'test']  # TODO: make it more generic

    for nfold in range(self._nb_folds):
        print('Preparing sample list for fold {}'.format(str(nfold + 1)))
        counter = 1
        samplelist = {'class': np.array([]), 'audiofile': np.array([]), 'duration': np.array([]), 'onoffset': [],
                      'nSamples': [],
                      'nSamplesPerClass': np.array([]), 'meanStdDurationPerClass': np.array([]),
                      'minMaxDurationPerClass': np.array([])}
        for ncl in range(self._nb_classes):
            nb_samples_per_class = len(folds[ncl][nfold])

            for ns in range(nb_samples_per_class):
                samplelist['class'] = np.append(samplelist['class'], ncl)
                samplelist['audiofile'] = np.append(samplelist['audiofile'], folds[ncl][nfold][ns])
                audiopath = os.path.join(self._db_path, self._classes[ncl], folds_names[nfold], folds[ncl][nfold][ns])
                audio, sr = librosa.load(audiopath)
                duration = len(audio) / float(sr)
                samplelist['duration'] = np.append(samplelist['duration'], duration)
                samplelist['onoffset'].append(np.array([[0., duration], ]))
                samplelist['nSamples'].append(counter)
                counter += 1
        samplelist['onoffset'] = np.squeeze(np.array(samplelist['onoffset'], dtype=object))
        for n_class in range(self._nb_classes):
            class_idx = (samplelist['class'] == n_class)
            samplelist['nSamplesPerClass'] = np.append(samplelist['nSamplesPerClass'], np.sum(class_idx))
            if n_class == 0:
                samplelist['meanStdDurationPerClass'] = np.array(
                    [[np.mean(samplelist['duration'][class_idx]), np.std(samplelist['duration'][class_idx])]])
                samplelist['minMaxDurationPerClass'] = np.array(
                    [[np.min(samplelist['duration'][class_idx]), np.max(samplelist['duration'][class_idx])]])
            else:
                samplelist['meanStdDurationPerClass'] = np.vstack((samplelist['meanStdDurationPerClass'], np.array(
                    [np.mean(samplelist['duration'][class_idx]), np.std(samplelist['duration'][class_idx])])))
                samplelist['minMaxDurationPerClass'] = np.vstack((samplelist['minMaxDurationPerClass'], np.array(
                    [np.min(samplelist['duration'][class_idx]), np.max(samplelist['duration'][class_idx])])))
        samplelist_per_fold.append(samplelist)

    return samplelist_per_fold


fsd_config_cstm = db_config.DBConfig(params=params)
fsd_config_cstm._fs = 44100
fsd_config_cstm._classes = os.listdir(params['db_path'])
fsd_config_cstm._nb_classes = len(fsd_config_cstm._classes)
fsd_config_cstm._class_mobility = class_mobiliy  # [2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0]  # todo
fsd_config_cstm._apply_class_gains = False
fsd_config_cstm._samplelist = costumr_load_db_fileinfo_fsd(fsd_config_cstm)

db_handler = open('db_config_fsd_custom_carewell.obj', 'wb')
pickle.dump(fsd_config_cstm, db_handler)
db_handler.close()
