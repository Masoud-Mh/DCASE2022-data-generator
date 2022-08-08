# import db_config
import os
import json
import shutil
import pandas
import pandas as pd


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


'''
In the First step we should read the dataset files
and put each file in its corresponding folder class
Hence we need to classify the files based on their ground truth label'''

db_name = 'Sub_FSDK50K'
db_dir = 'E:\SELD_2022\FSDK50K'
out_dir = 'E:\SELD_2022\classified_FSD50K'
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
                                                if not sub_id_flag:
                                                    Desired_dic[P4['name']] = P4['id']
                                                    sub_id_flag = True
                                            elif inp4 == '2':
                                                Desired_dic[P4['name']] = sub_id(P4, ontology)
                                                sub_id_flag = True
                                    if not sub_id_flag:
                                        Desired_dic[P3['name']] = [P3['id']]
                                        sub_id_flag = True
                                elif inp3 == '2':
                                    Desired_dic[P3['name']] = sub_id(P3, ontology)
                                    sub_id_flag = True
                        if not sub_id_flag:
                            Desired_dic[P2['name']] = [P2['id']]
                            sub_id_flag = True
                    elif inp2 == '2':
                        Desired_dic[P2['name']] = sub_id(P2, ontology)
                        sub_id_flag = True

# for P in ontology:
#     if P['name'] in Parent_list0:
#         Desired_dic[P['name']] = {}  # dict(P['child_ids'])
#         for P2 in ontology:
#             if P2['id'] in P['child_ids']:  # Desired_dic[P['name']]:
#                 print(P2['name'])
#                 inp = input(f"If {P['name']}/{P2['name']} this class is relevant, enter 1, otherwise enter anything "
#                             f"else\n")
#                 if inp == '1':
#                     if not P2['child_ids']:
#                         Desired_dic[P['name']][P2['name']] = {'level': 'Finished level2'}
#                     else:
#                         Desired_dic[P['name']][P2['name']] = {'level': 'Finished level2'}
#                         for P3 in ontology:
#                             if P3['id'] in P2['child_ids']:
#                                 # Desired_dic[P['name']][P2['id']] = {}
#                                 print(P3['name'])
#                                 inp2 = input(
#                                     f"If {P['name']}/{P2['name']}/{P3['name']} this class is relevant, enter 1, otherwise enter anything"
#                                     f" else\n")
#                                 if inp2 == '1':
#                                     if not P3['child_ids']:
#                                         Desired_dic[P['name']][P2['name']][P3['name']] = {'level': 'Finished level3'}
#                                     else:
#                                         Desired_dic[P['name']][P2['name']][P3['name']] = {'level': 'Finished level3'}
#                                         for P4 in ontology:
#                                             if P4['id'] in P3['child_ids']:
#                                                 # Desired_dic[P['name']][P2['id']] = {}
#                                                 print(P4['name'])
#                                                 inp3 = input(
#                                                     f"If {P['name']}/{P2['name']}/{P3['name']}/{P4['name']} this class is relevant, enter 1, otherwise enter anything else\n")
#                                                 if inp3 == '1':
#                                                     if not P4['child_ids']:
#                                                         Desired_dic[P['name']][P2['name']][P3['name']][
#                                                             P4['name']] = {'level': 'Finished level4'}
#                                                     else:
#                                                         Desired_dic[P['name']][P2['name']][P3['name']][P4['name']] = {
#                                                             'level': 'Finished level4'}
#                                                         for P5 in ontology:
#                                                             if P5['id'] in P4['child_ids']:
#                                                                 # Desired_dic[P['name']][P2['id']] = {}
#                                                                 print(P5['name'])
#                                                                 inp4 = input(
#                                                                     f"If {P['name']}/{P2['name']}/{P3['name']}/{P4['name']}/{P5['name']} this class is relevant, enter 1, otherwise enter anything else\n")
#                                                                 if inp4 == '1':
#                                                                     if not P5['child_ids']:
#                                                                         Desired_dic[P['name']][P2['name']][P3['name']][
#                                                                             P4['name']][
#                                                                             P5['name']] = {'level': 'Finished level5'}
#                                                                     else:
#                                                                         Desired_dic[P['name']][P2['name']][P3['name']][
#                                                                             P4['name']][
#                                                                             P5['name']] = {'level': 'Finished level5'}
#                                                                         for P6 in ontology:
#                                                                             if P6['id'] in P5['child_ids']:
#                                                                                 # Desired_dic[P['name']][P2['id']] = {}
#                                                                                 print(P6['name'])
#                                                                                 inp5 = input(
#                                                                                     f"If {P['name']}/{P2['name']}/{P3['name']}/{P4['name']}/{P5['name']}/{P6['name']} this class is relevant, enter 1, otherwise enter anything else\n")
#                                                                                 if inp5 == '1':
#                                                                                     if not P6['child_ids']:
#                                                                                         Desired_dic[P['name']][
#                                                                                             P2['name']][P3['name']][
#                                                                                             P4['name']][P5['name']][P6[
#                                                                                             'name']] = {
#                                                                                             'level': 'Finished level6'}
#                                                                                     else:
#                                                                                         print('tree is too long')
#                                                                                 elif inp5 == '2':
#                                                                                     Desired_dic[P['name']][
#                                                                                         P2['name']][P3['name']][
#                                                                                         P4['name']][P5['name']][P6[
#                                                                                         'name']] = {
#                                                                                         'level': 'Finished level6_2'}
#
#                                                                                 # else:
#                                                                                 #     Desired_dic[P['name']][
#                                                                                 #         P2['name']][P3['name']][
#                                                                                 #         P4['name']]['Finished level5'] = 'Finished level5'
#
#                                                                 elif inp4 == '2':
#                                                                     Desired_dic[P['name']][
#                                                                         P2['name']][P3['name']][
#                                                                         P4['name']][P5['name']] = {
#                                                                         'level': 'Finished level5_2'}
#                                                                 # else:
#                                                                 #     Desired_dic[P['name']][
#                                                                 #         P2['name']][P3['name']]['Finished level4'] = 'Finished level4'
#
#                                                 elif inp3 == '2':
#                                                     Desired_dic[P['name']][
#                                                         P2['name']][P3['name']][
#                                                         P4['name']] = {'level': 'Finished level4_2'}
#                                                 # else:
#                                                 #     Desired_dic[P['name']][
#                                                 #         P2['name']]['Finished level3'] = 'Finished level3'
#
#                                 elif inp2 == '2':
#                                     Desired_dic[P['name']][
#                                         P2['name']][P3['name']] = {'level': 'Finished level3_2'}
#                                 # else:
#                                 #     Desired_dic[P['name']][
#                                 #         'Finished level2'] = 'Finished level2'
#
#                 elif inp == '2':
#                     Desired_dic[P['name']][
#                         P2['name']] = {'level': 'Finished level2_2'}

db_label_dir = os.path.join(db_dir, 'FSD50K.ground_truth')

dev_df = pandas.read_csv(os.path.join(db_label_dir, 'dev.csv'))

print('ontology printed')
# def examp(sam):
#     return True
# [examp(i) for i in dev_df.values]
number_of_sample=0
mixed_files = 0

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
        for classes in Desired_dic.keys():
            if fmid in Desired_dic[classes]:
                if tempclass is None:
                    tempclass=classes
                else:
                    if tempclass != classes:
                        print('mixed file')
                        mixed_flag = True
    if tempclass != None:
        if mixed_flag:
            mixed_files += 1
        else:
            number_of_sample += 1





dev_df.columns[1]
dev_df.values[0]

# Parent_list0 = ['Human sounds', 'Animal', 'Music', 'Sounds of things']
# Desired_dic = {}
#
# for P in ontology:
#     if P['name'] in Parent_list0:
#         Desired_dic[P['name']] = {}  # dict(P['child_ids'])
#         for P2 in ontology:
#             if P2['id'] in P['child_ids']:  # Desired_dic[P['name']]:
#                 print(P2['name'])
#                 inp = input(f"If {P['name']}/{P2['name']} this class is relevant, enter 1, otherwise enter anything "
#                             f"else\n")
#                 if inp == '1':
#                     if not P2['child_ids']:
#                         Desired_dic[P['name']][P2['name']] = {'level': 'Finished level2'}
#                     else:
#                         Desired_dic[P['name']][P2['name']] = {'level': 'Finished level2'}
#                         for P3 in ontology:
#                             if P3['id'] in P2['child_ids']:
#                                 # Desired_dic[P['name']][P2['id']] = {}
#                                 print(P3['name'])
#                                 inp2 = input(
#                                     f"If {P['name']}/{P2['name']}/{P3['name']} this class is relevant, enter 1, otherwise enter anything"
#                                     f" else\n")
#                                 if inp2 == '1':
#                                     if not P3['child_ids']:
#                                         Desired_dic[P['name']][P2['name']][P3['name']] = {'level': 'Finished level3'}
#                                     else:
#                                         Desired_dic[P['name']][P2['name']][P3['name']] = {'level': 'Finished level3'}
#                                         for P4 in ontology:
#                                             if P4['id'] in P3['child_ids']:
#                                                 # Desired_dic[P['name']][P2['id']] = {}
#                                                 print(P4['name'])
#                                                 inp3 = input(
#                                                     f"If {P['name']}/{P2['name']}/{P3['name']}/{P4['name']} this class is relevant, enter 1, otherwise enter anything else\n")
#                                                 if inp3 == '1':
#                                                     if not P4['child_ids']:
#                                                         Desired_dic[P['name']][P2['name']][P3['name']][
#                                                             P4['name']] = {'level': 'Finished level4'}
#                                                     else:
#                                                         Desired_dic[P['name']][P2['name']][P3['name']][P4['name']] = {
#                                                             'level': 'Finished level4'}
#                                                         for P5 in ontology:
#                                                             if P5['id'] in P4['child_ids']:
#                                                                 # Desired_dic[P['name']][P2['id']] = {}
#                                                                 print(P5['name'])
#                                                                 inp4 = input(
#                                                                     f"If {P['name']}/{P2['name']}/{P3['name']}/{P4['name']}/{P5['name']} this class is relevant, enter 1, otherwise enter anything else\n")
#                                                                 if inp4 == '1':
#                                                                     if not P5['child_ids']:
#                                                                         Desired_dic[P['name']][P2['name']][P3['name']][
#                                                                             P4['name']][
#                                                                             P5['name']] = {'level': 'Finished level5'}
#                                                                     else:
#                                                                         Desired_dic[P['name']][P2['name']][P3['name']][
#                                                                             P4['name']][
#                                                                             P5['name']] = {'level': 'Finished level5'}
#                                                                         for P6 in ontology:
#                                                                             if P6['id'] in P5['child_ids']:
#                                                                                 # Desired_dic[P['name']][P2['id']] = {}
#                                                                                 print(P6['name'])
#                                                                                 inp5 = input(
#                                                                                     f"If {P['name']}/{P2['name']}/{P3['name']}/{P4['name']}/{P5['name']}/{P6['name']} this class is relevant, enter 1, otherwise enter anything else\n")
#                                                                                 if inp5 == '1':
#                                                                                     if not P6['child_ids']:
#                                                                                         Desired_dic[P['name']][
#                                                                                             P2['name']][P3['name']][
#                                                                                             P4['name']][P5['name']][P6[
#                                                                                             'name']] = {
#                                                                                             'level': 'Finished level6'}
#                                                                                     else:
#                                                                                         print('tree is too long')
#                                                                                 elif inp5 == '2':
#                                                                                     Desired_dic[P['name']][
#                                                                                         P2['name']][P3['name']][
#                                                                                         P4['name']][P5['name']][P6[
#                                                                                         'name']] = {
#                                                                                         'level': 'Finished level6_2'}
#
#                                                                                 # else:
#                                                                                 #     Desired_dic[P['name']][
#                                                                                 #         P2['name']][P3['name']][
#                                                                                 #         P4['name']]['Finished level5'] = 'Finished level5'
#
#                                                                 elif inp4 == '2':
#                                                                     Desired_dic[P['name']][
#                                                                         P2['name']][P3['name']][
#                                                                         P4['name']][P5['name']] = {
#                                                                         'level': 'Finished level5_2'}
#                                                                 # else:
#                                                                 #     Desired_dic[P['name']][
#                                                                 #         P2['name']][P3['name']]['Finished level4'] = 'Finished level4'
#
#                                                 elif inp3 == '2':
#                                                     Desired_dic[P['name']][
#                                                         P2['name']][P3['name']][
#                                                         P4['name']] = {'level': 'Finished level4_2'}
#                                                 # else:
#                                                 #     Desired_dic[P['name']][
#                                                 #         P2['name']]['Finished level3'] = 'Finished level3'
#
#                                 elif inp2 == '2':
#                                     Desired_dic[P['name']][
#                                         P2['name']][P3['name']] = {'level': 'Finished level3_2'}
#                                 # else:
#                                 #     Desired_dic[P['name']][
#                                 #         'Finished level2'] = 'Finished level2'
#
#                 elif inp == '2':
#                     Desired_dic[P['name']][
#                         P2['name']] = {'level': 'Finished level2_2'}




# for sample in dev_df.values:
#     fname = str(sample[0]) + '.wav'
#     flabel = sample[1]
#     fmids = sample[2].split(',')
#     fsplit = sample[3]
#     flabel = flabel.replace("_", " ")
#     flabels = flabel.split(',')
#     if flabels[-1] in Desired_dic.keys():
#         print(flabels[-1])
#         if not Desired_dic[flabels[-1]] == {}:
#             print('hi')
#             if flabels[-2] in Desired_dic[flabels[-1]].keys():
#                 print('hello level 2')
#                 if Desired_dic[flabels[-1]][flabels[-2]].keys():
#                     print('hello level 3')
#                     if len(Desired_dic[flabels[-1]][flabels[-2]].keys()) > 1:
#                         print('Have to go one level further')
#                         if flabels[-3] in Desired_dic[flabels[-1]][flabels[-2]].keys():
#                             print('hello level 4')
#                             if len(Desired_dic[flabels[-1]][flabels[-2]][flabels[-3]].keys()) > 1:
#                                 print('Have to go one level further')
#                                 if flabels[-4] in Desired_dic[flabels[-1]][flabels[-2]][flabels[-3]].keys():
#                                     print('hello level 5')
#                                     if len(Desired_dic[flabels[-1]][flabels[-2]][flabels[-3]][flabels[-4]].keys()) > 1:
#                                         print('Have to go one level further')
#                                         if flabels[-5] in Desired_dic[flabels[-1]][flabels[-2]][flabels[-3]][
#                                             flabels[-4]].keys():
#                                             print('hello level 6')
#                                             if len(Desired_dic[flabels[-1]][flabels[-2]][flabels[-3]][
#                                                        flabels[-4]][flabels[-5]].keys()) > 1:
#                                                 print('Have to go one level further, but wont')
#                                             else:
#                                                 level6_dir = os.path.join(out_dir, flabels[-5])
#                                                 copy_file(level6_dir,
#                                                           source=os.path.join(db_dir, 'FSD50K.dev_audio', fname),
#                                                           destination=os.path.join(level6_dir, fname), filename=fname)
#                                     else:
#                                         level5_dir = os.path.join(out_dir, flabels[-4])
#                                         copy_file(level5_dir, source=os.path.join(db_dir, 'FSD50K.dev_audio', fname),
#                                                   destination=os.path.join(level5_dir, fname), filename=fname)
#                             else:
#                                 level4_dir = os.path.join(out_dir, flabels[-3])
#                                 copy_file(level4_dir, source=os.path.join(db_dir, 'FSD50K.dev_audio', fname),
#                                           destination=os.path.join(level4_dir, fname), filename=fname)
#                     else:
#                         level3_dir = os.path.join(out_dir, flabels[-2])
#                         copy_file(level3_dir, source=os.path.join(db_dir, 'FSD50K.dev_audio', fname),
#                                   destination=os.path.join(level3_dir, fname), filename=fname)