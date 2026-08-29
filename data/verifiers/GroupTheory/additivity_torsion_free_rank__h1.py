import sympy
from sympy import eye, zeros, Tuple, diag
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.group_constructs import DirectProduct

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

def get_torsion_free_rank(obj):
    """Attempt to extract or compute the torsion-free rank of an object."""
    if hasattr(obj, 'torsion_free_rank'):
        attr = obj.torsion_free_rank
        return attr() if callable(attr) else attr
    if hasattr(obj, 'abelian_invariants'):
        invs = obj.abelian_invariants()
        return invs.count(0)
    if hasattr(obj, 'betti_number'):
        attr = obj.betti_number
        return attr() if callable(attr) else attr
    if hasattr(obj, 'free_rank'):
        attr = obj.free_rank
        return attr() if callable(attr) else attr
    if hasattr(obj, 'rank'):
        attr = obj.rank
        return attr() if callable(attr) else attr
    if hasattr(obj, 'cols') and hasattr(obj, 'rank'):
        # For presentation matrices of modules
        return obj.cols - obj.rank()
    if isinstance(obj, (list, tuple, Tuple)):
        # For lists of invariant factors
        return list(obj).count(0)
    if isinstance(obj, dict) and 'torsion_free_rank' in obj:
        return obj['torsion_free_rank']
    if isinstance(obj, (int, float)):
        # If the object is already the rank itself
        return obj
    if hasattr(obj, 'is_Integer') and obj.is_Integer:
        return int(obj)
    raise ValueError(f"Cannot determine torsion-free rank for {obj}")

def get_direct_sum(A, B):
    """Attempt to compute the direct sum of A and B."""
    if hasattr(A, 'direct_sum'):
        return A.direct_sum(B)
    if hasattr(A, 'oplus'):
        return A.oplus(B)
    if hasattr(A, 'col_join') and hasattr(B, 'col_join'):
        return diag(A, B)
    try:
        return DirectProduct(A, B)
    except Exception:
        pass
    try:
        return A + B
    except Exception:
        pass
    try:
        return A * B
    except Exception:
        pass
    raise ValueError("Cannot compute direct sum")

def conditions(witness) -> list[bool]:
    try:
        # Unpack the witness
        if isinstance(witness, dict):
            A = witness['A']
            B = witness['B']
            A_oplus_B = witness.get('A_oplus_B', get_direct_sum(A, B))
        elif isinstance(witness, (tuple, list, Tuple)):
            if len(witness) == 3:
                A, B, A_oplus_B = witness
            elif len(witness) == 2:
                A, B = witness
                A_oplus_B = get_direct_sum(A, B)
            else:
                return [False]
        else:
            A = witness.A
            B = witness.B
            A_oplus_B = getattr(witness, 'A_oplus_B', get_direct_sum(A, B))
            
        # Compute ranks
        rA = get_torsion_free_rank(A)
        rB = get_torsion_free_rank(B)
        rAB = get_torsion_free_rank(A_oplus_B)
        
        if rA is None or rB is None or rAB is None:
            return [False]
            
        # The conclusion is that rank(A ⊕ B) == rank(A) + rank(B).
        # We want the negation of the conclusion (i.e., it fails).
        neg_Q = (rAB != rA + rB)
        
        return [bool(neg_Q)]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The torsion-free rank of the direct sum A ⊕ B is not equal to the sum of the torsion-free rank of A and the torsion-free rank of B"
]

N_HYP = 0
NEG_Q_INDEX = 0