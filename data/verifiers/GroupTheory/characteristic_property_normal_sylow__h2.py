import itertools
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.homomorphisms import homomorphism
from sympy.ntheory import isprime, factorint

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
    # Parse witness
    try:
        if len(witness) == 3:
            G, P, p = witness
        elif len(witness) == 2:
            G, P = witness
            order_P = P.order()
            if order_P == 1:
                p = 2
                while G.order() % p == 0:
                    p += 1
            else:
                factors = factorint(order_P)
                if len(factors) == 1:
                    p = list(factors.keys())[0]
                else:
                    p = -1
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        if not isprime(p):
            h2 = False
        elif not isinstance(P, PermutationGroup):
            h2 = False
        elif not all(g in G for g in P.generators):
            h2 = False
        else:
            order_G = G.order()
            order_P = P.order()
            k = 0
            temp = order_P
            while temp % p == 0 and temp > 1:
                temp //= p
                k += 1
            if temp != 1:
                h2 = False
            else:
                if (order_G // order_P) % p == 0:
                    h2 = False
                else:
                    h2 = True
    except Exception:
        h2 = False

    # H_3: P is a normal subgroup of G
    try:
        h3 = True
        P_elements = set(P.elements)
        for g in G.generators:
            g_inv = ~g
            for h in P.generators:
                if g * h * g_inv not in P_elements:
                    h3 = False
                    break
            if not h3:
                break
    except Exception:
        h3 = False

    # neg_Q: P is NOT a characteristic subgroup of G
    try:
        if G.order() == 1:
            neg_q = False
        else:
            is_char = True
            gens = G.generators
            P_elements = set(P.elements)
            
            for images in itertools.product(list(G.elements), repeat=len(gens)):
                # Optimization: automorphisms must preserve the order of elements
                if any(images[i].order() != gens[i].order() for i in range(len(gens))):
                    continue
                
                H = PermutationGroup(*images)
                if H.order() != G.order():
                    continue
                    
                try:
                    phi = homomorphism(G, G, gens, list(images))
                    if phi is not None:
                        # Check if phi(P) == P
                        for p_gen in P.generators:
                            if phi(p_gen) not in P_elements:
                                is_char = False
                                break
                except Exception:
                    pass
                    
                if not is_char:
                    break
                    
            neg_q = not is_char
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: P is a normal subgroup of G",
    "¬Q: P is not a characteristic subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3