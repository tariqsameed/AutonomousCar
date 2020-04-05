# extract degree rotation from post-crash event sentence.
# degreeExtraction(impact_sentence):
#      pattern = r'.+?(?=' + degrees + ')' # degrees in rotation
#      pre_degree_sentence = re.search(pattern, impact_sentence)
#      filtered_impact_sentence = removeStopWords(pre_degree_sentence)
#      v1_degree = getStrikerVehicleDegree(filtered_impact_sentence)
#      v2_degree = getVictimVehicleDegree(filtered_impact_sentence)
# return v1_degree,v2_degree # values of V1 and V2  degree rotation.

