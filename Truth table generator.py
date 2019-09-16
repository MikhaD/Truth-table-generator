"""Generate a truth table for a logical proposition"""
__author__ = 'Mikha'
#15/09/2019
# Put functions in a seperate file

# Read allowed symbols from a JSON file

# do a bracket split on the unfiltered proposition in order to get the verbose mode sub propositions the way they were input

# hook up a pyqt5 gui with checkboxes for things like verbose, which symbols to accept for each operator, a button to clear etc.

# correct the symbols being used and add the new ones from https://en.wikipedia.org/wiki/List_of_logic_symbols

# Add the LaTeX symbols that are used in webworks so problems can be copied straight from the questions.
# covert the LaTeX symbols straight to their single character equivalents in the edit box

# Order of operations is PARENTHATSES, NOT, AND, OR
operators = {
"!":["not", "~", "¬"],
"↔":["<->", "->"],
"↑":["nand", "|", "⊼"],
"&":["and", "∧"],
"⇒":["if and only if"],
"→":["if"],
"⟡":["then"],
"⊕":["xor"],
"⇔":["xnor", "<=>", "=>", "iff"],
"↓":["nor", "⊽"],
"+":["or", "∨"]}

from stack import Stack

class testEx(Exception):
    pass

def partition(string):
    """Split a proposition up into lists where each list was a set of brackets or an atomic proposition"""
    result = []
    stack = Stack()
    start = 0
    for i, char in enumerate(string):
        if char == "(":
            stack.push(i)
        elif char == ")":
            if stack.height() == 0:
                raise testEx("Uneven brackets")
            lastOpen = stack.pop()
            if stack.height() == 0:
                if lastOpen > start: result.append(string[start:lastOpen].strip())
                result.append(partition(string[lastOpen+1:i]))
                start = i + 1
    if start < string.__len__(): result.append(string[start::].strip())
    return result

def partitionIfs(array):
    """Put each if/iff then statement in a seperate list in order to execute them in the correct order"""
    result = []
    stack = Stack()
    sArray = str(array)[::-1]
    i = 0
    while i < sArray.__len__():
        lastRealClose = 0
        if sArray[i] == "]":
            stack.push(i)
        elif sArray[i] == "[":
            lastClose = stack.pop()
        elif sArray[i] == "⟡":
            sArray = sArray[:lastClose] + "]" + sArray[lastClose:]
            lastRealClose = lastClose
            i += 1
        elif sArray[i] in {"→", "⇒"}:
            sArray = sArray[:i+2] + "[" + sArray[i+2:]
            if lastRealClose: lastClose = lastRealClose
            i += 2
        i += 1
    return eval(sArray[::-1])

def simplifyOperations(array):
    """simplify array of consecutive operations by removing useless nots and ensuring all operations are valid"""
    global operators
    simplified = []
    allowOthers = True
    nots = 0
    for i, operation in enumerate(array):
        if operation == "!":
            nots += 1
            continue
        elif operation in {"→", "⇒"}:
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
            simplified.extend(simplifyOperations(element.split()))
    return simplified

def refactor(array):
    if array.__len__() == 1 and type(array[0]) is str: return array
    """convert all non basic operations into their base operation equivalents, and replace all symbols with operations"""
    prfSufOps = {"↔":"['not', x, 'or', y]", "⇔":"[[x, 'and', y], 'or', 'not', [x, 'or', y]]", "↑":"['not', [x, 'and', y]]", "↓":"['not', [x, 'or', y]]", "⊕":"[[x, 'or', y], 'and', 'not', [x, 'and', y]]", "+":"[x, 'or', y]", "&":"[x, 'and', y]"}
    suffixOps = {"→":"['not', x, 'or', y]", "⇒":"[[x, 'and', y], 'or', 'not', [x, 'or', y]]"}
    words = {"&":"and", "+":"or"}
    global operators
    answer = []
    i = 0
    while i < array.__len__():
        firstNot, secondNot = 0, 0
        x, y = [], []
        if type(array[i]) is list:
            i += 1
            continue
        elif array[i] in suffixOps:
            if array[i+1] == "!":
                firstNot = 1
                x = ["not", refactor(array[i+1+firstNot])]
            else: x = refactor(array[i+1+firstNot])
            if array[i+3+firstNot] == "!":
                secondNot = 1
                y = ["not", refactor(array[i+3+firstNot+secondNot])]
            else: y = refactor(array[i+3+firstNot+secondNot])
            answer.append(eval(suffixOps[array[i]].replace("x", str(x)).replace("y", str(y))))
        elif array[i] in prfSufOps:
            try:
                x = ["not", refactor(array[i-1])] if (i-2 >= 0 and array[i-2] == "!") else refactor(array[i-1])
                y = ["not", refactor(array[i+2])] if (array[i+1] == "!") else refactor(array[i+1])
            except IndexError:
                raise testEx(f"invalid {operators[array[i]][0]} statement")
            answer.append(eval(prfSufOps[array[i]].replace("x", str(x)).replace("y", str(y))))
        i += len(x) + len(y) + (0 if type(array[i]) is list or array[i] not in suffixOps else 1)
        i += 1
    return answer

def restore(array):
    """transform the array into a string that can be evaluated as a logical proposition"""
    string = ""
    for i, char in enumerate(str(array)):
        if char in {"'", ","}: continue 
        elif char == "[": char = "("
        elif char == "]": char = ")"
        string += char
    return string


variables = []
proposition = input("Please enter a proposition to generate a truth table for:\n")
modedProp = proposition.lower()
# verbose = input("Verbose table (y/n, default n): ")

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

# modedProp = partition(modedProp)
# modedProp = simplify(modedProp)
# modedProp = partitionIfs(modedProp)
# modedProp = refactor(modedProp)
# modedProp = restore(modedProp)
# modedProp = modedProp[2:-2]

# Find where the extra sets of outside brackets are being added and deal with them there
modedProp = restore(refactor(partitionIfs(simplify(partition(modedProp)))))[2:-2]
# print(modedProp)

print()
for var in variables:
    print(f"{var:^3}|", end="")
print(f" {proposition} |")

for i in range(2**len(variables)):
    for j, value in enumerate("{0:0{1}b}".format(i, len(variables))):
        exec("{0} = {1}".format(variables[j], value))
        print(f"{eval(variables[j]):^3}|", end="")
    print(f"{1 if eval(modedProp) else 0:^{len(proposition)+2}}|")