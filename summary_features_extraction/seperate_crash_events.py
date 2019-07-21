# Seprate sentennces and paragraph into Precrash Event, Impact and Pos Crah Event.
# Iterate the sentences get the sentences based on feature vector.


# Things to do
# Put all lines in pre crash until crash event is detected. , extract road geometry, direction.
# On crash. 1) Extract the location of impact, point of impact:  Enable post crash event.
# https://medium.com/factory-mind/regex-tutorial-a-simple-cheatsheet-by-examples-649dc1c3f285
# In post crash event, detect rotation (spinning, clockwise, counter-clockwise) and direction., distance



import glob
import json
import os
import nltk
from nltk.tokenize import RegexpTokenizer
import nltk.tokenize as tokenize
from stanfordcorenlp import StanfordCoreNLP
import json
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import csv

import sys
sys.stdout = open('output.txt','w')

nlp = StanfordCoreNLP(r'F:\Softwares\stanford-corenlp-full-2018-10-05')

pre_crash_counter = 0
crash_counter = 0
pro_crash_counter = 0
pos_crash_dict = {}


def create_csv_file():
    csv_columns = ['case_id','number_of_vehicles', 'striker_damage_area', 'victim_damage_area','striker_rotation', 'victim_rotation', 'striker_degrees', 'vicitm_degrees', 'striker_facing', 'victim_facing', 'striker_destination_lane', 'victim_destination_lane']
    csv_file = "pos_crash_event.csv"
    try:
        with open(csv_file, 'w', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=',', lineterminator='\n')
            writer.writeheader()
    except IOError:
        print("I/O error")


def preprocessing(summary):
    # use regex to replace variables (V1, vehicleone, vehicle one, vehicle#1, vehicle #1, vehicle # 1)
    # use regex to replace variables (V2, vehicletwo, vehicle two, vehicle#2, vehicle #2, vehicle # 2)
    v1_list = ['v1', 'vehicleone', 'vehicle one', 'vehicle 1', 'Vehicle 1', 'vehicle#1', 'vehicle #1', 'vehicle # 1','Vehicle one','Vehicle#1','Vehicle #1', 'Vehicle # 1','one-vehcile']
    v2_list = ['v2', 'vehicletwo', 'vehicle two', 'vehicle 2', 'Vehicle 2', 'vehicle#2', 'vehicle #2', 'vehicle # 2', 'Vehicle two','Vehicle#2','Vehicle #2', 'Vehicle # 2', 'two-vehicle']
    v3_list = ['v3', 'vehiclethree', 'vehicle three', 'vehicle 3', 'Vehicle 3', 'vehicle#3', 'vehicle #3', 'vehicle # 3','Vehicle three', 'Vehicle#3', 'Vehicle #3', 'Vehicle # 3', 'three-vehcile']
    v4_list = ['v4', 'vehiclefour', 'vehicle four', 'vehicle 4', 'Vehicle 4', 'vehicle#4', 'vehicle #4', 'vehicle # 4','Vehicle four', 'Vehicle#4', 'Vehicle #4', 'Vehicle # 4', 'four-vehicle']
    for word in v1_list:
        summary = summary.replace(word, "V1")

    for word in v2_list:
        summary = summary.replace(word, "V2")

    for word in v3_list:
        summary = summary.replace(word, "V3")

    for word in v4_list:
        summary = summary.replace(word, "V4")

    summary = summary.replace(r"\r", '')
    summary = summary.replace(r"\t", '')
    summary = summary.replace(r"\r", '')
    summary = summary.replace(r"\n", ' ')

    return summary



def clockwise_counter_clockwise_rotation(crash_event_sentences):

    pos_crash_dict['striker_rotation'] = 'default'
    pos_crash_dict['victim_rotation'] = 'default'

    for impact_sentence in crash_event_sentences:
        rotated_list = ['rotated', 'clockwise', 'counterclockwise', 'spin','spun',]  # Create Google Word 2 Vector list to increase accuracy
        if any(word in impact_sentence for word in rotated_list):
            print(impact_sentence)
            # openie does not give good result for rotation.
            # Use regex pattern to extract it.
            clockwise_list = ['clockwise', 'counterclockwise']  # Create Google Word 2 Vector list to increase accuracy
            for word in clockwise_list:
                if word in impact_sentence:
                    verb = word
                    pattern = r'.+?(?=' + verb + ')'
                    pre_verb = re.search(pattern, impact_sentence)
                    print(pre_verb[0])
                    # check counter, rotated (dictionary), and vehicle, slightly
                    stop_words = set(stopwords.words('english'))
                    word_tokens = word_tokenize(pre_verb[0])
                    filtered_sentence = [w for w in word_tokens if not w in stop_words]
                    bClockwise = False
                    bClockwiseV1 = False
                    bClockwiseV2 = False
                    bCounterClockwise = False
                    for item in reversed(filtered_sentence):
                        if item.lower() == 'counter':
                            bCounterClockwise = True

                        if item == 'V1':
                            bClockwise = True
                            bClockwiseV1 = True
                        elif item == 'V2':
                            bClockwise = True
                            bClockwiseV2 = True

                        if bClockwise and bClockwiseV1 and bCounterClockwise:
                            print('V1 Counter Clockwise')
                            pos_crash_dict['striker_rotation'] = 'counterclockwise'
                            break

                        if bClockwise and bClockwiseV1:
                            print('V1 Clockwise')
                            pos_crash_dict['striker_rotation'] = 'clockwise'
                            break

                        if bClockwise and bClockwiseV2 and bCounterClockwise:
                            print('V2 Counter Clockwise')
                            pos_crash_dict['victim_rotation'] = 'counterclockwise'
                            break
                        if bClockwise and bClockwiseV2:
                            print('V2 Clockwise')
                            pos_crash_dict['victim_rotation'] = 'clockwise'
                            break

                    pattern = r'(?<=' + verb + ').*'
                    pos_verb = re.search(pattern, impact_sentence)
                    print(pos_verb[0].strip())


        if "degrees right" in impact_sentence:
            word = "degrees right"
            pattern = r'.+?(?=' + word + ')'
            pre_right = re.search(pattern, impact_sentence)
            print(pre_right[0]+ "loop")
            # check counter, rotated (dictionary), and vehicle, slightly
            stop_words = set(stopwords.words('english'))
            word_tokens = word_tokenize(pre_right[0])
            filtered_sentence = [w for w in word_tokens if not w in stop_words]

            for item in reversed(filtered_sentence):
                if item == 'V1':
                    print("V1 degrees right")
                    break

                if item == 'V2':
                    print("V2 degrees right")
                    break




        if "degrees left" in impact_sentence:
            word = "degrees left"
            pattern = r'.+?(?=' + word + ')'
            pre_left = re.search(pattern, impact_sentence)
            print(pre_left[0])
            # check counter, rotated (dictionary), and vehicle, slightly
            stop_words = set(stopwords.words('english'))
            word_tokens = word_tokenize(pre_right[0])
            filtered_sentence = [w for w in word_tokens if not w in stop_words]

            for item in reversed(filtered_sentence):
                if item == 'V1':
                    print("V1 degrees left")
                    break

                if item == 'V2':
                    print("V2 degrees left")
                    break


def degrees_rotation(crash_event_sentences):

    pos_crash_dict['striker_degrees'] = 'default'
    pos_crash_dict['victim_degrees'] = 'default'

    for impact_sentence in crash_event_sentences:
        derees_list = ['degrees']  # Create Google Word 2 Vector list to increase accuracy
        if any(word in impact_sentence for word in derees_list):
            print(impact_sentence)
            # openie does not give good result for rotation.
            # Use regex pattern to extract it.
            for word in derees_list:
                if word in impact_sentence:
                    pattern = r'.+?(?=' + word + ')'
                    pre_degree = re.search(pattern, impact_sentence)
                    print(pre_degree[0])
                    # check counter, rotated (dictionary), and vehicle, slightly
                    stop_words = set(stopwords.words('english'))
                    word_tokens = word_tokenize(pre_degree[0])
                    filtered_sentence = [w for w in word_tokens if not w in stop_words]
                    bDegreesV1 = False
                    bDegreesV2 = False
                    bVehicle = False
                    degree_value = 0
                    for item in reversed(filtered_sentence):

                        if item.isdigit():
                            degree_value = item

                        if item == 'V1':
                            bDegreesV1 = True
                            bVehicle = True

                        if item == 'V2':
                            bDegreesV2 = True
                            bVehicle = True

                        if bVehicle and degree_value != 0:

                            if bDegreesV1:
                                print("V1 degree "+degree_value)
                                pos_crash_dict['striker_degrees'] = degree_value
                                break

                            if bDegreesV2:
                                print("V2 degree "+degree_value)
                                pos_crash_dict['victim_degrees'] = degree_value
                                break

                    if bVehicle and degree_value == 0:
                        pattern = r'(?<=' + word + ').*'
                        pos_degree = re.search(pattern, impact_sentence)
                        print(pos_degree[0].strip())

                        stop_words = set(stopwords.words('english'))
                        word_tokens = word_tokenize(pre_degree[0])
                        filtered_sentence = [w for w in word_tokens if not w in stop_words]

                        for item in reversed(filtered_sentence):

                            if item.isdigit():
                                degree_value = item

                            if bVehicle and degree_value != 0:

                                if bDegreesV1:
                                    print("V1 degree " + degree_value)
                                    pos_crash_dict['striker_degrees'] = degree_value
                                    break

                                if bDegreesV2:
                                    print("V2 degree " + degree_value)
                                    pos_crash_dict['victim_degrees'] = degree_value
                                    break

                    if degree_value == 0:
                        print("No degree found")


def facing_direction(crash_event_sentences):

    pos_crash_dict['striker_facing'] = 'initialdirection'
    pos_crash_dict['victim_facing'] = 'initialdirection'

    direction_string = "rest, face, facing, rightmost ,northbound ,southbound ,eastbound ,ONE  CLOSED OVER,righthand ,northbound,northbound ,bound carriageway,westbound,crosswalk,stoplight,eastbound,railroad crossing,northbound ,offramp,westbound,opposite direction,directions,opposite directions,toward,downward,backwards,directon,south,east,west,northeast,southeast,southwest,northwest,northern,eastern,northeast,west,north,south,southeast,northeast,southwest,northwest,eastern,southward,eastward,north,east,west,southeast,northeast,southwest,northwest,southern,eastern,northern,east,north,south,southwest,southeast,northeast,northwest,eastern,western,southwesterly direction,southbound,westbound,eastbound,southbound ,westbound ,northbound ,eastbound ,northbound ,southbound ,eastbound"
    direction_list = direction_string.split(",")
    for impact_sentence in crash_event_sentences:
        if any(word in impact_sentence for word in direction_list):
            print(impact_sentence)
            face_list = ['face', 'facing']  # Create Google Word 2 Vector list to increase accuracy
            for word in face_list:
                if word in impact_sentence:

                    bFaceV1 = False
                    bFaceV2 = False
                    bFaceV1V2 = False

                    pattern = r'.+?(?=' + word + ')'
                    pre_face = re.search(pattern, impact_sentence)
                    print(pre_face[0])
                    # check counter, rotated (dictionary), and vehicle, slightly
                    stop_words = set(stopwords.words('english'))
                    word_tokens = word_tokenize(pre_face[0])
                    filtered_sentence = [w for w in word_tokens if not w in stop_words]

                    for item in reversed(filtered_sentence):

                        if item == 'V1':
                            bFaceV1 = True
                            break


                        if item == 'V2':
                            bFaceV2 = True
                            break

                        if item.lower() == 'vehicles' or item.lower() == 'both':
                            bFaceV1V2 = True
                            break

                    face = word
                    pattern = r'(?<=' + face + ').*'
                    pos_face = re.search(pattern, impact_sentence)
                    print(pos_face[0].strip())

                    stop_words = set(stopwords.words('english'))
                    word_tokens = word_tokenize(pos_face[0])
                    filtered_sentence = [w for w in word_tokens if not w in stop_words]

                    for item in (filtered_sentence):
                        if __name__ == '__main__':
                            if(item.startswith('north') or item.startswith('east') or item.startswith('south') or item.startswith('west')):
                                print(item)
                                if bFaceV1:
                                    print("faceCounter")
                                    pos_crash_dict['striker_facing'] = item

                                if bFaceV2:
                                    print("faceCounter")
                                    pos_crash_dict['victim_facing'] = item

                                if bFaceV1V2:
                                    print("faceCounter")
                                    pos_crash_dict['striker_facing'] = item
                                    pos_crash_dict['victim_facing'] = item

                                break



        # defauolt direction
        # Study the default direction cases. if direction does not exiit. it will be considired as original direction
        # The original direction scenario will be determined after the finding the destination lane. (Off road, on road, original lane)


def destination_lane(crash_event_sentences):

    pos_crash_dict['striker_destination_lane'] = 'default'
    pos_crash_dict['victim_destination_lane'] = 'default'

    direction_string = "stop, rest, face, facing, rightmost ,northbound ,southbound ,eastbound ,one closed over,righthand ,northbound,northbound ,bound carriageway,westbound,crosswalk,stoplight,eastbound,railroad crossing,northbound ,offramp,westbound,opposite direction,directions,opposite directions,toward,downward,backwards,directon,south,east,west,northeast,southeast,southwest,northwest,northern,eastern,northeast,west,north,south,southeast,northeast,southwest,northwest,eastern,southward,eastward,north,east,west,southeast,northeast,southwest,northwest,southern,eastern,northern,east,north,south,southwest,southeast,northeast,northwest,eastern,western,southwesterly direction,southbound,westbound,eastbound,southbound ,westbound ,northbound ,eastbound ,northbound ,southbound ,eastbound"
    direction_list = direction_string.split(",")
    for impact_sentence in crash_event_sentences:
        if any(word in impact_sentence for word in direction_list):
            print(impact_sentence)

            # cover rest cases first
            stop_list = ['stop', 'rest']
            if any(word in impact_sentence for word in stop_list):
                print(impact_sentence)
                # NO sentence after rest =  rotate ccw and came to rest.
                # default case
                for word in stop_list:
                    if word in impact_sentence:
                        bNotFound = True
                        # pos rest
                        print('p1-----------')
                        pattern = r'(?<=' + word + ').*'
                        pos_verb = re.search(pattern, impact_sentence)

                        if pos_verb[0] == '' or pos_verb[0] == '.':
                            bNotFound = False
                            print('Initial direction|on road|INSIDE')
                            pos_crash_dict['striker_destination_lane'] = 'innerzone'
                            pos_crash_dict['victim_destination_lane'] = 'innerzone'
                            break

                        print('-----------')
                        print('p2-----------')
                        road_list = ['roadway', 'lane', 'intersection', 'median', 'shoulder', 'road', 'exit']
                        # detect on the roadway, off the roadway
                        if any(word in pos_verb[0] for word in road_list):
                            print(pos_verb[0])

                            if 'roadway' in pos_verb[0] or 'road' in pos_verb[0]:
                                print('roadway-----')
                                road = 'road'
                                pattern = r'.+?(?=' + road + ')'
                                pre_road = re.search(pattern, impact_sentence)
                                print(pre_road[0])

                                off_road_list = ['off', 'outside', 'mail', 'sign','tree', 'pole', 'shoulder', 'park']

                                bRoad = True

                                if any(word in pre_road[0] for word in off_road_list):
                                    print('OUTSIDE')
                                    bRoad = False
                                    bNotFound = False
                                else:
                                    print('INSIDE')
                                    bRoad = False
                                    bNotFound = False

                                if bRoad:
                                    print('INSIDE')


                            if 'shoulder' in pos_verb[0] or 'median' in pos_verb[0]:
                                print('OUTSIDE')

                            if 'lane' in pos_verb[0] or 'intersection' in pos_verb[0]:
                                off_road_list = ['off', 'outside', 'mail', 'sign', 'tree', 'pole', 'shoulder', 'park']

                                if any(word in pos_verb[0] for word in off_road_list):
                                    print('OUTSIDE')
                                else:
                                    print('INSIDE')

                        if bNotFound:
                            print('INSIDE')

                        print('-----------')
                        # pre rest





def pre_crash_event(caseId):
    print(caseId)
    # service call to ac3r

def crash_event(summary):
    global crash_counter
    crash_event_sentences = []
    sentenceTokens = tokenize.sent_tokenize(summary)
    crash_event_detected = True
    pos_crash_event = False
    # Score Evaluation parameters
    # clockwise, counterclockwise, spin  --> done
    # Direction (north, south, east, west)  --> done
    # Distance  (Lane where it comes to rest) @off road, on roads
    # Crash Event --> XML --> done
    for line in sentenceTokens:
        line = line.strip()  #\r\n , remove these from lines.

        if pos_crash_event:
            pre_crash_word_list = ['precrash', 'Precrash','Pre-Crash', 'PreCrash']
            if any(word in line for word in pre_crash_word_list):
                #print('precrash')
                #print(line)
                pos_crash_event = False

        if crash_event_detected:
            list_ = ['impact','struck', 'hit', 'contacted','impacted'] # Create Google Word 2 Vector list to increase accuracy
            if any(word in line for word in list_):
                print(line)
                crash_event_sentences.append(line)
                crash_counter = crash_counter + 1
                crash_event_detected = False
                pos_crash_event = True

        if pos_crash_event:
            #print(line)
            crash_event_sentences.append(line)

    clockwise_counter_clockwise_rotation(crash_event_sentences)
    degrees_rotation(crash_event_sentences)
    facing_direction(crash_event_sentences)
    destination_lane(crash_event_sentences)



def saveDictionaryToCsvFile():

    csv_columns = ['case_id', 'number_of_vehicles', 'striker_damage_area', 'victim_damage_area', 'striker_rotation',
                   'victim_rotation', 'striker_degrees', 'victim_degrees', 'striker_facing', 'victim_facing',
                   'striker_destination_lane', 'victim_destination_lane']
    csv_file = "pos_crash_event.csv"
    try:
        with open(csv_file, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=',', lineterminator='\n')
            writer.writerow(pos_crash_dict)
    except IOError:
        print("I/O error")






#folder_path = '../resources/summary/'
create_csv_file()
folder_path = '../../preprocessed_nhtsa/'
entries = os.listdir(folder_path)
for file in entries:
    jsonFile = glob.glob(folder_path+file)
    summDict = {}
    print(jsonFile[0])
    with open(jsonFile[0], 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        summDict[data['CaseID']] = data['SUMMARY'] # Get Id and Summary of each JSON file.
        summary = preprocessing(data['SUMMARY'])
        striker_damage_area = data['STRIKER_AREA_DAMAGE']
        victim_damage_area = data['HIT_AREA_DAMAGE']
        pre_crash_event(data['CaseID'])
        crash_event(summary)

        pos_crash_dict['case_id'] = data['CaseID']
        pos_crash_dict['number_of_vehicles'] = data['NumOfVehicle']
        pos_crash_dict['striker_damage_area'] = striker_damage_area
        pos_crash_dict['victim_damage_area'] = victim_damage_area

        saveDictionaryToCsvFile()



print(crash_counter)