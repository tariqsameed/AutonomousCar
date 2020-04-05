# extract rotation from post-crash event sentence.
# rotationExtraction(impact_sentence):
#     pattern = r'.+?(?=' + rotation_type + ')' # clockwise or counterclockwise
#     pre_verb_sentence = re.search(pattern, impact_sentence)
#     filtered_impact_sentence = removeStopWords(pre_verb_sentence)
#     v1_rotation = getStrikerVehicleRotation(filtered_impact_sentence)
#     v2_rotation = getVictimVehicleRotation(filtered_impact_sentence)
# return v1_rotation,v2_rotation # values of V1 and V2 rotation.