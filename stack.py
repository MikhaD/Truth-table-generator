class Stack:
    def __init__(this, *args):
        if args.__len__() == 0:
            this.stack = []
        elif args.__len__() == 1 and type(args[0]) is list:
            this.stack = args[0]
        else:
            this.stack = list(args)
    def push(this, val):
        this.stack.append(val)
    def pop(this):
        return this.stack.pop(-1)
    def top(this):
        return this.stack[-1]
    def height(this):
        return this.stack.__len__()
    def clear(this):
        this.stack = []