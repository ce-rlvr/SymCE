import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G, p, P, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False
        
    # H_3: P is a Sylow p-subgroup of G
    try:
        if isinstance(P, PermutationGroup) and P.is_subgroup(G):
            if isinstance(p, (int, sympy.Integer)) and p > 1:
                order = G.order()
                max_pow = 1
                while order % p == 0:
                    max_pow *= p
                    order //= p
                h3 = bool(P.order() == max_pow)
            else:
                h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: There does NOT exist an element g in G such that H is a subgroup of gPg^(-1)
    try:
        if not isinstance(H, PermutationGroup):
            neg_q = True
        else:
            neg_q = True
            count = 0
            for g in G.elements:
                count += 1
                if count > 5000:
                    break
                is_sub = True
                for h in H.generators:
                    try:
                        # Check if h is in gPg^(-1), which is equivalent to g^(-1)hg in P
                        conj = ~g * h * g
                        if conj not in P:
                            is_sub = False
                            break
                    except Exception:
                        is_sub = False
                        break
                if is_sub:
                    neg_q = False
                    break
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: There does not exist an element g in G such that H is a subgroup of gPg^(-1)"
]

N_HYP = 3
NEG_Q_INDEX = 3