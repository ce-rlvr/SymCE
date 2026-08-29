import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            G, G_prime, phi = witness
        elif len(witness) == 2:
            G, phi = witness
            G_prime = G.derived_subgroup()
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: G' is the commutator subgroup of G
    try:
        derived = G.derived_subgroup()
        if hasattr(G_prime, 'elements'):
            g_prime_elems = set(G_prime.elements)
        else:
            g_prime_elems = set(G_prime)
        h1 = (g_prime_elems == set(derived.elements))
    except Exception:
        h1 = False

    # H2: phi is an automorphism of G
    try:
        g_elems = list(G.elements)
        if callable(phi):
            phi_dict = {x: phi(x) for x in g_elems}
        else:
            phi_dict = phi
            
        h2 = True
        if set(phi_dict.keys()) != set(g_elems):
            h2 = False
        elif set(phi_dict.values()) != set(g_elems):
            h2 = False
        else:
            for a in g_elems:
                for b in g_elems:
                    if phi_dict[a * b] != phi_dict[a] * phi_dict[b]:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # neg_Q: phi(G') != G'
    try:
        if hasattr(G_prime, 'elements'):
            g_prime_elems = set(G_prime.elements)
        else:
            g_prime_elems = set(G_prime)
            
        if callable(phi):
            mapped_g_prime = {phi(x) for x in g_prime_elems}
        else:
            mapped_g_prime = {phi[x] for x in g_prime_elems}
            
        neg_q = (mapped_g_prime != g_prime_elems)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G' is the commutator subgroup of G",
    "H_2: phi is an automorphism of G",
    "¬Q: phi(G') != G'"
]

N_HYP = 2
NEG_Q_INDEX = 2