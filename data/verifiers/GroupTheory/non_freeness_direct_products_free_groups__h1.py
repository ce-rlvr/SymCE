import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    """
    Given a witness (F1, F2), check if it is a valid counterexample.
    The witness can be a tuple of SymPy groups or a tuple of integers representing the ranks of the free groups.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        
        F1, F2 = witness
        
        def is_free_group(G):
            if isinstance(G, int) or (hasattr(G, 'is_Integer') and G.is_Integer):
                return int(G) >= 0
            if type(G).__name__ == 'FreeGroup':
                return True
            try:
                if hasattr(G, 'order') and G.order() == 1:
                    return True
            except Exception:
                pass
            return False

        def free_group_rank(G):
            if isinstance(G, int) or (hasattr(G, 'is_Integer') and G.is_Integer):
                return int(G)
            if type(G).__name__ == 'FreeGroup':
                return len(G.generators)
            try:
                if hasattr(G, 'order') and G.order() == 1:
                    return 0
            except Exception:
                pass
            return None

        # H_1: F_2 is a non-trivial free group
        try:
            h1_ok = is_free_group(F2) and free_group_rank(F2) > 0
        except Exception:
            h1_ok = False
            
        # ¬Q: F_1 \times F_2 is a free group
        # The direct product of two groups is a free group if and only if 
        # both are free groups and at least one of them is the trivial group (rank 0).
        try:
            neg_q_ok = (is_free_group(F1) and is_free_group(F2) and 
                        (free_group_rank(F1) == 0 or free_group_rank(F2) == 0))
        except Exception:
            neg_q_ok = False
            
        return [bool(h1_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: F_2 is a non-trivial free group",
    "¬Q: F_1 \\times F_2 is a free group"
]

N_HYP = 1
NEG_Q_INDEX = 1
