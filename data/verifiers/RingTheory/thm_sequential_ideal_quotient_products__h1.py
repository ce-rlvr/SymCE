import sympy
from sympy import eye, zeros
import itertools

# Standard linear algebra objects
I2 = eye(2)
O2 = zeros(2, 2)

# A finite non-commutative ring: 2x2 matrices over Z/2Z
class Mat2Z2:
    def __init__(self, a, b, c, d):
        self.m = (a % 2, b % 2, c % 2, d % 2)
        
    def __add__(self, other):
        return Mat2Z2(*(x + y for x, y in zip(self.m, other.m)))
        
    def __sub__(self, other):
        return Mat2Z2(*(x - y for x, y in zip(self.m, other.m)))
        
    def __mul__(self, other):
        a1, b1, c1, d1 = self.m
        a2, b2, c2, d2 = other.m
        return Mat2Z2(
            a1 * a2 + b1 * c2,
            a1 * b2 + b1 * d2,
            c1 * a2 + d1 * c2,
            c1 * b2 + d1 * d2
        )
        
    def __eq__(self, other):
        return isinstance(other, Mat2Z2) and self.m == other.m
        
    def __hash__(self):
        return hash(self.m)
        
    def __repr__(self):
        return f"Mat2Z2{self.m}"

M2_Z2 = [Mat2Z2(a, b, c, d) for a in (0, 1) for b in (0, 1) for c in (0, 1) for d in (0, 1)]

def is_in(elem, lst):
    return any(elem == e for e in lst)

def subset(lst1, lst2):
    return all(is_in(e, lst2) for e in lst1)

def unique(lst):
    res = []
    for e in lst:
        if not is_in(e, res):
            res.append(e)
    return res

def conditions(witness):
    try:
        R, I, x, y = witness
    except Exception:
        return [False, False, False]
        
    # H_1: I is an ideal of R
    try:
        if not R or not I:
            h1 = False
        else:
            R_list = unique(R)
            I_list = unique(I)
            
            h1 = True
            if not subset(I_list, R_list):
                h1 = False
            else:
                # Check R is a ring
                zero = R_list[0] - R_list[0]
                if not is_in(zero, R_list):
                    h1 = False
                else:
                    for a in R_list:
                        if not is_in(zero - a, R_list): h1 = False
                        for b in R_list:
                            if not is_in(a + b, R_list): h1 = False
                            if not is_in(a * b, R_list): h1 = False
                            if not is_in(a - b, R_list): h1 = False
                    
                    if h1:
                        has_one = False
                        for e in R_list:
                            if all((e * a == a) and (a * e == a) for a in R_list):
                                has_one = True
                                break
                        if not has_one:
                            h1 = False
                    
                    if h1:
                        for a in R_list:
                            for b in R_list:
                                if a + b != b + a: h1 = False
                                for c in R_list:
                                    if (a + b) + c != a + (b + c): h1 = False
                                    if (a * b) * c != a * (b * c): h1 = False
                                    if a * (b + c) != (a * b) + (a * c): h1 = False
                                    if (a + b) * c != (a * c) + (b * c): h1 = False
                
                # Check I is an ideal
                if h1:
                    if not is_in(zero, I_list):
                        h1 = False
                    for i in I_list:
                        for j in I_list:
                            if not is_in(i + j, I_list): h1 = False
                            if not is_in(i - j, I_list): h1 = False
                        for r in R_list:
                            if not is_in(r * i, I_list): h1 = False
                            if not is_in(i * r, I_list): h1 = False
    except Exception:
        h1 = False

    # H_2: x and y are elements of R
    try:
        h2 = is_in(x, R_list) and is_in(y, R_list)
    except Exception:
        h2 = False

    # ¬Q: The ideal quotient (I : xy) is not equal to ((I : x) : y)
    try:
        # Left quotient: (I : a) = {r in R | r*a in I}
        def left_quotient(ideal_list, elem):
            return [r for r in R_list if is_in(r * elem, ideal_list)]
            
        I_xy = left_quotient(I_list, x * y)
        I_x = left_quotient(I_list, x)
        
        # ((I : x) : y) = {r in R | r*y in I_x}
        I_x_y = [r for r in R_list if is_in(r * y, I_x)]
        
        same = subset(I_xy, I_x_y) and subset(I_x_y, I_xy)
        neg_q = not same
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: x and y are elements of R",
    "¬Q: The ideal quotient (I : xy) is not equal to ((I : x) : y)"
]

N_HYP = 2
NEG_Q_INDEX = 2