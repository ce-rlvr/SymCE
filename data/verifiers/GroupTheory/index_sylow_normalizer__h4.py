import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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

def conditions(witness):
    try:
        G, p, P = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() < float('inf')
    except Exception:
        h1 = False

    # H2: p is a prime number dividing the order of G
    try:
        h2 = isprime(p) and (G.order() % p == 0)
    except Exception:
        h2 = False

    # H3: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            h3 = False
        else:
            # Check if P is a subgroup of G
            is_sub = all(G.contains(gen) for gen in P.generators)
            if not is_sub:
                h3 = False
            else:
                # Check if the order of P is the highest power of p dividing |G|
                order_G = G.order()
                order_P = P.order()
                k = 0
                temp = order_G
                while temp % p == 0 and temp > 0:
                    k += 1
                    temp //= p
                h3 = (order_P == p**k)
    except Exception:
        h3 = False

    # neg_Q: The index of the normalizer N_G(P) in G is NOT equal to n_p
    try:
        G_gens = G.generators
        
        # Compute the index of N_G(P) in G by finding the size of the conjugacy class of P
        P_elements = frozenset(P.generate())
        orbit_set = {P_elements}
        queue = [P_elements]
        while queue:
            curr = queue.pop(0)
            for g in G_gens:
                conj = frozenset(g * x * ~g for x in curr)
                if conj not in orbit_set:
                    orbit_set.add(conj)
                    queue.append(conj)
        index_N_G_P = len(orbit_set)

        # Compute n_p (the number of Sylow p-subgroups of G)
        S = G.sylow_subgroup(p)
        S_elements = frozenset(S.generate())
        S_orbit_set = {S_elements}
        queue_S = [S_elements]
        while queue_S:
            curr = queue_S.pop(0)
            for g in G_gens:
                conj = frozenset(g * x * ~g for x in curr)
                if conj not in S_orbit_set:
                    S_orbit_set.add(conj)
                    queue_S.append(conj)
        n_p = len(S_orbit_set)

        neg_q = (index_N_G_P != n_p)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number dividing the order of G",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: The index of the normalizer N_G(P) in G is not equal to n_p"
]

N_HYP = 3
NEG_Q_INDEX = 3