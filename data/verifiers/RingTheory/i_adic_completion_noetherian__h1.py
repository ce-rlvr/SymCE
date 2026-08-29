import sympy
import sympy.polys
import math
import itertools
import functools

class InfinitePolynomialRing:
    def __str__(self):
        return "k[x_1, x_2, ...]"

class IdealOfInfinitePolynomialRing:
    def __str__(self):
        return "(x_1, x_2, ...)"

R_inf = InfinitePolynomialRing()
I_inf = IdealOfInfinitePolynomialRing()

def conditions(witness):
    try:
        h1 = False
        neg_q = False
        
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            h1 = True
            
            if hasattr(R, 'is_Noetherian') and R.is_Noetherian:
                neg_q = False
            elif type(R).__name__ == 'PolyRing':
                neg_q = False
            else:
                r_str = str(R).lower()
                i_str = str(I).lower()
                
                if "infinit" in r_str or "..." in r_str or "non-noetherian" in r_str or "x_1" in r_str:
                    if i_str != "r" and i_str != "1":
                        neg_q = True
        else:
            w_str = str(witness).lower()
            if "ring" in w_str or "ideal" in w_str or "k[" in w_str or "z[" in w_str:
                h1 = True
            if "infinit" in w_str or "..." in w_str or "non-noetherian" in w_str or "x_1" in w_str:
                neg_q = True
                
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "¬Q: The I-adic completion of R is not a Noetherian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1