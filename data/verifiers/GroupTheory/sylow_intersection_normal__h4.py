import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import sympy.ntheory

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
        G, N, P, p = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False
        
    # H3: p is a prime number
    try:
        h3 = sympy.ntheory.isprime(p)
    except Exception:
        h3 = False
        
    # neg_Q: P \cap N is NOT a Sylow p-subgroup of N
    try:
        if isinstance(P, PermutationGroup):
            P_elms = set(P.generate())
        else:
            P_elms = set(P)
            
        N_elms = set(N.generate())
        
        # Normalize permutations to their minimal array form to ensure robust equality checks
        def normalize(perm):
            arr = list(perm.array_form)
            while arr and arr[-1] == len(arr) - 1:
                arr.pop()
            return tuple(arr)
            
        P_norm = {normalize(p_elem) for p_elem in P_elms}
        intersect_list = [n_elem for n_elem in N_elms if normalize(n_elem) in P_norm]
        
        n_order = len(N_elms)
        if n_order == 0:
            neg_q = False
        else:
            p_k = 1
            if sympy.ntheory.isprime(p):
                while n_order % (p_k * p) == 0:
                    p_k *= p
            else:
                p_k = -1
                
            if len(intersect_list) != p_k:
                is_sylow = False
            else:
                is_sylow = True
                if len(intersect_list) > 0:
                    # Check if the intersection contains the identity
                    if not any(normalize(x) == () for x in intersect_list):
                        is_sylow = False
                    else:
                        # Check closure under multiplication
                        for a in intersect_list:
                            for b in intersect_list:
                                if normalize(a * b) not in P_norm:
                                    is_sylow = False
                                    break
                            if not is_sylow:
                                break
                else:
                    is_sylow = False
            neg_q = not is_sylow
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: p is a prime number",
    "¬Q: P \\cap N is not a Sylow p-subgroup of N"
]

N_HYP = 3
NEG_Q_INDEX = 3