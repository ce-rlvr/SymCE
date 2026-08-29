import sympy
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        p, P = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False
        
    try:
        if isinstance(P, PermutationGroup) and P.degree <= p and P.order() == p:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False
        
    try:
        if not isinstance(P, PermutationGroup):
            neg_q = False
        else:
            order_P = P.order()
            if order_P > 100000:
                neg_q = False
            else:
                gen = None
                for g in P.generate():
                    if g.order() == order_P:
                        gen = g
                        break
                
                if gen is not None:
                    moved = sum(len(c) for c in gen.cyclic_form)
                    c1 = int(p - moved)
                    if c1 < 0 or c1 > 10000:
                        neg_q = False
                    else:
                        counts = {}
                        for c in gen.cyclic_form:
                            length = len(c)
                            counts[length] = counts.get(length, 0) + 1
                        if c1 > 0:
                            counts[1] = c1
                            
                        c_g = 1
                        for length, count in counts.items():
                            c_g *= (length ** count) * math.factorial(int(count))
                            
                        phi = sympy.totient(order_P)
                        order_NP = c_g * phi
                        
                        neg_q = bool(order_NP != p * (p - 1))
                else:
                    neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P is a Sylow p-subgroup of the symmetric group S_p",
    "¬Q: The order of N(P) is not p(p-1)"
]

N_HYP = 2
NEG_Q_INDEX = 2