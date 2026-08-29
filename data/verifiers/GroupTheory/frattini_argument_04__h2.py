from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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
    try:
        G, H, P, p = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = isinstance(G, PermutationGroup) and G.order() > 0 and isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h1_ok = False

    try:
        if not isprime(p):
            h2_ok = False
        elif not isinstance(P, PermutationGroup) or not P.is_subgroup(H):
            h2_ok = False
        else:
            order_H = H.order()
            order_P = P.order()
            expected_p_power = 1
            temp = order_H
            while temp % p == 0:
                expected_p_power *= p
                temp //= p
            h2_ok = (order_P == expected_p_power)
    except Exception:
        h2_ok = False

    try:
        P_elems = set(P.generate())
        N_G_P_elems = []
        for g in G.generate():
            normalizes = True
            for p_gen in P.generators:
                if (g * p_gen * (~g)) not in P_elems:
                    normalizes = False
                    break
            if normalizes:
                N_G_P_elems.append(g)
        
        HN_set = set()
        for h in H.generate():
            for n in N_G_P_elems:
                HN_set.add(h * n)
                
        neg_q_ok = len(HN_set) != G.order()
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of H",
    "¬Q: G != H N_G(P)"
]

N_HYP = 2
NEG_Q_INDEX = 2