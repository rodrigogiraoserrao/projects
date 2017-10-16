from auxiliars import *

def nullConstant(k):
    def aux():
        return k
    return aux
    
def zero(n):
    return 0
    
def succ(n):
    return n+1
    
def projection(tuple_length):
    def get_nth_element(index):
        def aux(*args):
            if len(args) != tuple_length:
                raise Exception("Projection expected {}-tuple and"\
                        " got {}-tuple".format(tuple_length, len(args)))
            if index <= 0 or index > len(args):
                raise Exception("Bad projection index")
            return args[index-1]
        return aux
    return get_nth_element
    
def composition(f, g):
    def aux(*args):
        temp = g(*args)
        if hasattr(temp, "__iter__"):
            return f(*temp)
        else:
            return f(temp)
    return aux
        
def aggregation(*functions):
    def aux(*args):
        out = tuple()
        for func in functions:
            out = out + (func(*args), )
        return out
    return aux
  
def recursion(f, g):
    def aux(*args):
        if args[-1] == 0:
            if len(args) > 1:
                return f(*args[:-1])
            else:
                return f()
        else:
            new_args = list(args)
            new_args[-1] -= 1
            return g(*new_args, aux(*new_args))
    return aux

def minimization(f):
    def aux(*args):
        i = 0
        while f(*args, i) != 0:
            i = i+1
        return i
    return aux