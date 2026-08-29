import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y

# Top-level setup
Z = ZZ
Q = QQ

def conditions(witness):
    """
    Checks the conditions for the conjecture:
    Hypotheses:
      - R is a principal ideal domain.
      - S is a subring of K.
      - R is contained in S.
    Conclusion:
      - S is a principal ideal domain.
      
    The witness is expected to be a tuple of SymPy domains: (R, S, K).
    Example of a valid counterexample witness: (ZZ, ZZ[x], QQ[x])
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
            K = witness.get('K')
        else:
            R, S, K = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: R is a principal ideal domain
    try:
        h1 = bool(R.is_PID)
    except Exception:
        h1 = False
        
    # H_2: S is a subring of K
    # In SymPy domains, S is a subring of K if unifying S and K yields K.
    try:
        h2 = bool(S.unify(K) == K)
    except Exception:
        h2 = False
        
    # H_3: R is contained in S
    try:
        h3 = bool(R.unify(S) == S)
    except Exception:
        h3 = False
        
    # ¬Q: S is NOT a principal ideal domain
    try:
        neg_q = not bool(S.is_PID)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: S is a subring of K",
    "H_3: R is contained in S",
    "¬Q: S is not a principal ideal domain"
]

N_HYP = 3
NEG_Q_INDEX = 3