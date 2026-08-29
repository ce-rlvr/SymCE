import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, phi = witness
    except Exception:
        return [False, False, False, False]

    if callable(phi):
        phi_func = phi
    else:
        phi_func = lambda x: phi[x]

    # H1: G is a non-abelian group
    try:
        h1 = isinstance(G, PermutationGroup) and not G.is_abelian
    except Exception:
        h1 = False

    # H2: Z(G) is the center of G
    try:
        try:
            Z = G.center()
        except TypeError:
            Z = G.center
        h2 = isinstance(G, PermutationGroup) and isinstance(Z, PermutationGroup)
    except Exception:
        h2 = False

    # H3: For all x \in G \setminus Z(G), \phi(x) = x
    try:
        if not isinstance(G, PermutationGroup):
            h3 = False
        else:
            try:
                Z = G.center()
            except TypeError:
                Z = G.center
            Z_elems = set(Z.elements)
            h3 = True
            for x in G.elements:
                if x not in Z_elems:
                    if phi_func(x) != x:
                        h3 = False
                        break
    except Exception:
        h3 = False

    # neg_Q: \phi is NOT the identity automorphism on G
    try:
        if not isinstance(G, PermutationGroup):
            neg_q = False
        else:
            is_identity_automorphism = True
            
            # Check if it's the identity function
            for x in G.elements:
                if phi_func(x) != x:
                    is_identity_automorphism = False
                    break
            
            # Check if it's a homomorphism
            if is_identity_automorphism:
                for x in G.elements:
                    for y in G.elements:
                        if phi_func(x * y) != phi_func(x) * phi_func(y):
                            is_identity_automorphism = False
                            break
                    if not is_identity_automorphism:
                        break
            
            # Check if image is valid
            if is_identity_automorphism:
                for x in G.elements:
                    if phi_func(x) not in G.elements:
                        is_identity_automorphism = False
                        break
            
            # Check bijection
            if is_identity_automorphism:
                image_set = set()
                for x in G.elements:
                    image_set.add(phi_func(x))
                if len(image_set) != len(list(G.elements)):
                    is_identity_automorphism = False
            
            neg_q = not is_identity_automorphism
    except Exception:
        # If evaluating phi fails, it is not a valid identity automorphism
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a non-abelian group",
    "H_2: Z(G) is the center of G",
    "H_3: For all x \\in G \\setminus Z(G), \\phi(x) = x",
    "¬Q: \\phi is not the identity automorphism on G"
]

N_HYP = 3
NEG_Q_INDEX = 3