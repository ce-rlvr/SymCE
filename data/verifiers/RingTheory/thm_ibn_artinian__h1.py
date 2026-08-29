import sympy
from sympy import QQ, ZZ

# Top-level setup: named object bindings that the witness expression may reference.
# Since SymPy primarily deals with commutative rings (which always have the IBN property),
# we define custom objects to represent well-known non-IBN rings.
class AbstractRing:
    def __init__(self, name, has_ibn):
        self.name = name
        self.has_ibn = has_ibn

    def __str__(self):
        return self.name

# Standard rings with IBN
Z = AbstractRing("Z", has_ibn=True)
Q = AbstractRing("Q", has_ibn=True)
R = AbstractRing("R", has_ibn=True)
C = AbstractRing("C", has_ibn=True)

# Well-known rings without IBN
End_V_inf = AbstractRing("Endomorphism ring of an infinite-dimensional vector space", has_ibn=False)
Column_finite_matrices = AbstractRing("Ring of column-finite infinite matrices", has_ibn=False)
Leavitt_algebra = AbstractRing("Leavitt algebra", has_ibn=False)
Cuntz_algebra = AbstractRing("Cuntz algebra", has_ibn=False)


def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a ring that does NOT have the Invariant Basis Number (IBN) property.
    """
    try:
        if hasattr(witness, 'has_ibn'):
            neg_q = not witness.has_ibn
        elif isinstance(witness, str):
            w = witness.lower()
            # Check for common keywords associated with non-IBN rings
            neg_q = any(kw in w for kw in [
                "end", "leavitt", "cuntz", "column-finite", 
                "row-finite", "infinite matrix", "infinite matrices", "b(h)"
            ])
        else:
            # Any standard SymPy ring (like ZZ, QQ, polynomial rings) is commutative and thus has IBN.
            # Finite matrix rings over commutative rings also have IBN.
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(neg_q)]


CONDITION_LABELS = [
    "¬Q: R does not have the Invariant Basis Number property"
]

N_HYP = 0
NEG_Q_INDEX = 0