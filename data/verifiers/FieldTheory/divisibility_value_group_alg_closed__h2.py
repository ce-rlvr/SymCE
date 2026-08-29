import sympy
from sympy import S
import math
from functools import reduce

# Top-level setup
CC = S.Complexes
ZZ = S.Integers
QQ = S.Rationals
RR = S.Reals

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            K, Gamma, v, samples = witness
        else:
            K = getattr(witness, 'K', None)
            Gamma = getattr(witness, 'Gamma', None)
            v = getattr(witness, 'v', None)
            samples = getattr(witness, 'K_samples', None)
            if K is None or Gamma is None or v is None or samples is None:
                return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: K is an algebraically closed field
    try:
        K_str = str(K).strip()
        h1 = K in [CC, S.AlgebraicNumbers] or K_str in ['CC', 'Complexes', 'C', 'AlgebraicNumbers', 'S.Complexes', 'S.AlgebraicNumbers']
    except Exception:
        h1 = False
        
    # H_2: Gamma is the value group of v
    try:
        h2 = False
        if callable(v):
            get_val = v
        elif isinstance(v, dict):
            get_val = lambda x: v[x]
        else:
            get_val = None
            
        if get_val is not None and samples:
            vals = []
            valid = True
            for x in samples:
                val = get_val(x)
                vals.append(val)
                if Gamma == ZZ or str(Gamma).strip() in ['Z', 'Integers', 'S.Integers', 'ZZ']:
                    if not (isinstance(val, int) or getattr(val, 'is_integer', False)):
                        valid = False
                        break
            if valid:
                if Gamma == ZZ or str(Gamma).strip() in ['Z', 'Integers', 'S.Integers', 'ZZ']:
                    g = reduce(math.gcd, [int(val) for val in vals], 0)
                    if g == 1:
                        h2 = True
    except Exception:
        h2 = False
        
    # ¬Q: Gamma is not a divisible abelian group
    try:
        if Gamma == ZZ or str(Gamma).strip() in ['Z', 'Integers', 'S.Integers', 'ZZ']:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: Gamma is the value group of v",
    "¬Q: Gamma is not a divisible abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2