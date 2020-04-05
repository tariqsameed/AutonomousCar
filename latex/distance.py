# # extract of distance from post-crash event sentence.
# distanceExtraction(impact_sentence):
#     pattern = r'.+?(?=' + rest + ')'  # rest word2vec
#     pre_rest_sentence = re.search(pattern, impact_sentence)
#     pattern = r'(?<=' + rest + ').*'  # rest word2vec
#     pos_rest_sentence = re.search(pattern, impact_sentence)
#     v1_distance = getStrikerVehicleDistance(pre_rest_sentence,
#                                              pos_rest_sentence)
#     v2_distance = getVictimVehicleDistance(pre_rest_sentence,
#                                             pos_rest_sentence)
#     return v1_distance, v2_distance  # values of V1 and V2 distance.