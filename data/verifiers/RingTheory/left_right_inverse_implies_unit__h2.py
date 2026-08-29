import sympy
from sympy import symbols, Rational, Integer
from sympy.matrices import eye, zeros
import itertools
import math
import functools

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a ring with identity 1",
    "H_2: There exists an element b in R such that ba = 1",
    "H_3: There exists an element c in R such that ac = 1",
    "¬Q: a is not a unit in R or b != c"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    elements_list = []
    a = b = c = one = zero = None
    add_op = mul_op = None

    try:
        if isinstance(witness, dict):
            elements_list = list(witness['elements'])
            zero = witness['zero']
            one = witness['one']
            a = witness['a']
            b = witness['b']
            c = witness['c']
            add_op = witness['add']
            mul_op = witness['mul']
        else:
            elements_list = list(witness.elements)
            zero = witness.zero
            one = witness.one
            a = witness.a
            b = witness.b
            c = witness.c
            add_op = witness.add
            mul_op = witness.mul
    except Exception:
        pass

    def add(x, y):
        if callable(add_op): return add_op(x, y)
        if isinstance(add_op, dict): return add_op[(x, y)]
        return add_op[elements_list.index(x)][elements_list.index(y)]

    def mul(x, y):
        if callable(mul_op): return mul_op(x, y)
        if isinstance(mul_op, dict): return mul_op[(x, y)]
        return mul_op[elements_list.index(x)][elements_list.index(y)]

    try:
        h1 = True
        if not elements_list:
            h1 = False
        elif zero not in elements_list or one not in elements_list:
            h1 = False
        else:
            for x in elements_list:
                if not h1: break
                
                # Identity for addition and multiplication
                if add(x, zero) != x or add(zero, x) != x:
                    h1 = False; break
                if mul(x, one) != x or mul(one, x) != x:
                    h1 = False; break
                
                # Additive inverse
                has_inv = False
                for y in elements_list:
                    if add(x, y) == zero and add(y, x) == zero:
                        has_inv = True; break
                if not has_inv:
                    h1 = False; break
                    
                for y in elements_list:
                    if not h1: break
                    
                    # Closure
                    if add(x, y) not in elements_list:
                        h1 = False; break
                    if mul(x, y) not in elements_list:
                        h1 = False; break
                        
                    # Commutativity of addition
                    if add(x, y) != add(y, x):
                        h1 = False; break
                        
                    for z in elements_list:
                        # Associativity of addition
                        if add(add(x, y), z) != add(x, add(y, z)):
                            h1 = False; break
                            
                        # Distributivity of multiplication over addition
                        if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)):
                            h1 = False; break
                        if mul(add(y, z), x) != add(mul(y, x), mul(z, x)):
                            h1 = False; break
    except Exception:
        h1 = False

    try:
        h2 = (b in elements_list) and (a in elements_list) and (mul(b, a) == one)
    except Exception:
        h2 = False

    try:
        h3 = (c in elements_list) and (a in elements_list) and (mul(a, c) == one)
    except Exception:
        h3 = False

    try:
        is_unit = False
        for u in elements_list:
            if mul(a, u) == one and mul(u, a) == one:
                is_unit = True
                break
        q = is_unit and (b == c)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]