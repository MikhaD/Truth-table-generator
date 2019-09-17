"""Regular expression module testing"""
__author__ = 'Mikha'
#03/09/2019
# import re

# string = "(a or b) and not (a and (b)) xor not (c)"
# result = re.search(r"not \(.*?\)", string)
# print(result.group(0))
# print(re.sub(r"not \(.*?\)", "test", string))\
a = [[[[[[[["sub"], ["sub", [[["two"]]], ["sub3"]]]]]]]]]

def clean(array):
    answer = []
    for element in array:
        if type(element) is list:
            element = clean(element)
            if len(element) == 1 or len(array) == 1:
                answer.extend(element)
                continue
        answer.append(element)
    return answer

print(clean(a))