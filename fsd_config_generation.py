import db_config
import os
import json

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
print('ontology printed')

