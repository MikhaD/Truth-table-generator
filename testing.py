"""Regular expression module testing"""
__author__ = 'Mikha'
#03/09/2019
import re

string = "(a or b) and not (a and (b)) xor not (c)"
result = re.search(r"not \(.*?\)", string)
print(result.group(0))
print(re.sub(r"not \(.*?\)", "test", string))