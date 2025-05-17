import random


def flipcoin():

    result = random.randint(0, 1)

    if result == 1:
        return True
    
    else :
        return False


print(flipcoin())


