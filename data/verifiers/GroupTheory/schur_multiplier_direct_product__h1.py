import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "The Schur multiplier M(G x H) is isomorphic to M(G) x M(H) x (G_ab ⊗ H_ab)"
    
    The formula holds if at least one of G_ab or H_ab is finite.
    It fails (meaning neg_Q is True) if and only if BOTH G_ab and H_ab are infinite
    (i.e., they both have a free abelian component).
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False]
        
        G, H = witness
        
        def is_inf_ab(grp):
            if grp is sympy.S.Integers or grp is sympy.ZZ:
                return True
            if hasattr(grp, 'abelian_invariants'):
                invs = grp.abelian_invariants()
                return 0 in invs
            if isinstance(grp, (list, tuple)):
                return 0 in grp
            if isinstance(grp, str):
                s = grp.strip().upper()
                s = s.replace('*', ' ').replace('X', ' ').replace('+', ' ')
                parts = s.split()
                return 'Z' in parts or 'INTEGERS' in parts
            if isinstance(grp, sympy.Symbol):
                return str(grp).upper() == 'Z'
            return False
            
        neg_q = is_inf_ab(G) and is_inf_ab(H)
        return [bool(neg_q)]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: M(G x H) is not isomorphic to M(G) x M(H) x (G_ab ⊗ H_ab)"
]

N_HYP = 0
NEG_Q_INDEX = 0