# import db_config
import os
import json

import pandas
import pandas as pd

'''
In the First step we should read the dataset files
and put each file in its corresponding folder class
Hence we need to classify the files based on their ground truth label'''

db_name = 'Sub_FSDK50K'
db_dir = 'E:\SELD_2022\FSDK50K'
required_classes = ('Music', 'Musical_instrument', 'Domestic_sounds_and_home_sounds', 'Shatter,Glass',
                    'Glass,Boom,Explosion', 'Dishes_and_pots_and_pans', 'Dog', 'Cat', 'Speech,Human_voice', 'Yell',
                    'Shout', 'Ringtone,Telephone,Alarm', 'Burping_and_eructation', 'Crying_and_sobbing',
                    'Cutlery_and_silverware', 'Walk_and_footsteps', 'Sneeze', 'Purr', 'Screaming',
                    'Laughter,Human_voice', 'Human_voice', 'Cough', 'Respiratory_sounds', 'Singing',
                    'Chewing_and_mastication', 'Breathing', 'Gasp', 'Sigh', 'Run', 'Computer_keyboard,Typing',
                    'Domestic_sounds_and_home_sounds')
'''(Speech_synthesizer, Whispering,Human_voice, etc) should not be included in the dataset. so we look at the audioset
Ontology to find relative data, from parent to child search direction'''

f = open('ontology.json')
ontology = json.load(f)

Parent_list0 = ['Human sounds', 'Animal', 'Music', 'Sounds of things']
Desired_dic = {}

for P in ontology:
    if P['name'] in Parent_list0:
        Desired_dic[P['name']] = {}  # dict(P['child_ids'])
        for P2 in ontology:
            if P2['id'] in P['child_ids']:  # Desired_dic[P['name']]:
                print(P2['name'])
                inp = input(f"If {P['name']}/{P2['name']} this class is relevant, enter 1, otherwise enter anything "
                            f"else\n")
                if inp == '1':
                    if not P2['child_ids']:
                        Desired_dic[P['name']][P2['name']] = {'level': 'Finished level2'}
                    else:
                        Desired_dic[P['name']][P2['name']] = {'level': 'Finished level2'}
                        for P3 in ontology:
                            if P3['id'] in P2['child_ids']:
                                # Desired_dic[P['name']][P2['id']] = {}
                                print(P3['name'])
                                inp2 = input(
                                    f"If {P['name']}/{P2['name']}/{P3['name']} this class is relevant, enter 1, otherwise enter anything"
                                    f" else\n")
                                if inp2 == '1':
                                    if not P3['child_ids']:
                                        Desired_dic[P['name']][P2['name']][P3['name']] = {'level': 'Finished level3'}
                                    else:
                                        Desired_dic[P['name']][P2['name']][P3['name']] = {'level': 'Finished level3'}
                                        for P4 in ontology:
                                            if P4['id'] in P3['child_ids']:
                                                # Desired_dic[P['name']][P2['id']] = {}
                                                print(P4['name'])
                                                inp3 = input(
                                                    f"If {P['name']}/{P2['name']}/{P3['name']}/{P4['name']} this class is relevant, enter 1, otherwise enter anything else\n")
                                                if inp3 == '1':
                                                    if not P4['child_ids']:
                                                        Desired_dic[P['name']][P2['name']][P3['name']][
                                                            P4['name']] = {'level': 'Finished level4'}
                                                    else:
                                                        Desired_dic[P['name']][P2['name']][P3['name']][P4['name']] = {
                                                            'level': 'Finished level4'}
                                                        for P5 in ontology:
                                                            if P5['id'] in P4['child_ids']:
                                                                # Desired_dic[P['name']][P2['id']] = {}
                                                                print(P5['name'])
                                                                inp4 = input(
                                                                    f"If {P['name']}/{P2['name']}/{P3['name']}/{P4['name']}/{P5['name']} this class is relevant, enter 1, otherwise enter anything else\n")
                                                                if inp4 == '1':
                                                                    if not P5['child_ids']:
                                                                        Desired_dic[P['name']][P2['name']][P3['name']][
                                                                            P4['name']][
                                                                            P5['name']] = {'level': 'Finished level5'}
                                                                    else:
                                                                        Desired_dic[P['name']][P2['name']][P3['name']][
                                                                            P4['name']][
                                                                            P5['name']] = {'level': 'Finished level5'}
                                                                        for P6 in ontology:
                                                                            if P6['id'] in P5['child_ids']:
                                                                                # Desired_dic[P['name']][P2['id']] = {}
                                                                                print(P6['name'])
                                                                                inp5 = input(
                                                                                    f"If {P['name']}/{P2['name']}/{P3['name']}/{P4['name']}/{P5['name']}/{P6['name']} this class is relevant, enter 1, otherwise enter anything else\n")
                                                                                if inp5 == '1':
                                                                                    if not P6['child_ids']:
                                                                                        Desired_dic[P['name']][
                                                                                            P2['name']][P3['name']][
                                                                                            P4['name']][P5['name']][P6[
                                                                                            'name']] = {
                                                                                            'level': 'Finished level6'}
                                                                                    else:
                                                                                        print('tree is too long')
                                                                                elif inp5 == '2':
                                                                                    Desired_dic[P['name']][
                                                                                        P2['name']][P3['name']][
                                                                                        P4['name']][P5['name']][P6[
                                                                                        'name']] = {
                                                                                        'level': 'Finished level6_2'}

                                                                                # else:
                                                                                #     Desired_dic[P['name']][
                                                                                #         P2['name']][P3['name']][
                                                                                #         P4['name']]['Finished level5'] = 'Finished level5'

                                                                elif inp4 == '2':
                                                                    Desired_dic[P['name']][
                                                                        P2['name']][P3['name']][
                                                                        P4['name']][P5['name']] = {
                                                                        'level': 'Finished level5_2'}
                                                                # else:
                                                                #     Desired_dic[P['name']][
                                                                #         P2['name']][P3['name']]['Finished level4'] = 'Finished level4'

                                                elif inp3 == '2':
                                                    Desired_dic[P['name']][
                                                        P2['name']][P3['name']][
                                                        P4['name']] = {'level': 'Finished level4_2'}
                                                # else:
                                                #     Desired_dic[P['name']][
                                                #         P2['name']]['Finished level3'] = 'Finished level3'

                                elif inp2 == '2':
                                    Desired_dic[P['name']][
                                        P2['name']][P3['name']] = {'level': 'Finished level3_2'}
                                # else:
                                #     Desired_dic[P['name']][
                                #         'Finished level2'] = 'Finished level2'

                elif inp == '2':
                    Desired_dic[P['name']][
                        P2['name']] = {'level': 'Finished level2_2'}

db_label_dir = os.path.join(db_dir, 'FSD50K.ground_truth')

dev_df = pandas.read_csv(os.path.join(db_label_dir, 'dev.csv'))

print('ontology printed')
# def examp(sam):
#     return True
# [examp(i) for i in dev_df.values]
for sample in dev_df.values:
    fname = str(sample[0]) + '.wav'
    flabel = sample[1]
    fmids = sample[2]
    fsplit = sample[3]
    flabels = flabel.split(',')
    if flabels[-1] in Desired_dic.keys():
        print(flabels[-1])
        if not Desired_dic[flabels[-1]] == {}:
            print('hi')
            if flabels[-2] in Desired_dic[flabels[-1]].keys():
                print('hello level 2')


dev_df.columns[1]
dev_df.values[0]
