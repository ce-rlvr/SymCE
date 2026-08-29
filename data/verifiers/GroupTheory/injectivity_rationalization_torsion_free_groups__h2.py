import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    # 1. Matrix witness (implicit domain R^n, which is an abelian torsion-free group)
    try:
        if hasattr(witness, 'nullspace') and callable(witness.nullspace):
            h1 = True
            is_torsion_free = True
            is_injective = (len(witness.nullspace()) == 0)
            q = (is_injective == is_torsion_free)
            return [h1, not q]
    except Exception:
        pass

    # 2. Tuple (G, phi) or Homomorphism phi
    try:
        if isinstance(witness, tuple):
            G, phi = witness
        else:
            phi = witness
            G = phi.domain
            
        h1 = bool(G.is_abelian)
    except Exception:
        h1 = False

    try:
        is_torsion_free = False
        if hasattr(G, 'order'):
            order = G.order()
            if order == 1:
                is_torsion_free = True
            elif order == sympy.oo:
                if hasattr(G, 'relators') and len(G.relators) == 0:
                    is_torsion_free = True
                elif G.__class__.__name__ == 'FreeGroup':
                    is_torsion_free = True

        if isinstance(phi, dict):
            vals = list(phi.values())
            unique_vals = []
            for v in vals:
                if v not in unique_vals:
                    unique_vals.append(v)
            is_injective = (len(unique_vals) == len(vals))
        elif hasattr(phi, 'nullspace') and callable(phi.nullspace):
            is_injective = (len(phi.nullspace()) == 0)
        elif callable(getattr(phi, 'is_injective', None)):
            is_injective = bool(phi.is_injective())
        else:
            is_injective = bool(phi.is_injective)

        q = (is_injective == is_torsion_free)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "¬Q: The homomorphism phi is NOT (injective iff G is torsion-free)"
]

N_HYP = 1
NEG_Q_INDEX = 1