# verbose doesn't pick up first bracket if it is the first character
"""Truth table generator"""
__author__ = 'Mikha'
#03/09/2019

# Get XOR working
# Get NAND working
# Get if … then working
# Get if and only if working

def segment(string):
    statements = []
    if string.count("(") > 0:
        i = 0
        while i < string.rfind("("):
            bracs = 1
            start = string.index("(", i)+1
            for i, char in enumerate(string[start:], start):
                if char == "(":
                    bracs += 1
                elif char == ")":
                    bracs -= 1
                if bracs == 0:
                    statements.append(string[start-1:i+1])
                    break
    statements.append(string)
    return statements


operators = {"and":["∧", "&"], "or":["∨", "+"], "not":["~", "¬"], "xor":["⊕"], "nand":["|"]}
atomicProps = []
theirProp = input("Please enter a proposition to generate a truth table for:\n")
verbose = input("Verbose table (y/n, default n): ")
prop = theirProp.lower()

prop.replace("[", "(")
prop.replace("]", ")")
prop.replace("{", "(")
prop.replace("}", ")")
if prop.count("(") == prop.count(")"):
    if verbose == "y":
        theirProp = segment(theirProp)
    else:
        theirProp = [theirProp]
    
    for ops in operators:
        prop = prop.replace(ops, operators[ops][0])

    for i in prop:
        if i in "abcdefghijklmnopqrstuvwxyz" and i not in atomicProps:
            atomicProps.append(i)
            prop = prop.replace(i, f" {i} ")

    for ops in operators:
        for op in operators[ops]:
            prop = prop.replace(op, ops)

    if verbose == "y":
        prop = segment(prop)
    else:
        prop = [prop]
    print()
    for atom in atomicProps:
        print(f"{atom:^3}|", end="")
    for subProp in theirProp:
        print(f"{subProp:^3}|", end="")
    print()

    for i in range(2**len(atomicProps)):  
        for j, k in enumerate("{0:0{1}b}".format(i, len(atomicProps))):
            exec("{0} = {1}".format(atomicProps[j], k))
            print(f"{eval(atomicProps[j]):^3}|", end="")
        for evProp, subProp in zip(prop, theirProp):
            print("{0:^{1}}|".format(eval(evProp), len(subProp)), end="")
        print()
else:
    print("Invalid proposition")