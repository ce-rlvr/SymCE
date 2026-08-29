import math
from sympy.ntheory import isprime
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, p, Q), checks if it is a valid counterexample to the false conjecture.
    """
    try:
        G, p, Q = witness
    except Exception:
        return [False, False, False]

    # H_1: p is a prime number
    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    # H_2: Q is a p-subgroup of G
    try:
        h2_ok = False
        if Q.is_subgroup(G):
            order = Q.order()
            if order > 0:
                # Check if order is a power of p
                k = int(round(math.log(order, p)))
                if p**k == order:
                    h2_ok = True
    except Exception:
        h2_ok = False

    # neg_Q: The number of Sylow p-subgroups of G that contain Q is NOT congruent to 1 (mod p)
    try:
        neg_q_ok = False
        if G.order() % p == 0:
            # Find one Sylow p-subgroup
            P = G.sylow_subgroup(p)
            syls = []
            # Find all Sylow p-subgroups by conjugating P
            for g in G.elements:
                gens = [g * gen * ~g for gen in P.generators]
                P_conj = PermutationGroup(gens)
                if P_conj not in syls:
                    syls.append(P_conj)
            
            # Count how many contain Q
            count = 0
            for S in syls:
                if Q.is_subgroup(S):
                    count += 1
            
            if count % p != 1:
                neg_q_ok = True
        else:
            # If p does not divide |G|, the only Sylow p-subgroup is the trivial group
            # Q must be the trivial group, so it is contained in the 1 Sylow p-subgroup.
            # 1 = 1 mod p, so neg_Q is False.
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: Q is a p-subgroup of G",
    "¬Q: The number of Sylow p-subgroups of G that contain Q is not congruent to 1 (mod p)"
]

N_HYP = 2
NEG_Q_INDEX = 2