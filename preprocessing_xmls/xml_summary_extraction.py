import xml.etree.ElementTree as ET
import json
import glob

#xmlFiles = glob.glob("../resources/nhtsa/*/*.xml")
xmlFiles = glob.glob("../resources/nhtsa/all_cases/*.xml")
summFolderPath = "../resources/summary/"

for xmlFile in xmlFiles:
    tree = ET.parse(xmlFile);
    root = tree.getroot();

    print(root.attrib)
    # Empty dict
    dict = {}
    # Fill in the entries one by one
    for name, value in root.attrib.items():
        if name == 'CaseID':
            dict[name] = root.attrib[name]
            print(root.attrib[name])

        if name == 'NumOfVehicle':
            dict[name] = root.attrib[name]
            print(root.attrib[name])

    for child in root:
        crashSummary = child.find('Crash/CRASH/XML_CASESUMMARY/SUMMARY')
        dict[crashSummary.tag] = crashSummary.text.strip().replace("\n", "")
    #    print(crashSummary.text)
    summJson = json.dumps(dict)
    print(summJson)

    with open(summFolderPath+dict.get('CaseID')+'.json', 'w', encoding='utf8') as outfile:
        json.dump(dict, outfile)


