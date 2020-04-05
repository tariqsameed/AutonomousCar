# extract of direction from post-crash event sentence.
# directionExtraction(impact_sentence):
#        pattern = r'.+?(?=' + direction + ')' # direction word2vec
#        pre_direction_sentence = re.search(pattern, impact_sentence)
#        pattern = r'(?<=' + face + ').*'
#        pos_direction_sentence = re.search(pattern, impact_sentence)
#        v1_direction = getStrikerVehicleDegree(pre_direction_sentence, pos_direction_sentence)
#        v2_direction = getVictimVehicleDegree(pre_direction_sentence, pos_direction_sentence)
# return v1_direction,v2_direction # values of V1 and V2 direction.