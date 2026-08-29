import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import sympy.ntheory

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            p = witness.get('p')
            P = witness.get('P')
        else:
            G, N, p, P = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if isinstance(N, PermutationGroup) and isinstance(G, PermutationGroup):
            is_sub = True
            for gen in N.generators:
                if gen not in G:
                    is_sub = False
                    break
            if is_sub:
                is_norm = True
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * ~g) not in N:
                            is_norm = False
                            break
                        if (~g * n * g) not in N:
                            is_norm = False
                            break
                    if not is_norm:
                        break
                h2 = is_norm
    except Exception:
        h2 = False

    # H_3: p is a prime number
    try:
        h3 = sympy.ntheory.isprime(p)
    except Exception:
        h3 = False

    # ¬Q: G is not the product of N and the normalizer of P in G (G != N * N_G(P))
    try:
        neg_q = False
        if isinstance(P, PermutationGroup) and isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            # Find the normalizer of P in G: N_G(P)
            N_G_P = []
            for g in G.elements:
                is_norm = True
                for x in P.generators:
                    if (g * x * ~g) not in P:
                        is_norm = False
                        break
                if is_norm:
                    N_G_P.append(g)
            
            # Compute the set of elements in the product N * N_G(P)
            prod_set = set()
            deg = max(G.degree, N.degree, P.degree)
            for n in N.elements:
                for m in N_G_P:
                    p_prod = n * m
                    arr = p_prod.array_form
                    # Pad array form to ensure consistent hashing for permutations of the same action
                    if len(arr) < deg:
                        arr = arr + list(range(len(arr), deg))
                    prod_set.add(tuple(arr))
            
            # If the size of the product set is not equal to the order of G, then G != N * N_G(P)
            neg_q = len(prod_set) != G.order()
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: p is a prime number",
    "¬Q: G is not the product of N and the normalizer of P in G (G != N * N_G(P))"
]

N_HYP = 3
NEG_Q_INDEX = 3