import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    try:
        G, g = witness
    except Exception:
        return [False, False]

    # H_1: g is an element of G
    try:
        h1_ok = bool(g in G)
    except Exception:
        h1_ok = False

    # ¬Q: g raised to the power of the order of G is NOT equal to the identity element of G
    try:
        try:
            # Determine the order of G
            if hasattr(G, 'order'):
                order = G.order() if callable(G.order) else G.order
            elif hasattr(G, '__len__'):
                order = len(G)
            else:
                order = sympy.oo
                
            # Determine the identity element of G
            if hasattr(G, 'identity'):
                identity = G.identity
            elif hasattr(G, 'id'):
                identity = G.id
            elif hasattr(G, 'identity_element'):
                identity = G.identity_element
            else:
                try:
                    identity = g ** 0
                except Exception:
                    identity = None

            # Evaluate the conclusion: g ** |G| == e
            if order in (sympy.oo, float('inf')) or order is None:
                # If the group is infinite, exponentiation by group order is undefined/false
                conclusion = False
            else:
                if identity is None:
                    conclusion = False
                else:
                    conclusion = bool((g ** order) == identity)
        except Exception:
            # If evaluation fails (e.g., undefined operation), the conclusion is false
            conclusion = False
            
        neg_q_ok = not conclusion
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: g is an element of G",
    "¬Q: g raised to the power of the order of G is not equal to the identity element of G"
]

N_HYP = 1
NEG_Q_INDEX = 1