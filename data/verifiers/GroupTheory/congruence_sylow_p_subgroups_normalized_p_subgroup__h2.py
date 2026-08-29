import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.combinatorics.named_groups import AbelianGroup
from sympy.ntheory import isprime, factorint

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
        G, Q, p = witness
    except Exception:
        return [False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: Q is a p-subgroup of G
    try:
        if not isprime(p):
            h2 = False
        else:
            if isinstance(Q, PermutationGroup):
                gens_in_G = True
                degree = G.degree
                for gen in Q.generators:
                    arr = gen.array_form
                    if len(arr) < degree:
                        arr = arr + list(range(len(arr), degree))
                    elif len(arr) > degree:
                        if any(arr[i] != i for i in range(degree, len(arr))):
                            gens_in_G = False
                            break
                        arr = arr[:degree]
                    padded_gen = Permutation(arr)
                    if padded_gen not in G:
                        gens_in_G = False
                        break
                if not gens_in_G:
                    h2 = False
                else:
                    try:
                        order_Q = Q.order()
                    except TypeError:
                        order_Q = Q.order
                        
                    if order_Q == 1:
                        h2 = True
                    else:
                        factors = factorint(order_Q)
                        h2 = (list(factors.keys()) == [p])
            else:
                h2 = False
    except Exception:
        h2 = False

    # neg_Q: The number of Sylow p-subgroups of G that contain Q is NOT congruent to 1 mod p
    try:
        if not isprime(p):
            neg_q = False
        else:
            P = G.sylow_subgroup(p)
            P_elements = frozenset(P.generate())
            sylows = {P_elements}
            queue = [P_elements]
            G_gens = G.generators
            
            while queue:
                curr = queue.pop(0)
                for g in G_gens:
                    g_inv = ~g
                    conj = frozenset({g * x * g_inv for x in curr})
                    if conj not in sylows:
                        sylows.add(conj)
                        queue.append(conj)
                        
            degree = G.degree
            Q_gens_padded = []
            for gen in Q.generators:
                arr = gen.array_form
                if len(arr) < degree:
                    arr = arr + list(range(len(arr), degree))
                elif len(arr) > degree:
                    arr = arr[:degree]
                Q_gens_padded.append(Permutation(arr))
                
            count = 0
            for S in sylows:
                if all(q in S for q in Q_gens_padded):
                    count += 1
                    
            neg_q = (count % p != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: Q is a p-subgroup of G",
    "¬Q: The number of Sylow p-subgroups of G that contain Q is not congruent to 1 mod p"
]

N_HYP = 2
NEG_Q_INDEX = 2