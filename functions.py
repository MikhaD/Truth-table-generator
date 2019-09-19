from stack import Stack

class propositionError(Exception):
    pass

def standardiseOperators(string, operators):
    """Ensure the same symbol is being used for all of the various operations"""
    for ops in operators:
        string = string.replace(ops, f"{ops} ")
        for op in operators[ops]:
            string = string.replace(op, f"{ops} ")
    return string

def partition(string):
    """Split a proposition up into lists where each list was a set of brackets or an atomic proposition"""
    result = []
    stack = Stack()
    start = 0
    for i, char in enumerate(string):
        if char in {"(", "[", "{"}:
            stack.push(i)
        elif char in {")", "]", "}"}:
            if stack.height() == 0:
                raise propositionError("Uneven brackets")
            lastOpen = stack.pop()
            if stack.height() == 0:
                if lastOpen > start: result.append(string[start:lastOpen].strip())
                result.append(partition(string[lastOpen+1:i]))
                start = i + 1
    if start < len(string): result.append(string[start::].strip())
    return result

# Integrate simplify into simplify operations
def simplify(array, operators):
    """simplify"""
    simplified = []
    for element in array:
        if type(element) is list:
            simplified.append(simplify(element, operators))
        else:
            simplified.extend(simplifyOperations(element.split(), operators))
    return simplified

# The section of this function that checks whether a function is legal needs to be checked.
def simplifyOperations(array, operators):
    """simplify array of consecutive operations by removing useless nots and ensuring all operations are valid"""
    if len(array) == 1 and array[0] is str and len(array[0]) == 1: return array
    simplified = []
    allowOthers = True
    nots = 0
    for i, operation in enumerate(array):
        if operation == "!":
            nots += 1
            continue
        elif nots % 2 != 0:
            simplified.append("!")
            nots = 0
        if operation in {"►", "◄"}:
            simplified.append(operation)
            allowOthers = False
        elif allowOthers:
            simplified.append(operation)
            allowOthers = False
        else:
            raise propositionError(f"Invalid {operators[operation][0]} statement")
    if nots % 2 != 0:
        simplified.append("!")
    return simplified

def partitionIfs(array):
    """Put each if/iff then statement in a seperate list in order to execute them in the correct order"""
    result = []
    stack = Stack()
    sArray = str(array)[::-1]
    i = 0
    lastRealClose = None
    while i < len(sArray):
        if sArray[i] == "]":
            stack.push(i)
        elif sArray[i] == "[":
            lastClose = stack.pop()
        elif sArray[i] == "⟡":
            sArray = sArray[:lastClose] + "]" + sArray[lastClose:]
            lastRealClose = lastClose
            i += 1
        elif sArray[i] in {"►", "◄"}:
            sArray = sArray[:i+2] + "[" + sArray[i+2:]
            if lastRealClose: lastClose = lastRealClose
            i += 2
        i += 1
    return eval(sArray[::-1])

def refactor(array, operators):
    if len(array) == 1 and type(array[0]) is str: return array
    """convert all non basic operations into their base operation equivalents, and replace all symbols with operations"""
    answer = []
    i = 0
    while i < len(array):
        firstNot, secondNot = 0, 0
        x, y = [], []
        if type(array[i]) is list:
            array[i] = refactor(array[i], operators)
            i += 1
            continue
        elif array[i] in operators[2]:
            if array[i+1] == "!":
                firstNot = 1
                x = ["not", refactor(array[i+1+firstNot], operators)]
            else: x = refactor(array[i+1+firstNot], operators)
            if array[i+3+firstNot] == "!":
                secondNot = 1
                y = ["not", refactor(array[i+3+firstNot+secondNot], operators)]
            else: y = refactor(array[i+3+firstNot+secondNot], operators)
            answer.append(eval(operators[2][array[i]].replace("x", str(x)).replace("y", str(y))))
        elif array[i] in operators[1]:
            try:
                x = ["not", refactor(array[i-1], operators)] if (i-2 >= 0 and array[i-2] == "not") else refactor(array[i-1], operators)
                y = ["not", refactor(array[i+2], operators)] if (array[i+1] == "!") else refactor(array[i+1], operators)
            except IndexError:
                raise propositionError(f"invalid {operators[0][array[i]][0]} statement")
            answer.append(eval(operators[1][array[i]].replace("x", str(x)).replace("y", str(y))))
        elif array[i] == "!":
            array[i] = "not"
        i += len(x) + len(y) + (0 if type(array[i]) is list or array[i] not in operators[2] else 1)
        i += 1
    if len(answer) == 0:
        answer.extend(array)
    return answer

def clean(array):
    """turn all lists that contain only one element into their element"""
    answer = []
    for element in array:
        if type(element) is list:
            element = clean(element)
            if len(element) == 1 or len(array) == 1:
                answer.extend(element)
                continue
        answer.append(element)
    return answer

def restore(array):
    """transform the array into a string that can be evaluated as a logical proposition"""
    string = ""
    for i, char in enumerate(str(array)[1:-1]):
        if char in {"'", ","}: continue 
        elif char == "[": char = "("
        elif char == "]": char = ")"
        string += char
    return string

# Function to generate the default operators.json file in case it gets deleted
'''
from json import dump
def generateDefaultOperatorsFile(name="operators.json", indent=4):
    operators = {"!":["not", "~", "¬"],"⟡":["then"],"⊕":["xor", "⊻"],"⇔":["xnor", "↔", "<->", "<=>", "≡", "iff"],"⇒":["->", "→", "=>", "⊃"],"◄":["if and only if"],"►":["if"],"⊼":["nand", "|", "↑"],"&":["and", "∧", "."],"⊽":["nor", "↓"],"∥":["or", "∨", "+"]}
    prfSufOps = {"⇒":"['not', x, 'or', y]","⇔":"[[x, 'and', y], 'or', 'not', [x, 'or', y]]","⊼":"['not', [x, 'and', y]]","⊽":"['not', [x, 'or', y]]","⊕":"[[x, 'or', y], 'and', 'not', [x, 'and', y]]","∥":"[x, 'or', y]","&":"[x, 'and', y]"}
    suffixOps = {"►":"['not', x, 'or', y]","◄":"[[x, 'and', y], 'or', 'not', [x, 'or', y]]"}
    with open(name, "w", encoding="utf8") as opsFile:
        dump([operators, prfSufOps, suffixOps], opsFile, indent=indent, ensure_ascii=False)
'''