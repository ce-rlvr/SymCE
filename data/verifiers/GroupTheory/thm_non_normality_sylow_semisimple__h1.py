import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings that the witness expression may reference.
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, p, P = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a non-trivial semisimple group
    # A finite group is semisimple if it has no non-trivial abelian normal subgroups,
    # OR (in some contexts) if it is completely reducible (a direct product of simple groups).
    try:
        h1 = False
        if G.order() > 1:
            normals = G.normal_subgroups()
            
            # Check Definition 1: No non-trivial abelian normal subgroups
            has_abelian_normal = False
            for N in normals:
                if N.order() > 1 and N.is_abelian:
                    has_abelian_normal = True
                    break
            
            if not has_abelian_normal:
                h1 = True
            else:
                # Check Definition 2: Completely reducible (direct product of simple groups)
                # A group is completely reducible iff every normal subgroup has a normal complement.
                is_completely_reducible = True
                for N in normals:
                    has_complement = False
                    for M in normals:
                        if N.order() * M.order() == G.order():
                            # Check if intersection is trivial
                            if N.order() < M.order():
                                A, B = N, M
                            else:
                                A, B = M, N
                            
                            intersection_trivial = True
                            for g in A.generate():
                                if not g.is_Identity and g in B:
                                    intersection_trivial = False
                                    break
                            
                            if intersection_trivial:
                                has_complement = True
                                break
                    if not has_complement:
                        is_completely_reducible = False
                        break
                
                if is_completely_reducible:
                    h1 = True
    except Exception:
        h1 = False

    # H_2: p is a prime number dividing the order of G
    try:
        h2 = isprime(p) and (G.order() % p == 0)
    except Exception:
        h2 = False

    # H_3: P is a Sylow p-subgroup of G
    try:
        h3 = False
        # Check if P is a subgroup of G
        is_sub = True
        for g in P.generators:
            if g not in G:
                is_sub = False
                break
        
        if is_sub:
            order_G = G.order()
            order_P = P.order()
            count = 0
            temp = order_G
            while temp % p == 0:
                count += 1
                temp //= p
            
            if order_P == p**count:
                h3 = True
    except Exception:
        h3 = False

    # ¬Q: P is a normal subgroup of G
    try:
        neg_q = False
        if h3:
            is_normal = True
            for g in G.generators:
                g_inv = ~g
                for x in P.generators:
                    conj = g * x * g_inv
                    if conj not in P:
                        is_normal = False
                        break
                if not is_normal:
                    break
            neg_q = is_normal
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a non-trivial semisimple group",
    "H_2: p is a prime number dividing the order of G",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: P is a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3