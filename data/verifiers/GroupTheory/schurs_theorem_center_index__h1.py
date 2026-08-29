import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: The center Z(G) has finite index in G",
    "¬Q: The commutator subgroup G' is not a finite group"
]

N_HYP = 1
NEG_Q_INDEX = 1

def is_finite_group(G):
    try:
        if hasattr(G, 'is_finite'):
            val = G.is_finite() if callable(G.is_finite) else G.is_finite
            if val is not None:
                return bool(val)
    except Exception:
        pass
    try:
        if hasattr(G, 'order'):
            o = G.order() if callable(G.order) else G.order
            from sympy import oo
            if o != oo and o != float('inf'):
                return True
            else:
                return False
    except Exception:
        pass
    return False

def conditions(witness):
    # H1: Z(G) has finite index in G
    h1 = False
    try:
        if hasattr(witness, 'Z_index_finite'):
            h1 = bool(witness.Z_index_finite() if callable(witness.Z_index_finite) else witness.Z_index_finite)
        elif is_finite_group(witness):
            h1 = True
        else:
            if hasattr(witness, 'center_index'):
                idx = witness.center_index() if callable(witness.center_index) else witness.center_index
                from sympy import oo
                h1 = (idx != oo and idx != float('inf'))
            elif hasattr(witness, 'center') and hasattr(witness, 'index'):
                Z = witness.center() if callable(witness.center) else witness.center
                idx = witness.index(Z)
                from sympy import oo
                h1 = (idx != oo and idx != float('inf'))
    except Exception:
        h1 = False

    # neg_Q: G' is NOT a finite group
    neg_q = False
    try:
        if hasattr(witness, 'G_prime_finite'):
            is_fin = bool(witness.G_prime_finite() if callable(witness.G_prime_finite) else witness.G_prime_finite)
            neg_q = not is_fin
        elif is_finite_group(witness):
            neg_q = False
        else:
            D = None
            if hasattr(witness, 'derived_subgroup'):
                D = witness.derived_subgroup() if callable(witness.derived_subgroup) else witness.derived_subgroup
            elif hasattr(witness, 'commutator_subgroup'):
                D = witness.commutator_subgroup() if callable(witness.commutator_subgroup) else witness.commutator_subgroup
            
            if D is not None:
                neg_q = not is_finite_group(D)
    except Exception:
        neg_q = False

    return [h1, neg_q]