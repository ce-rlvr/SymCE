import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup, Permutation
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    # Unpack witness if it's a tuple (G, e)
    if isinstance(witness, tuple):
        if len(witness) == 2:
            G, e_wit = witness
        elif len(witness) >= 1:
            G = witness[0]
            e_wit = witness[1] if len(witness) > 1 else None
        else:
            G = None
            e_wit = None
    else:
        G = witness
        e_wit = None

    # H_1: G is a group
    try:
        if hasattr(G, 'elements') and hasattr(G, 'identity'):
            is_group = True
            elements = list(G.elements)
            identity = G.identity
        elif isinstance(G, list) and len(G) > 0:
            is_group = True
            elements = G
            identity = None
            for x in elements:
                # Check if x acts as identity
                if all(x * y == y and y * x == y for y in elements):
                    identity = x
                    break
            if identity is None:
                is_group = False
        else:
            is_group = False
            elements = []
            identity = None
    except Exception:
        is_group = False
        elements = []
        identity = None

    # H_2: e is the identity element of G
    try:
        if e_wit is not None:
            e = e_wit
            e_is_identity = bool(e == identity)
        else:
            e = identity
            e_is_identity = True
    except Exception:
        e_is_identity = False
        e = None

    # ¬Q: The stabilizer of e in G x G is NOT the diagonal subgroup
    try:
        if not is_group or e is None:
            neg_Q = False
        else:
            stabilizer_is_delta = True
            for g in elements:
                for h in elements:
                    # Compute h^{-1}
                    try:
                        h_inv = h**-1
                    except Exception:
                        h_inv = h.inv()
                    
                    # Left-right multiplication action: (g, h) . x = g * x * h^{-1}
                    val = g * e * h_inv
                    
                    stabilizes = bool(val == e)
                    in_delta = bool(g == h)
                    
                    if stabilizes != in_delta:
                        stabilizer_is_delta = False
                        break
                if not stabilizer_is_delta:
                    break
            
            neg_Q = not stabilizer_is_delta
    except Exception:
        neg_Q = False

    return [is_group, e_is_identity, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: e is the identity element of G",
    "¬Q: The stabilizer of e in G x G is not the diagonal subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2