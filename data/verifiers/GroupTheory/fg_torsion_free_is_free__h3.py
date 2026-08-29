import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy import eye, zeros, oo

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    # H1: G is a finitely generated group
    try:
        h1 = hasattr(witness, 'generators') and len(list(witness.generators)) >= 0
    except Exception:
        h1 = False

    # H2: G is an abelian group
    try:
        h2 = bool(getattr(witness, 'is_abelian', False))
    except Exception:
        h2 = False

    # neg_Q: G is not a free abelian group
    try:
        is_free_abelian = False
        if h2:
            if hasattr(witness, 'order'):
                try:
                    ord_G = witness.order() if callable(witness.order) else witness.order
                except Exception:
                    ord_G = witness.order
                
                if ord_G == oo:
                    # For infinite abelian groups, it is free abelian iff it is torsion-free.
                    # We check if any generator has finite order (torsion).
                    is_free_abelian = True
                    if hasattr(witness, 'generators'):
                        for g in witness.generators:
                            try:
                                g_ord = g.order() if callable(g.order) else g.order
                                if g_ord != oo:
                                    is_free_abelian = False
                                    break
                            except Exception:
                                pass
                else:
                    # For finite abelian groups, it is free abelian iff it is the trivial group.
                    is_free_abelian = (int(ord_G) == 1)
        
        neg_q = not is_free_abelian
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "H_2: G is an abelian group",
    "¬Q: G is not a free abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2