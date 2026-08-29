import sympy
from sympy.abc import x
import math
import itertools
import functools

# Top-level setup
# (No specific named objects required for this ring theory conjecture; 
# witnesses can use standard Python ints for ZZ or sympy expressions for QQ[x])

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: d is a submultiplicative Euclidean function on R",
    "H_3: a and b are non-zero elements of R",
    "H_4: a divides b",
    "¬Q: a and b are not associate elements in R"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        R, d, a, b = witness
    except Exception:
        return [False] * 5
        
    # H1: R is a Euclidean domain
    try:
        h1 = R in ["ZZ", "QQ[x]"]
    except Exception:
        h1 = False
        
    # H2: d is a submultiplicative Euclidean function on R
    try:
        if R == "ZZ":
            test_elements = [1, -1, 2, -2, 3, 4, 5, -7]
            if isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)):
                test_elements.extend([int(a), int(b), int(a*b)])
            test_elements = list(set([elem for elem in test_elements if elem != 0]))
        elif R == "QQ[x]":
            test_elements = [sympy.Integer(1), sympy.Integer(-1), x, x**2, 2*x+1]
            if isinstance(a, sympy.Expr) and isinstance(b, sympy.Expr):
                test_elements.extend([a, b, a*b])
            test_elements = list(set([elem for elem in test_elements if elem != 0]))
        else:
            test_elements = []
            
        h2 = True
        if not test_elements:
            h2 = False
            
        # Check d maps to non-negative integers
        if h2:
            for elem in test_elements:
                val = d(elem)
                if not isinstance(val, (int, sympy.Integer)) or val < 0:
                    h2 = False
                    break
                    
        # Check submultiplicative and standard property
        if h2:
            for x_elem in test_elements:
                for y_elem in test_elements:
                    xy = x_elem * y_elem
                    if xy != 0:
                        d_xy = d(xy)
                        d_x = d(x_elem)
                        d_y = d(y_elem)
                        if d_xy > d_x * d_y:
                            h2 = False
                            break
                        if d_x > d_xy:
                            h2 = False
                            break
                if not h2:
                    break
                    
        # Check division algorithm
        if h2:
            for x_elem in test_elements:
                for y_elem in test_elements:
                    if y_elem != 0:
                        if R == "ZZ":
                            q = int(x_elem) // int(y_elem)
                            found = False
                            for dq in [-2, -1, 0, 1, 2]:
                                q_test = q + dq
                                r_test = int(x_elem) - q_test * int(y_elem)
                                if r_test == 0 or d(r_test) < d(y_elem):
                                    found = True
                                    break
                            if not found:
                                h2 = False
                                break
                        elif R == "QQ[x]":
                            q, r = sympy.div(x_elem, y_elem, domain='QQ')
                            if not (r == 0 or d(r) < d(y_elem)):
                                h2 = False
                                break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H3: a and b are non-zero elements of R
    try:
        if R == "ZZ":
            h3 = isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)) and a != 0 and b != 0
        elif R == "QQ[x]":
            h3 = isinstance(a, sympy.Expr) and isinstance(b, sympy.Expr) and a != 0 and b != 0
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: a divides b
    try:
        if R == "ZZ":
            h4 = (int(b) % int(a) == 0)
        elif R == "QQ[x]":
            _, r = sympy.div(b, a, domain='QQ')
            h4 = (r == 0)
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: a and b are not associate elements in R
    try:
        if R == "ZZ":
            div_ab = (int(b) % int(a) == 0)
            div_ba = (int(a) % int(b) == 0)
            are_assoc = div_ab and div_ba
        elif R == "QQ[x]":
            _, r1 = sympy.div(b, a, domain='QQ')
            _, r2 = sympy.div(a, b, domain='QQ')
            are_assoc = (r1 == 0) and (r2 == 0)
        else:
            are_assoc = True
        neg_q = not are_assoc
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]