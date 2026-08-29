import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "¬Q: ker(f) is not a two-sided ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        # Parse the witness to extract the domain size n (representing ring Z_n)
        # and the mapping f: Z_n -> S
        if isinstance(witness, list):
            n = len(witness)
            f = {i: witness[i] for i in range(n)}
            h1 = n > 0
        elif isinstance(witness, dict):
            n = len(witness)
            f = witness
            if all(isinstance(k, int) for k in f.keys()) and set(f.keys()) == set(range(n)):
                h1 = n > 0
            else:
                h1 = False
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, S, f_obj = witness
            if isinstance(R, int):
                n = R
            elif hasattr(R, '__len__'):
                n = len(R)
            else:
                n = -1
                
            if isinstance(f_obj, list):
                f = {i: f_obj[i] for i in range(len(f_obj))}
            elif isinstance(f_obj, dict):
                f = f_obj
            elif callable(f_obj):
                try:
                    f = {i: f_obj(i) for i in range(n)}
                except Exception:
                    f = {}
            else:
                f = {}
                
            if n > 0 and set(f.keys()) == set(range(n)):
                h1 = True
            else:
                h1 = False
        elif callable(witness):
            try:
                f = {i: witness(i) for i in range(2)}
                n = 2
                h1 = True
            except Exception:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    if not h1:
        return [False, False]

    try:
        # The kernel is the set of elements mapping to 0
        ker = {i for i in range(n) if f[i] == 0}
        
        is_ideal = True
        if not ker:
            is_ideal = False
        elif 0 not in ker:
            is_ideal = False
        else:
            # Check if ker is closed under addition and negation mod n
            for a in ker:
                for b in ker:
                    if (a + b) % n not in ker:
                        is_ideal = False
                        break
                if (-a) % n not in ker:
                    is_ideal = False
                if not is_ideal:
                    break
            
            # Check if ker absorbs multiplication from Z_n
            if is_ideal:
                for a in ker:
                    for r in range(n):
                        if (a * r) % n not in ker:
                            is_ideal = False
                            break
                        if (r * a) % n not in ker:
                            is_ideal = False
                            break
                    if not is_ideal:
                        break
                        
        neg_q = not is_ideal
    except Exception:
        neg_q = False
        
    return [h1, neg_q]