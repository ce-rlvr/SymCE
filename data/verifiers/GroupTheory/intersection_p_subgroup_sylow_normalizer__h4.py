import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (G, p, P, H)
    """
    try:
        G, p, P, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group (and H is a subgroup of G)
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: P is a Sylow p-subgroup of G
    try:
        if not (isinstance(P, PermutationGroup) and P.is_subgroup(G)):
            h3 = False
        else:
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

    # ¬Q: H \cap N_G(P) != H \cap P
    try:
        # Compute the normalizer N_G(P)
        N_G_P_elements = []
        for g in G.generate():
            is_norm = True
            for p_gen in P.generators:
                if (g * p_gen * (~g)) not in P:
                    is_norm = False
                    break
            if is_norm:
                N_G_P_elements.append(g)
        
        N_G_P = PermutationGroup(N_G_P_elements)
        
        # Compute the order of H \cap N_G(P)
        count_N = 0
        for h_elem in H.generate():
            if h_elem in N_G_P:
                count_N += 1
                
        # Compute the order of H \cap P
        count_P = 0
        for h_elem in H.generate():
            if h_elem in P:
                count_P += 1
                
        # Since H \cap P is a subgroup of H \cap N_G(P), 
        # they are equal if and only if their orders are equal.
        neg_q = (count_N != count_P)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: H \\cap N_G(P) != H \\cap P"
]

N_HYP = 3
NEG_Q_INDEX = 3