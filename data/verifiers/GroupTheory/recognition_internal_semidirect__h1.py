import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4) # V4 is isomorphic to A4's Sylow 2-subgroup, but we can just use standard groups
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
    """
    Given a witness (G, N, H), checks the remaining hypotheses and the negated conclusion.
    """
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: Let N be a normal subgroup of G
    try:
        h1_ok = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h1_ok = False

    # H_2: Let H be a subgroup of G
    try:
        h2_ok = bool(H.is_subgroup(G))
    except Exception:
        h2_ok = False

    # H_3: G = NH
    try:
        # Check if the set of products nh covers G
        nh_elements = set()
        for n in N.elements:
            for h in H.elements:
                nh_elements.add(n * h)
        h3_ok = bool(nh_elements == set(G.elements))
    except Exception:
        h3_ok = False

    # H_4: N \cap H = {e}
    try:
        intersection = set(N.elements).intersection(set(H.elements))
        # The identity element is the only common element
        h4_ok = bool(len(intersection) == 1 and list(intersection)[0].is_Identity)
    except Exception:
        h4_ok = False

    # neg_Q: The group G is NOT isomorphic to the external semidirect product N \rtimes_\phi H
    try:
        # Mathematically, if H1-H4 hold, G is ALWAYS isomorphic to N \rtimes_\phi H 
        # where \phi is given by conjugation \phi(h)(n) = h * n * h^{-1}.
        # If the witness is a valid counterexample, it must be that G is not isomorphic.
        # We check if the map f(n, h) = n * h is an isomorphism.
        # If it is an isomorphism, then G IS isomorphic, so neg_Q is False.
        # If it is not, then neg_Q is True.
        
        is_homomorphism = True
        for n1 in N.elements:
            for h1 in H.elements:
                for n2 in N.elements:
                    for h2 in H.elements:
                        # \phi(h1)(n2) = h1 * n2 * h1^{-1}
                        phi_h1_n2 = h1 * n2 * (h1**-1)
                        # Product in semidirect product: (n1, h1) * (n2, h2) = (n1 * \phi(h1)(n2), h1 * h2)
                        prod_n = n1 * phi_h1_n2
                        prod_h = h1 * h2
                        
                        # Map f(n, h) = n * h
                        f_prod = prod_n * prod_h
                        f_1 = n1 * h1
                        f_2 = n2 * h2
                        
                        if f_prod != f_1 * f_2:
                            is_homomorphism = False
                            break
                    if not is_homomorphism:
                        break
                if not is_homomorphism:
                    break
            if not is_homomorphism:
                break
                
        # If f is a homomorphism, and since |G| = |N||H| (from H3 and H4), f is an isomorphism.
        # Thus G is isomorphic to the semidirect product, meaning the conclusion holds (neg_Q is False).
        # If f is not a homomorphism, the standard isomorphism fails.
        neg_q_ok = not is_homomorphism
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: H is a subgroup of G",
    "H_3: G = NH",
    "H_4: N \\cap H = \\{e\\}",
    "¬Q: G is not isomorphic to the external semidirect product N \\rtimes_\\phi H"
]

N_HYP = 4
NEG_Q_INDEX = 4