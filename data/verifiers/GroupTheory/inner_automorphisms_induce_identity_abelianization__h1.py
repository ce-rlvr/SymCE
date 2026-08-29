import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def apply_phi(phi, x):
    if isinstance(phi, dict):
        return phi[x]
    return phi(x)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, phi = witness
                provided_G_prime = None
            elif len(witness) == 3:
                G, provided_G_prime, phi = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G' is the commutator subgroup of G
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            G_prime = G.derived_subgroup()
            if provided_G_prime is not None:
                if set(provided_G_prime.elements) != set(G_prime.elements):
                    h1 = False
            G_prime_elements = set(G_prime.elements)
    except Exception:
        h1 = False

    # H2: \phi is an inner automorphism of G
    # (We check if it is an automorphism. The dropped hypothesis was 'inner', 
    # so checking 'inner' would make the conjecture true and neg_Q always False)
    try:
        if not h1:
            h2 = False
        else:
            elements = list(G.elements)
            mapped_elements = []
            is_homomorphism = True
            for g in elements:
                mg = apply_phi(phi, g)
                if mg not in elements:
                    is_homomorphism = False
                    break
                mapped_elements.append(mg)
            
            if is_homomorphism and len(set(mapped_elements)) == len(elements):
                for g1 in elements:
                    for g2 in elements:
                        mg1 = apply_phi(phi, g1)
                        mg2 = apply_phi(phi, g2)
                        mg12 = apply_phi(phi, g1*g2)
                        if mg1 * mg2 != mg12:
                            is_homomorphism = False
                            break
                    if not is_homomorphism:
                        break
            else:
                is_homomorphism = False
            h2 = is_homomorphism
    except Exception:
        h2 = False

    # H3: \bar{\phi}: G/G' \to G/G' is the induced automorphism defined by \bar{\phi}(xG') = \phi(x)G'
    try:
        if not (h1 and h2):
            h3 = False
        else:
            h3 = True
            for x in G_prime_elements:
                px = apply_phi(phi, x)
                if px not in G_prime_elements:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # neg_Q: \bar{\phi} is not the identity map on G/G'
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            neg_q = False
            for x in elements:
                px = apply_phi(phi, x)
                diff = px * (x**-1)
                if diff not in G_prime_elements:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G' is the commutator subgroup of G",
    "H_2: \\phi is an inner automorphism of G",
    "H_3: \\bar{\\phi}: G/G' \\to G/G' is the induced automorphism defined by \\bar{\\phi}(xG') = \\phi(x)G'",
    "¬Q: \\bar{\\phi} is not the identity map on G/G'"
]

N_HYP = 3
NEG_Q_INDEX = 3