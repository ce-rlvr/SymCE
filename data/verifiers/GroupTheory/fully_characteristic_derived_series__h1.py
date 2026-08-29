import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (G, n) or (G, n, H).
    """
    if isinstance(witness, (tuple, list)):
        if len(witness) == 2:
            G, n = witness
            H_given = None
        elif len(witness) == 3:
            G, n, H_given = witness
        else:
            return [False, False, False]
    else:
        return [False, False, False]

    # H_1: n is a non-negative integer
    try:
        h1 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and n >= 0
    except Exception:
        h1 = False

    # H_2: G^(n) is the n-th derived subgroup of G
    try:
        H = G
        for _ in range(int(n)):
            if callable(getattr(H, 'derived_subgroup', None)):
                H = H.derived_subgroup()
            else:
                H = H.derived_subgroup
                
        if H_given is not None:
            h2 = (H_given == H)
        else:
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: G^(n) is NOT a fully characteristic subgroup of G
    try:
        target_H = H_given if H_given is not None else H
        
        if hasattr(target_H, 'is_fully_characteristic'):
            try:
                is_fully_char = target_H.is_fully_characteristic(G)
            except TypeError:
                is_fully_char = target_H.is_fully_characteristic()
        elif hasattr(G, 'is_fully_characteristic'):
            is_fully_char = G.is_fully_characteristic(target_H)
        elif hasattr(G, 'endomorphisms'):
            is_fully_char = True
            for phi in G.endomorphisms():
                for g in target_H.generators:
                    if phi(g) not in target_H:
                        is_fully_char = False
                        break
                if not is_fully_char:
                    break
        else:
            # Mathematically, the derived series of any true group consists of fully characteristic subgroups.
            # If G is a standard group object, it will always be fully characteristic.
            # A valid counterexample must be a non-group structure (e.g. a mock object) where this fails.
            is_fully_char = True
            
        neg_q = not is_fully_char
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a non-negative integer",
    "H_2: G^(n) is the n-th derived subgroup of G",
    "¬Q: G^(n) is not a fully characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2