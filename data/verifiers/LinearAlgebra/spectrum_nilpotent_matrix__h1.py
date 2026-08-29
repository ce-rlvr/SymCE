import sympy
from sympy import eye, zeros, Rational, Integer, Symbol, Matrix, simplify
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: There exists a positive integer k such that A^k = 0",
    "¬Q: Not every eigenvalue of A is equal to 0"
]

N_HYP = 1
NEG_Q_INDEX = 1

def check_zero(obj):
    try:
        if hasattr(obj, 'is_zero_matrix'):
            if obj.is_zero_matrix:
                return True
    except Exception:
        pass
    
    try:
        if hasattr(obj, 'is_zero') and obj.is_zero:
            return True
    except Exception:
        pass
    
    try:
        eq = (obj == 0)
        if isinstance(eq, bool):
            if eq: 
                return True
    except Exception:
        pass
    
    try:
        if hasattr(obj, '__iter__') and not isinstance(obj, str):
            all_zero = True
            for e in obj:
                if not check_zero(e):
                    all_zero = False
                    break
            if all_zero:
                return True
    except Exception:
        pass
    
    try:
        if simplify(obj) == 0:
            return True
    except Exception:
        pass
    
    return False

def conditions(witness):
    h1_ok = False
    try:
        for k in range(1, 51):
            try:
                Ak = witness**k
                if check_zero(Ak):
                    h1_ok = True
                    break
            except Exception:
                pass
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        if hasattr(witness, 'eigenvals'):
            evs = witness.eigenvals()
            if isinstance(evs, dict):
                ev_list = list(evs.keys())
            else:
                ev_list = list(evs)
            
            if len(ev_list) == 0:
                every_zero = True
            else:
                every_zero = all(check_zero(ev) for ev in ev_list)
                
            neg_q_ok = not every_zero
        else:
            every_zero = check_zero(witness)
            neg_q_ok = not every_zero
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]