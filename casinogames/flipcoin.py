import random


def flipcoin():

    result = random.randint(0, 1)

    if result == 1:
        return {"Round_result":"Win"}
    
    else :
        return {"Round_result":"Loss"}







