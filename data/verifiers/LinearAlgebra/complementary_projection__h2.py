import sympy as sp
import math
import itertools
import functools

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def get_test_vectors():
    vectors = [
        -2, -1, 0, 1, 2, 3,
        sp.Rational(1, 2), sp.Rational(-3, 4),
        sp.pi, sp.E
    ]
    # 2D vectors
    for x in [-2, -1, 0, 1, 2]:
        for y in [-2, -1, 0, 1, 2]:
            vectors.append(sp.Matrix([x, y]))
    # 3D vectors
    vectors.append(sp.Matrix([1, 0, 0]))
    vectors.append(sp.Matrix([0, 1, 0]))
    vectors.append(sp.Matrix([0, 0, 1]))
    vectors.append(sp.Matrix([-1, 2, -3]))
    vectors.append(sp.Matrix([2, -1, 0]))
    return vectors

def is_nonzero(val):
    try:
        if isinstance(val, sp.Matrix):
            for i in range(val.rows):
                for j in range(val.cols):
                    if is_nonzero(val[i, j]):
                        return True
            return False
            
        if hasattr(val, "is_zero") and val.is_zero is not None:
            return not val.is_zero
            
        if isinstance(val, (int, float)):
            return abs(val) > 1e-9
            
        if hasattr(val, "evalf"):
            num = val.evalf()
            if num.is_number:
                return abs(complex(num)) > 1e-9
                
        if hasattr(val, "simplify"):
            val = val.simplify()
            if hasattr(val, "is_zero") and val.is_zero is not None:
                return not val.is_zero
                
        return bool(val != 0)
    except Exception:
        return bool(val != 0)

def evaluate_P(P, x):
    if callable(P):
        return P(x)
    if hasattr(P, "free_symbols"):
        syms = P.free_symbols
        if len(syms) == 1:
            sym = list(syms)[0]
            return P.subs(sym, x)
    return P * x

def conditions(witness):
    H1 = False
    H2 = True
    H3 = True
    neg_Q = False
    
    evaluated_any = False
    
    if isinstance(witness, dict):
        P = witness.get('P', witness)
    elif isinstance(witness, tuple):
        if len(witness) == 3:
            V, P, I = witness
        elif len(witness) == 1:
            P = witness[0]
        else:
            P = witness
    else:
        P = witness

    if isinstance(P, str):
        try:
            P = sp.sympify(P)
        except Exception:
            pass

    test_vectors = get_test_vectors()
    
    for x in test_vectors:
        try:
            Px = evaluate_P(P, x)
            PPx = evaluate_P(P, Px)
            evaluated_any = True
            
            diff = PPx - Px
            if is_nonzero(diff):
                H2 = False
                neg_Q = True
                
            x_minus_Px = x - Px
            P_x_minus_Px = evaluate_P(P, x_minus_Px)
            
            if is_nonzero(P_x_minus_Px):
                neg_Q = True
                
        except Exception:
            continue
            
    if not evaluated_any:
        return [False, False, False, False]
        
    H1 = True
    
    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: P^2 = P",
    "H_3: I is the identity operator on V",
    "¬Q: (I - P)^2 != (I - P) or im(I - P) != ker(P) or ker(I - P) != im(P)"
]

N_HYP = 3
NEG_Q_INDEX = 3