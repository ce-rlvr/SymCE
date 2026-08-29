import math
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import primefactors

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: G is a group acting faithfully on a set X",
    "H_2: H is a group acting faithfully on a set Y",
    "not Q: W does not have a faithful action on the Cartesian product X \\times Y"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, H = witness
            elif len(witness) == 4:
                G, H, X, Y = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(H, PermutationGroup)
    except Exception:
        h2 = False

    neg_q = False
    try:
        if h1 and h2:
            X_size = G.degree
            Y_size = H.degree
            N = X_size * Y_size
            
            if X_size == 0 and H.order() > 1:
                neg_q = True
            else:
                order_G = G.order()
                order_H = H.order()
                
                def vp(n, p):
                    count = 0
                    while n > 0 and n % p == 0:
                        count += 1
                        n //= p
                    return count
                    
                def vp_factorial(n, p):
                    count = 0
                    while n > 0:
                        count += n // p
                        n //= p
                    return count
                
                # Check if the regular wreath product can embed in Sym(X \times Y)
                # by comparing the sizes of their Sylow p-subgroups.
                if order_G > 1:
                    for p in primefactors(order_G):
                        if vp(order_G, p) * order_H + vp(order_H, p) > vp_factorial(N, p):
                            neg_q = True
                            break
                            
                # Fallback size check using logarithms to prevent huge integer arithmetic
                if not neg_q and order_G > 1:
                    if order_H > 10**100:
                        neg_q = True
                    else:
                        log_W = float(order_H) * math.log(float(order_G)) + math.log(float(order_H))
                        log_N_fact = sum(math.log(i) for i in range(1, N + 1)) if N > 0 else 0.0
                        if log_W > log_N_fact + 1e-6:
                            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]