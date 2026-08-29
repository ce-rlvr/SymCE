import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def groups_equal(H1, H2):
    """Check if two permutation groups are equal by comparing their generators."""
    try:
        for g in H1.generators:
            if g not in H2:
                return False
        for g in H2.generators:
            if g not in H1:
                return False
        return True
    except Exception:
        return False

def is_normal_subgroup(H, G):
    """Check if H is a normal subgroup of G."""
    try:
        # Check if H is a subgroup of G
        for h in H.generators:
            if h not in G:
                return False
        # Check normality condition: g * h * g^-1 in H
        for g in G.generators:
            g_inv = g**-1
            for h in H.generators:
                if (g * h * g_inv) not in H:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # The witness can be just a group G, or a tuple (G, G')
    if isinstance(witness, tuple) and len(witness) == 2:
        G, G_prime_candidate = witness
    else:
        G = witness
        try:
            G_prime_candidate = G.derived_subgroup()
        except Exception:
            return [False, False]
            
    # H_1: G' is the commutator subgroup of G
    try:
        actual_G_prime = G.derived_subgroup()
        h1_ok = groups_equal(G_prime_candidate, actual_G_prime)
    except Exception:
        h1_ok = False
        
    # neg_Q: The quotient group G/G' is NOT an abelian group
    try:
        actual_G_prime = G.derived_subgroup()
        
        # For G/G' to be a well-defined abelian group, G' must be normal in G,
        # and G' must contain the commutator subgroup of G.
        is_normal = is_normal_subgroup(G_prime_candidate, G)
        
        contains_commutator = True
        for g in actual_G_prime.generators:
            if g not in G_prime_candidate:
                contains_commutator = False
                break
                
        is_abelian_quotient = is_normal and contains_commutator
        neg_q_ok = not is_abelian_quotient
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G' is the commutator subgroup of G",
    "¬Q: The quotient group G/G' is not an abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1