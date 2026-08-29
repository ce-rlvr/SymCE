import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                p, P, N = witness
            elif len(witness) == 2:
                p, P = witness
                N = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H2: N(P) is the normalizer of P in S_p
    try:
        Sp = SymmetricGroup(p)
        P_is_sub = True
        if hasattr(P, 'generators'):
            for g in P.generators:
                if any(i >= p for i in g.support()):
                    P_is_sub = False
                    break
        else:
            P_is_sub = False
            
        if not P_is_sub:
            h2 = False
        else:
            # Restrict p to keep normalizer computation fast
            if p <= 7:
                norm_elements = []
                for x in Sp.generate():
                    normalizes = True
                    for g in P.generators:
                        if not P.contains(x * g * ~x):
                            normalizes = False
                            break
                    if normalizes:
                        norm_elements.append(x)
                
                if N is not None:
                    N_is_sub = True
                    if hasattr(N, 'generators'):
                        for g in N.generators:
                            if any(i >= p for i in g.support()):
                                N_is_sub = False
                                break
                    else:
                        N_is_sub = False
                        
                    if not N_is_sub:
                        h2 = False
                    else:
                        n_normalizes = True
                        for n in N.generators:
                            for g in P.generators:
                                if not P.contains(n * g * ~n):
                                    n_normalizes = False
                                    break
                            if not n_normalizes:
                                break
                        
                        h2 = n_normalizes and (N.order() == len(norm_elements))
                else:
                    h2 = True
            else:
                h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: The order of N(P) is not p(p-1)
    try:
        if N is not None:
            neg_q = bool(N.order() != p * (p - 1))
        elif 'norm_elements' in locals():
            neg_q = bool(len(norm_elements) != p * (p - 1))
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: N(P) is the normalizer of P in S_p",
    "¬Q: The order of N(P) is not p(p-1)"
]

N_HYP = 2
NEG_Q_INDEX = 2