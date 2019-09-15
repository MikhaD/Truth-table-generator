"""Generate a truth table for a logical proposition"""
__author__ = 'Mikha'
#15/09/2019

#######ALGORITHM#######
# - replace all types of brackets with parenthases
# - replace all words with symbols in order to extract the atomic propositions
# - extract atomic propositions and store for later
# X put brackets around each atomic proposition in the string
# - Split string into symbols and first level of brackets
#           All passes over should go into each element recursively
# Pass over array and combine all not symbols with the element in front of them, replacing each type of symbol with the word
# Pass over array and combine all and symbols with the elements in front and behind each one, replacing each type of symbol with the word
# Pass over array and combine all or symbols with the elements in front and behind each one, replacing each type of symbol with the word
# pass over array and combine all nand symbols and the elements before and after them into not (el before and el after)
# pass over array and combine all xor symbols and the elements before and after them into (el before or el after) and not (el before and el after)
# pass over array and find each corresponding pair of if then and convert to the form (not el before) or el after
# pass over array and combine all if then symbols and the elements before and after them into (not el before) or el after
# pass over array and find each corresponding pair of iff then and covert to the form (el before and el after) or not (el before or el after)
# pass over array and combine all iff then symbols and the elements before and after them into (el before and el after) or not (el before or el after)
# combine array into a large string and evaluate it for all the combinations of the atomic propositions and print a truth table

# Eventually hook up a gui with checkboxes for things like verbose, which symbols to accept for each operator, a button to clear etc.

# Order of operations is PARENTHATSES, NOT, AND, OR

# Get XOR working
# Get NAND working
# Get if … then working
# Get if and only if working

# Deal with <-> and <=>

from stack import Stack
class testEx(Exception):
    pass

def partition(string):
    """Split a proposition up into lists where each list was a set of brackets or an atomic proposition"""
    result = []
    stack = Stack((0, ""))
    start = 0
    for i, char in enumerate(string):
        if char == "(":
            stack.push(i)
        elif char == ")":
            if stack.height() == 1:
                raise testEx("Uneven brackets")
            lastOpen = stack.pop()
            if stack.height() == 1:
                if lastOpen > start: result.append(string[start:lastOpen].strip())
                result.append(partition(string[lastOpen+1:i]))
                start = i + 1
    if start < string.__len__(): result.append(string[start::].strip())
    return result

def simplifyOperations(array):
    """simplify array of consecutive operations by removing useless nots and ensuring all operations are valid"""
    suffixOps = {"ﬁ", "ﬀ"}
    global operators
    simplified = []
    allowOthers = True
    nots = 0
    for i, operation in enumerate(array):
        if operation == "!":
            nots += 1
            continue
        elif operation in {"ﬁ", "ﬀ"}:
            simplified.append(operation)
            allowOthers = False
        elif allowOthers:
            simplified.append(operation)
            allowOthers = False
        else:
            raise testEx(f"Invalid {operators[operation][0]} statement")
        if nots % 2 != 0:
            simplified.append("!")
        nots = 0
    if nots % 2 != 0:
        simplified.append("!")
    return simplified

def simplify(array):
    """simplify"""
    simplified = []
    for element in array:
        if type(element) is list:
            simplified.append(simplify(element))
        else:
            simplified.append(" ".join(simplifyOperations(element.split())))
    return simplified

operators = {"ﬀ":["if and only if", "xnor"], "ﬁ":["if"], "æ":["then"], "&":["and", "∧"], "+":["or", "∨"], "!":["not", "~", "¬"], "⊕":["xor"], "|":["nand"], "↔":["<->"], "⇔":["<=>", "iff"]}
variables = []

proposition = input("Please enter a proposition to generate a truth table for:\n")
modedProp = proposition.lower()
verbose = input("Verbose table (y/n, default n): ")

for ops in operators:
    modedProp = modedProp.replace(ops, f"{ops} ")
    for op in operators[ops]:
        modedProp = modedProp.replace(op, f"{ops} ")

for i, char in enumerate(modedProp):
    if char in {"[", "{"}:
        modedProp[i] = "("
    elif char in {"]", "}"}:
        modedProp[i] = ")"
    elif char.isalpha() and char not in variables:
        variables.append(char)
        modedProp = modedProp.replace(char, f"({char})")

modedProp = partition(modedProp)

for i, element in enumerate(modedProp):
    if type(element) is not list:
        operations = element.split()
        if operations.__len__() == 1 and i == 0 and operations[0] != "!":
            raise testEx("Invalid operation")
        
