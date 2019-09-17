"""Generate a truth table for a logical proposition"""
__author__ = 'Mikha'
#15/09/2019
# Put functions in a seperate file

# Add smart mode which puts every set of brackets on the truth table, with the exception of brackets with not <variable> in them, and uses generated symbols

# Read all symbols from a JSON file

# hook up a pyqt5 gui with checkboxes for things like verbose, which symbols to accept for each operator, a button to clear etc.

# correct the symbols being used and add the new ones from https://en.wikipedia.org/wiki/List_of_logic_symbols

# Add the LaTeX symbols that are used in webworks so problems can be copied straight from the questions.
# covert the LaTeX symbols straight to their single character equivalents in the edit box

# Order of operations is PARENTHATSES, NOT, AND, OR
operators = {
"!":["not", "~", "¬"],
"⟡":["then"],
"⊕":["xor", "⊻"],
"⇔":["xnor", "↔", "<->", "<=>", "≡", "iff"],
"⇒":["->", "→", "=>", "⊃"],
"◄":["if and only if"],
"►":["if"],
"⊼":["nand", "|", "↑"],
"&":["and", "∧", "."],
"⊽":["nor", "↓"],
"∥":["or", "∨", "+"]}

from stack import Stack

class propositionError(Exception):
    pass

def standardiseOperators(string, opsDict):
    for ops in opsDict:
        string = string.replace(ops, f"{ops} ")
        for op in opsDict[ops]:
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

# Integrate simplify into simplify operations
def simplify(array):
    """simplify"""
    simplified = []
    for element in array:
        if type(element) is list:
            simplified.append(simplify(element))
        else:
            simplified.extend(simplifyOperations(element.split(), operators))
    return simplified

def refactor(array, operators):
    if len(array) == 1 and type(array[0]) is str: return array
    """convert all non basic operations into their base operation equivalents, and replace all symbols with operations"""
    prfSufOps = {"⇒":"['not', x, 'or', y]", "⇔":"[[x, 'and', y], 'or', 'not', [x, 'or', y]]", "⊼":"['not', [x, 'and', y]]", "⊽":"['not', [x, 'or', y]]", "⊕":"[[x, 'or', y], 'and', 'not', [x, 'and', y]]", "∥":"[x, 'or', y]", "&":"[x, 'and', y]"}
    suffixOps = {"►":"['not', x, 'or', y]", "◄":"[[x, 'and', y], 'or', 'not', [x, 'or', y]]"}
    words = {"&":"and", "∥":"or"}
    answer = []
    i = 0
    while i < len(array):
        firstNot, secondNot = 0, 0
        x, y = [], []
        if type(array[i]) is list:
            array[i] = refactor(array[i], operators)
            i += 1
            continue
        elif array[i] in suffixOps:
            if array[i+1] == "!":
                firstNot = 1
                x = ["not", refactor(array[i+1+firstNot], operators)]
            else: x = refactor(array[i+1+firstNot], operators)
            if array[i+3+firstNot] == "!":
                secondNot = 1
                y = ["not", refactor(array[i+3+firstNot+secondNot], operators)]
            else: y = refactor(array[i+3+firstNot+secondNot], operators)
            answer.append(eval(suffixOps[array[i]].replace("x", str(x)).replace("y", str(y))))
        elif array[i] in prfSufOps:
            try:
                x = ["not", refactor(array[i-1], operators)] if (i-2 >= 0 and array[i-2] == "not") else refactor(array[i-1], operators)
                y = ["not", refactor(array[i+2], operators)] if (array[i+1] == "!") else refactor(array[i+1], operators)
            except IndexError:
                raise propositionError(f"invalid {operators[array[i]][0]} statement")
            answer.append(eval(prfSufOps[array[i]].replace("x", str(x)).replace("y", str(y))))
        elif array[i] == "!":
            array[i] = "not"
        i += len(x) + len(y) + (0 if type(array[i]) is list or array[i] not in suffixOps else 1)
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

proposition = input("Please enter a proposition to generate a truth table for (0 to exit):\n")
while proposition != "0":
    variables = []
    modedProp = proposition.lower()
    verbose = 1 if (input("Verbose table (y/n, default n): ").lower() == "y") else 0
    
    modedProp = standardiseOperators(modedProp, operators)

    for i, char in enumerate(modedProp):
        if char.isalpha() and char not in variables:
            variables.append(char)
            modedProp = modedProp.replace(char, f"({char})")

    try:
        modedProp = partition(modedProp)
        # print(modedProp)
        if verbose and len(modedProp) > 1:
            modedPropParts = [array for array in modedProp if type(array) is list and not (len(array) == 1 and type(array[0]) is str)]

            if modedPropParts:
                propParts = partition(proposition)
                propParts = [array for array in propParts if type(array) is list]
                propParts = [restore(array) for array in propParts]
                modedPropParts = [simplify(array) for array in modedPropParts]
                modedPropParts = [partitionIfs(array) for array in modedPropParts]
                modedPropParts = [refactor(array, operators) for array in modedPropParts]
                modedPropParts = [clean(array) for array in modedPropParts]
                modedPropParts = [restore(array) for array in modedPropParts]
        else: verbose = 0

        modedProp = simplify(modedProp)
        modedProp = partitionIfs(modedProp)
        modedProp = refactor(modedProp, operators)
        modedProp = clean(modedProp)
        modedProp = restore(modedProp)

        print()
        for var in variables:
            exec(f"{var} = 0")
        try:
            eval(modedProp)
        except:
            raise propositionError("Invalid proposition")

        for var in variables:
            print(f"{var:^3}|", end="")
        if verbose and modedPropParts:
            for subProp in propParts:
                print(f" {subProp} |", end="")
        print(f" {proposition} |")

        for i in range(2**len(variables)):
            for j, value in enumerate("{0:0{1}b}".format(i, len(variables))):
                exec("{0} = {1}".format(variables[j], value))
                print(f"{eval(variables[j]):^3}|", end="")
            if verbose and modedPropParts:
                for i, subProp in enumerate(modedPropParts):
                    print(f"{eval(subProp):^{len(propParts[i])+2}}|", end="")
            print(f"{1 if eval(modedProp) else 0:^{len(proposition)+2}}|")

    except propositionError as exceptionMessage:
        print(exceptionMessage)
    finally:
        proposition = input("\nPlease enter a proposition to generate a truth table for (0 to exit):\n")