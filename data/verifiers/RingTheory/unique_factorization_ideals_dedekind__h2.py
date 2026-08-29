import sympy
from sympy import ZZ, QQ

Z = ZZ
Q = QQ

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                R, I = witness
            else:
                return [False, False]
        else:
            R = ZZ
            I = witness
            
        is_dedekind = False
        if R in (ZZ, QQ):
            is_dedekind = True
            
        if not is_dedekind:
            return [False, False]
            
        if type(I) is bool:
            return [False, False]
            
        if not isinstance(I, (int, sympy.Integer)):
            return [False, False]
            
        h1 = True
        
        # In a Dedekind domain, the zero ideal (0) cannot be uniquely factored 
        # into prime ideals because (0) = (0) * P for any prime ideal P.
        # Non-zero ideals factor uniquely.
        neg_q = (int(I) == 0)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a Dedekind domain",
    "¬Q: I cannot be uniquely expressed as a product of prime ideals of R, up to the order of the factors"
]

N_HYP = 1
NEG_Q_INDEX = 1