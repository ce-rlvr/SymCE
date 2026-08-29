import sympy
from sympy import ZZ, QQ

# Top-level setup
Z = ZZ
Q = QQ

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a Noetherian ring",
    "¬Q: There do not exist prime ideals P_1, ..., P_n containing I such that P_1 ... P_n is contained in I"
]

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a tuple (R, I) where R is a ring (like ZZ) 
    and I is either a subset (e.g., [2]) or an ideal representation (e.g., ('ideal', [2])).
    """
    try:
        R, I = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a commutative ring with identity
    try:
        h1 = (R in [ZZ, QQ]) or (hasattr(R, 'is_CommutativeRing') and R.is_CommutativeRing)
    except Exception:
        h1 = False
        
    # H_2: R is a Noetherian ring
    try:
        # ZZ and QQ are Noetherian rings.
        h2 = (R in [ZZ, QQ])
    except Exception:
        h2 = False
        
    # ¬Q: There do NOT exist prime ideals P_1, ..., P_n (n >= 1) containing I 
    # such that P_1 ... P_n is contained in I.
    try:
        if R == ZZ:
            if I == ZZ:
                # I is the whole ring. No proper prime ideals contain ZZ.
                neg_q = True
            elif isinstance(I, tuple) and len(I) == 2 and I[0] == 'ideal':
                gens = I[1]
                if not gens:
                    # Ideal is (0). P_1 = (0) contains (0) and is contained in (0).
                    neg_q = False
                else:
                    g = sympy.gcd_list(gens)
                    if g == 1 or g == -1:
                        # Ideal is ZZ. No proper prime ideals contain ZZ.
                        neg_q = True
                    else:
                        # Ideal is (g) with g != 1. We can always form a product of prime ideals
                        # containing (g) that is contained in (g) by repeating prime factors.
                        neg_q = False
            else:
                # I is treated as a subset of ZZ.
                try:
                    if isinstance(I, (int, sympy.Integer)):
                        I_set = {I}
                    else:
                        I_set = set(I)
                except Exception:
                    I_set = set()
                
                # An infinite ideal can never be contained in a finite subset.
                # The only finite ideal is (0) = {0}.
                if I_set == {0}:
                    neg_q = False
                else:
                    neg_q = True
                    
        elif R == QQ:
            if I == QQ:
                neg_q = True
            elif isinstance(I, tuple) and len(I) == 2 and I[0] == 'ideal':
                gens = I[1]
                if all(g == 0 for g in gens):
                    neg_q = False
                else:
                    neg_q = True
            else:
                try:
                    if isinstance(I, (int, sympy.Integer)):
                        I_set = {I}
                    else:
                        I_set = set(I)
                except Exception:
                    I_set = set()
                
                if I_set == {0}:
                    neg_q = False
                else:
                    neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]