import sympy
from sympy import Matrix, ZZ, QQ
import itertools

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    "If R is a commutative ring with identity and P is a projective R-module, 
    then S^{-1}P is a projective S^{-1}R-module."
    
    The dropped hypothesis is that S must be a multiplicatively closed subset of R.
    Witness is expected to be a tuple: (R, M, S)
      - R: The ring (e.g., sympy.ZZ or a string like 'ZZ')
      - M: An idempotent sympy.Matrix representing the projective module P (as an image)
      - S: A subset of R (e.g., a list of elements)
    """
    try:
        R, M, S = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a commutative ring with identity
    try:
        h1 = False
        if R in [ZZ, QQ]:
            h1 = True
        elif isinstance(R, str) and R in ['ZZ', 'QQ', 'RR', 'CC', 'Z', 'Q', 'R', 'C']:
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative is not False:
            h1 = True
    except Exception:
        h1 = False

    # H_2: P is a projective R-module
    # A module is finitely generated projective iff it is the image of an idempotent matrix
    try:
        h2 = False
        if isinstance(M, Matrix):
            if M.shape[0] == M.shape[1]:
                if M * M == M:
                    h2 = True
    except Exception:
        h2 = False

    # ¬Q: S^{-1}P is not a projective S^{-1}R-module
    # This happens if S is not a valid multiplicatively closed subset containing 1,
    # meaning the standard localization S^{-1}R fails to form a proper ring.
    try:
        neg_q = False
        if not isinstance(S, (list, set, tuple, sympy.Set)):
            neg_q = True
        else:
            S_list = list(S)
            if len(S_list) == 0:
                neg_q = True
            else:
                has_one = False
                for s in S_list:
                    try:
                        if s == 1:
                            has_one = True
                            break
                    except Exception:
                        pass
                
                is_closed = True
                for a in S_list:
                    for b in S_list:
                        try:
                            prod = a * b
                            if prod not in S_list:
                                is_closed = False
                                break
                        except Exception:
                            is_closed = False
                            break
                    if not is_closed:
                        break
                
                if not (has_one and is_closed):
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: P is a projective R-module",
    "¬Q: S^{-1}P is not a projective S^{-1}R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2