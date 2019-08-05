import xml.etree.ElementTree as ET
import json
import glob
import csv

#xmlFiles = glob.glob("../resources/nhtsa/*/*.xml")
xmlFiles = glob.glob("../../NHTSA-cases/*.xml")
summFolderPath = "../../preprocessed_nhtsa/"

print(len(xmlFiles))


csv_columns = ['case_id','summary']
csv_file = "crash_event_summary.csv"
try:
    with open(csv_file, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=',', lineterminator='\n')
        writer.writeheader()
except IOError:
    print("I/O error")



for xmlFile in xmlFiles:
    tree = ET.parse(xmlFile);
    root = tree.getroot();

    crash_event_dict = {}
    # Fill in the entries one by one
    for name, value in root.attrib.items():
        if name == 'CaseID':
            crash_event_dict['case_id'] = root.attrib[name]

    for child in root:
        crashSummary = child.find('Crash/CRASH/XML_CASESUMMARY/SUMMARY')
        crash_event_dict['summary'] = crashSummary.text.strip().replace("\n", "")

    try:
        with open(csv_file, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=',', lineterminator='\n')
            writer.writerow(crash_event_dict)
    except IOError:
        print("I/O error")



