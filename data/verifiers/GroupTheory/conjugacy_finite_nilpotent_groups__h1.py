import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
import math
import itertools
import functools

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, x, y = witness
    except Exception:
        return [False, False]
        
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        elif not isinstance(x, Permutation) or not isinstance(y, Permutation):
            h1 = False
        else:
            h1 = x in G and y in G
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            def are_conjugate(G, a, b):
                if a.cycle_structure != b.cycle_structure:
                    return False
                for g in G.generate():
                    if g * a * ~g == b:
                        return True
                return False
            
            xy_conj = are_conjugate(G, x, y)
            
            order_G = G.order()
            primes = list(factorint(order_G).keys())
            
            order_x = x.order()
            order_y = y.order()
            
            def p_part(p_elem, p, n):
                k = 0
                temp = n
                while temp % p == 0:
                    k += 1
                    temp //= p
                pk = p**k
                m = n // pk
                if pk == 1:
                    return p_elem**n
                if m == 1:
                    return p_elem
                c = pow(m, -1, pk)
                e = (c * m) % n
                return p_elem**e
            
            all_p_parts_conj = True
            for p in primes:
                xp = p_part(x, p, order_x)
                yp = p_part(y, p, order_y)
                if not are_conjugate(G, xp, yp):
                    all_p_parts_conj = False
                    break
            
            neg_q = (xy_conj != all_p_parts_conj)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are elements of G",
    "¬Q: x and y are conjugate in G if and only if for every prime p dividing the order of G, their p-parts are conjugate in G (fails)"
]

N_HYP = 1
NEG_Q_INDEX = 1