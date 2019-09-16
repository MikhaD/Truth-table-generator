"""Regular expression module testing"""
__author__ = 'Mikha'
#03/09/2019
# import re

# string = "(a or b) and not (a and (b)) xor not (c)"
# result = re.search(r"not \(.*?\)", string)
# print(result.group(0))
# print(re.sub(r"not \(.*?\)", "test", string))\
def restore(array):
    """transform the array into a string that can be evaluated as a logical proposition"""
    string = ""
    for i, char in enumerate(str(array)):
        if char in {"'", ","}: continue 
        elif char == "[": char = "("
        elif char == "]": char = ")"
        string += char
    return string

print(restore(["this", ["array"], "is", "a", "test"]))