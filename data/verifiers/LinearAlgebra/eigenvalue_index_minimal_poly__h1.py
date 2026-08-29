import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, lambda_val, k = witness
    except Exception:
        return [False, False, False]

    # H1: lambda_val is an eigenvalue of A
    try:
        if not getattr(A, "is_square", False):
            h1 = False
        else:
            evs = A.eigenvals()
            h1 = False
            for ev in evs:
                if sympy.simplify(lambda_val - ev) == 0:
                    h1 = True
                    lambda_val = ev  # Use the exact SymPy expression for subsequent checks
                    break
    except Exception:
        h1 = False

    # H2: k is the multiplicity of lambda_val as a root of the minimal polynomial of A
    try:
        mp = sympy.minpoly(A, x)
        
        roots_dict = sympy.roots(mp, x)
        mult = 0
        found = False
        for r, m in roots_dict.items():
            if sympy.simplify(lambda_val - r) == 0:
                mult = m
                found = True
                break
        
        if not found:
            # Fallback for cases where sympy.roots might fail to find the root
            mp_temp = mp
            factor = x - lambda_val
            while True:
                q, rem = sympy.div(mp_temp, factor)
                if sympy.simplify(rem) == 0:
                    mult += 1
                    mp_temp = q
                else:
                    break
                    
        h2 = (k == mult)
    except Exception:
        h2 = False

    # neg_Q: k is NOT the index of lambda_val
    try:
        I = sympy.eye(A.rows)
        B = A - lambda_val * I
        
        m = 0
        B_m = I
        B_m1 = B
        
        while True:
            ns_m = B_m.nullspace()
            ns_m1 = B_m1.nullspace()
            
            # The null space dimension strictly increases until it stabilizes at the index
            if len(ns_m) == len(ns_m1):
                index = m
                break
            
            m += 1
            B_m = B_m1
            B_m1 = B_m1 * B
            
            # Prevent infinite loop in case of unexpected symbolic behavior
            if m > A.rows + 5:
                index = -1
                break
                
        neg_q = (k != index)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: lambda is an eigenvalue of A",
    "H_2: k is the multiplicity of lambda as a root of the minimal polynomial of A",
    "¬Q: k is not the index of lambda"
]

N_HYP = 2
NEG_Q_INDEX = 2