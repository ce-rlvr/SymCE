import sympy
from sympy.combinatorics import PermutationGroup
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

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is expected to provide a group G and a homomorphism phi.
    It can be a tuple (G, phi), (phi, G), or just phi if phi has a .domain attribute.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], PermutationGroup):
                G, phi = witness
            elif isinstance(witness[1], PermutationGroup):
                phi, G = witness
            else:
                G, phi = witness
        elif hasattr(witness, 'domain'):
            phi = witness
            G = phi.domain
        else:
            G = witness
            phi = None
    except Exception:
        G = None
        phi = None

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # neg_Q: The kernel of phi is not the center of G
    try:
        if phi is None or not h1:
            neg_q = False
        else:
            if hasattr(phi, 'kernel'):
                ker = phi.kernel()
                ker_elems = set(ker.elements)
            elif isinstance(phi, dict):
                id_img = phi[G.identity]
                ker_elems = {g for g in G.elements if phi.get(g) == id_img}
            elif callable(phi):
                id_img = phi(G.identity)
                ker_elems = {g for g in G.elements if phi(g) == id_img}
            else:
                ker_elems = None
            
            if ker_elems is not None:
                center_elems = set(G.center().elements)
                neg_q = ker_elems != center_elems
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The kernel of phi is not the center of G"
]

N_HYP = 1
NEG_Q_INDEX = 1