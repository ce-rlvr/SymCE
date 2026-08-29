import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: FG is the group algebra of G over F",
    "H_3: Z is the center of the group algebra FG",
    "¬Q: Class sums do not form a basis for the center"
]

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, G = witness
        else:
            G = witness
            
        class_names = [cls.__name__ for cls in G.__class__.__mro__]
        is_group = ('PermutationGroup' in class_names or 
                    'FpGroup' in class_names or 
                    'FreeGroup' in class_names or 
                    hasattr(G, 'generators'))
        h1 = is_group
        h2 = is_group
        h3 = is_group
    except Exception:
        h1 = False
        h2 = False
        h3 = False

    try:
        is_inf = False
        if hasattr(G, 'is_finite') and G.is_finite is not None:
            is_inf = not G.is_finite
        else:
            try:
                o = G.order() if callable(G.order) else G.order
                is_inf = (o == sympy.oo)
            except Exception:
                if type(G).__name__ == 'FreeGroup':
                    is_inf = True
                else:
                    is_inf = False

        is_ab = True
        if hasattr(G, 'is_abelian') and G.is_abelian is not None:
            is_ab = G.is_abelian
        else:
            if type(G).__name__ == 'FreeGroup':
                is_ab = len(G.generators) <= 1

        # The conclusion fails if G has an infinite conjugacy class.
        # In SymPy, infinite non-abelian groups (like FreeGroup with rank > 1) have infinite conjugacy classes.
        # For such groups, the class sums are infinite and do not belong to the group algebra.
        neg_q = is_inf and not is_ab
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]