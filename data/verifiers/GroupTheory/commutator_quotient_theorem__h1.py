import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_subgroup(H, G):
    try:
        for h in H.generators:
            if h not in G:
                return False
        return True
    except Exception:
        return False

def is_normal_subgroup(G, N):
    try:
        if not is_subgroup(N, G):
            return False
        for g in G.generators:
            for n in N.generators:
                if (g**-1 * n * g) not in N:
                    return False
        return True
    except Exception:
        return False

def quotient_is_abelian(G, N):
    try:
        for g1 in G.generators:
            for g2 in G.generators:
                if (g1**-1 * g2**-1 * g1 * g2) not in N:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            if G is None or N is None:
                return [False, False, False]
            if 'G_prime' in witness:
                G_prime = witness['G_prime']
                actual_G_prime = G.derived_subgroup()
                h2_ok = is_subgroup(G_prime, actual_G_prime) and is_subgroup(actual_G_prime, G_prime)
            else:
                G_prime = G.derived_subgroup()
                h2_ok = True
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                G, N = witness
                G_prime = G.derived_subgroup()
                h2_ok = True
            elif len(witness) == 3:
                G, N, G_prime = witness
                actual_G_prime = G.derived_subgroup()
                h2_ok = is_subgroup(G_prime, actual_G_prime) and is_subgroup(actual_G_prime, G_prime)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1_ok = is_normal_subgroup(G, N)
    except Exception:
        h1_ok = False

    try:
        q_abelian = quotient_is_abelian(G, N)
        g_prime_in_n = is_subgroup(G_prime, N)
        # The conclusion is "G/N is abelian iff G' <= N"
        # The negation is the XOR of the two sides
        neg_q_ok = (q_abelian != g_prime_in_n)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: G' is the commutator subgroup of G",
    "¬Q: G/N is abelian XOR G' <= N"
]

N_HYP = 2
NEG_Q_INDEX = 2