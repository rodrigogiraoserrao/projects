from basicFunctions import *

id = projection(1)(1)

def addition(x, y):
    f = id
    g = composition(succ, projection(3)(3))
    aux = recursion(f, g)
    return aux(x, y)
    
def pred(n):
    f = nullConstant(0)
    g = projection(2)(1)
    aux = recursion(f, g)
    return aux(n)

def zero_sub(x, y):
    # zero_sub(x, y) = x-y if x>y, 0 otherwise
    f = id
    g = composition(pred, projection(3)(3))
    aux = recursion(f, g)
    return aux(x, y)

def mod_sub(x, y):
    # mod_sub(x, y) = |x - y|
    aux = composition(
                    addition,
                    aggregation(
                                composition(
                                            zero_sub,
                                            aggregation(projection(2)(1), projection(2)(2))),
                                composition(
                                            zero_sub,
                                            aggregation(projection(2)(2), projection(2)(1)))
                    )
    )
    return aux(x, y)

def sgn(x):
    # sgn(x) = 1 if x > 0, 0 otherwise
    aux = composition(
                    zero_sub,
                    aggregation(
                                id,
                                composition(pred, id)))
    return aux(x)

def neq(x, y):
    # neq(x, y) = 1 if x != y
    aux = composition(
                    sgn,
                    composition(
                            mod_sub,
                            aggregation(projection(2)(1), projection(2)(2))))
    return aux(x, y)

def eq(x, y):
    # eq(x, y) = 1 iff x == y
    aux = composition(
                    neq,
                    aggregation(projection(2)(1), projection(2)(2))
                    )
    aux2 = nullConstant(1)
    # I feel I cheated here but I don't see how I could make this right
    return mod_sub(aux2(), aux(x, y))

def geq(x, y):
    # geq(x, y) = 1 iff x >= y, else 0
    aux = composition(sgn,
                    composition(
                                addition,
                                aggregation(
                                            composition(
                                                        sgn,
                                                        composition(
                                                                    zero_sub,
                                                                    aggregation(projection(2)(1), projection(2)(2))
                                                        )
                                            ),
                                            composition(
                                                        eq,
                                                        aggregation(projection(2)(1), projection(2)(2)
                                                        )
                                            )
                                )
                    ))
    return aux(x, y)

# could also define 'greater' first and then make use of it:
def greater(x, y):
    # greater(x, y) = 1 iff x > y, else 0
    aux = composition(
                    sgn,
                    composition(
                                zero_sub,
                                aggregation(projection(2)(1), projection(2)(2)))
    )
    return aux(x, y)

def less(x, y):
    # less(x, y) = 1 iff x < y, else 0
    aux = composition(
                    sgn,
                    composition(
                                zero_sub,
                                aggregation(projection(2)(2), projection(2)(1)))
    )
    return aux(x, y)

def geq2(x, y):
    # geq2(x, y) = 1 iff x >= y, else 0
    aux = composition(
                    addition,
                    aggregation(
                                composition(
                                            greater,
                                            aggregation(projection(2)(1), projection(2)(2))
                                ),
                                composition(
                                            eq,
                                            aggregation(projection(2)(1), projection(2)(2))
                                )
                    )
    )
    return aux(x, y)

def leq(x, y):
    # leq(x, y) = 1 iff x <= y, else 0
    aux = composition(
                    addition,
                    aggregation(
                                composition(
                                            less,
                                            aggregation(projection(2)(1), projection(2)(2))
                                ),
                                composition(
                                            eq,
                                            aggregation(projection(2)(1), projection(2)(2))
                                )
                    )
    )
    return aux(x, y)

def subtraction(x, y):
    # subtraction(x, y) = x-y if x>=y, undefined otherwise
    aux = composition(
                    neq,
                    aggregation(
                                projection(3)(1),
                                composition(
                                            addition,
                                            aggregation(projection(3)(2), projection(3)(3))
                                )
                    )
    )
    aux = minimization(aux)
    return aux(x, y)
    
def dup(n):
    aux = composition(addition, aggregation(id, id))
    return aux(n)
    
def mult(x, y):
    f = zero
    g = composition(addition,
                        aggregation(projection(3)(3), projection(3)(1))
                    )
    aux = recursion(f, g)
    return aux(x, y)
    
def factorial(n):
    f = nullConstant(1)
    g = composition(mult, aggregation(composition(succ, projection(2)(1)),
                                        projection(2)(2))
                    )
    aux = recursion(f, g)
    return aux(n)

def quotient(n, d):
    # quotient(n, d) = q if qd + r = n with q,r >= 0 and r < d
    aux = composition(
                    mult,
                    aggregation(
                                composition(
                                            leq,
                                            aggregation(
                                                        composition(
                                                                    mult,
                                                                    aggregation(projection(3)(2), projection(3)(3))
                                                        ),
                                                        projection(3)(1)
                                            )
                                ),
                                composition(
                                            leq,
                                            aggregation(
                                                        composition(
                                                                    mult,
                                                                    aggregation(
                                                                                projection(3)(2),
                                                                                composition(
                                                                                            succ,
                                                                                            projection(3)(3)
                                                                                )
                                                                    ),
                                                        ),
                                                        projection(3)(1)
                                            )
                                )
                    )
    )
    aux = minimization(aux)
    return aux(n, d)

def remainder(n, d):
    # remainder(n, d) = n%d
    aux = composition(
                    neq,
                    aggregation(
                                projection(3)(1),
                                composition(
                                            addition,
                                            aggregation(
                                                        projection(3)(3),
                                                        composition(
                                                                    mult,
                                                                    aggregation(
                                                                                composition(
                                                                                            quotient,
                                                                                            aggregation(projection(3)(1), projection(3)(2))
                                                                                ),
                                                                                projection(3)(2)
                                                                    )
                                                        )
                                            )
                                )
                    )
    )
    aux = minimization(aux)
    return aux(n, d)
