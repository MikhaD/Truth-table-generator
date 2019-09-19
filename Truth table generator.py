"""Generate a truth table for a logical proposition"""
__author__ = 'Mikha'
#15/09/2019
from json import load, dump
from functions import *
# Add smart mode which puts every set of brackets on the truth table, with the exception of brackets with not <variable> in them, and uses generated symbols

# hook up a pyqt5 gui with checkboxes for things like verbose, which symbols to accept for each operator, a button to clear etc.

# Add the LaTeX symbols that are used in webworks so problems can be copied straight from the questions.
# covert the LaTeX symbols straight to their single character equivalents in the edit box 

# Order of operations is PARENTHATSES, NOT, AND, OR
with open("operators.json", "r", encoding="utf8") as opsFile:
    operators = load(opsFile)

proposition = input("Please enter a proposition to generate a truth table for (0 to exit):\n")
while proposition != "0":
    variables = []
    modedProp = proposition.lower()
    verbose = 1 if (input("Verbose table (y/n, default n): ").lower() == "y") else 0
    
    modedProp = standardiseOperators(modedProp, operators[0])

    for i, char in enumerate(modedProp):
        if char.isalpha() and char not in variables:
            variables.append(char)
            modedProp = modedProp.replace(char, f"({char})")

    try:
        modedProp = partition(modedProp)

        if verbose and len(modedProp) > 1:
            modedPropParts = [array for array in modedProp if type(array) is list and not (len(array) == 1 and type(array[0]) is str)]

            if modedPropParts:
                propParts = partition(proposition)
                propParts = [array for array in propParts if type(array) is list]
                propParts = [restore(array) for array in propParts]
                modedPropParts = [simplify(array, operators[0]) for array in modedPropParts]
                modedPropParts = [partitionIfs(array) for array in modedPropParts]
                modedPropParts = [refactor(array, operators) for array in modedPropParts]
                modedPropParts = [clean(array) for array in modedPropParts]
                modedPropParts = [restore(array) for array in modedPropParts]
        else: verbose = 0

        modedProp = simplify(modedProp, operators[0])
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