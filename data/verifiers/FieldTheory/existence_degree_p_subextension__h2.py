import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import isprime

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
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            p = witness.get('p')
        else:
            G, H, p = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F is a field (witness is a valid field extension model)
    try:
        if not (isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)):
            h1 = False
        else:
            h1 = all(g in G for g in H.generators)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False

    # H_3: The Galois group Gal(E/F) is a p-group of order p^n for some integer n >= 1
    try:
        if not h1:
            h3 = False
        else:
            N_G_H_order = 0
            for g in G.generate():
                normalizes = True
                for h in H.generators:
                    if (g * h * ~g) not in H:
                        normalizes = False
                        break
                if normalizes:
                    N_G_H_order += 1
            
            order_H = H.order()
            if N_G_H_order % order_H != 0:
                h3 = False
            else:
                index = N_G_H_order // order_H
                if index > 1:
                    temp = index
                    while temp % p == 0:
                        temp //= p
                    h3 = (temp == 1)
                else:
                    h3 = False
    except Exception:
        h3 = False

    # neg_Q: There does not exist an intermediate field K between F and E such that K/F is a Galois extension of degree p
    try:
        if not h1:
            neg_q = False
        else:
            try:
                G_prime = G.derived_subgroup()
            except AttributeError:
                comms = set()
                elements = list(G.generate())
                for g1 in elements:
                    for g2 in elements:
                        comms.add(g1 * g2 * ~g1 * ~g2)
                G_prime = PermutationGroup(list(comms))
            
            gens_K = list(H.generators) + list(G_prime.generators)
            if not gens_K:
                for elem in G.generate():
                    id_elem = elem * ~elem
                    break
                gens_K = [id_elem]
            K = PermutationGroup(gens_K)
            K_order = K.order()
            
            G_order = G.order()
            if G_order % K_order != 0:
                neg_q = False
            else:
                index_K = G_order // K_order
                neg_q = (index_K % p != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: p is a prime number",
    "H_3: The Galois group Gal(E/F) is a p-group of order p^n for some integer n >= 1",
    "¬Q: There does not exist an intermediate field K between F and E such that K/F is a Galois extension of degree p"
]

N_HYP = 3
NEG_Q_INDEX = 3