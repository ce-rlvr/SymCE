import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    # 1. Dictionary-based witness
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("M_is_Artinian", False))
            h2 = bool(witness.get("N_is_submodule", False))
            neg_q = not bool(witness.get("N_is_Artinian", True))
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Object-based witness with attributes
    try:
        if hasattr(witness, "M_is_Artinian"):
            h1 = bool(getattr(witness, "M_is_Artinian", False))
            h2 = bool(getattr(witness, "N_is_submodule", False))
            neg_q = not bool(getattr(witness, "N_is_Artinian", True))
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Tuple-based witness (M, N)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            M, N = witness
            
            # Check H1: M is an Artinian R-module
            if hasattr(M, "is_artinian"):
                h1 = bool(M.is_artinian()) if callable(M.is_artinian) else bool(M.is_artinian)
            elif hasattr(M, "is_Artinian"):
                h1 = bool(M.is_Artinian()) if callable(M.is_Artinian) else bool(M.is_Artinian)
            elif hasattr(M, "is_abelian") and M.is_abelian and hasattr(M, "order") and M.order() < float('inf'):
                # Finite abelian groups are Artinian Z-modules
                h1 = True
                
            # Check H2: N is a submodule of M
            if hasattr(N, "is_submodule"):
                h2 = bool(N.is_submodule(M))
            elif hasattr(N, "is_subgroup"):
                h2 = bool(N.is_subgroup(M))
                
            # Check neg_Q: N is NOT an Artinian R-module
            n_art = True
            if hasattr(N, "is_artinian"):
                n_art = bool(N.is_artinian()) if callable(N.is_artinian) else bool(N.is_artinian)
            elif hasattr(N, "is_Artinian"):
                n_art = bool(N.is_Artinian()) if callable(N.is_Artinian) else bool(N.is_Artinian)
            elif hasattr(N, "is_abelian") and N.is_abelian and hasattr(N, "order") and N.order() < float('inf'):
                n_art = True
                
            neg_q = not n_art
            return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: M is an Artinian R-module",
    "H_2: N is a submodule of M",
    "¬Q: N is not an Artinian R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2