import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
        if isinstance(witness, dict):
            p = witness.get('p')
            n = witness.get('n')
            G = witness.get('G')
            U = witness.get('U')
        else:
            p, n, G, U = witness
    except Exception:
        return [False, False, False, False]

    # H_1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H_2: n is a positive integer
    try:
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False

    # H_3: G is the general linear group GL_n(F_p)
    try:
        if not (h1 and h2):
            h3 = False
        else:
            order_G = math.prod(p**n - p**i for i in range(n))
            if len(G) != order_G:
                h3 = False
            else:
                G_tuples = set()
                h3 = True
                for g_raw in G:
                    try:
                        g = sympy.Matrix(g_raw)
                    except Exception:
                        h3 = False
                        break
                    if g.shape != (n, n):
                        h3 = False
                        break
                    if any(x % 1 != 0 or x < 0 or x >= p for x in g):
                        h3 = False
                        break
                    if g.det() % p == 0:
                        h3 = False
                        break
                    G_tuples.add(tuple(g))
                if h3:
                    h3 = len(G_tuples) == order_G
    except Exception:
        h3 = False

    # ¬Q: U is not a Sylow p-subgroup of G
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            is_sylow = True
            try:
                order_G = len(G)
                if order_G == 0:
                    is_sylow = False
                else:
                    p_power = 1
                    temp = order_G
                    while temp % p == 0 and temp > 0:
                        p_power *= p
                        temp //= p
                    
                    if len(U) != p_power:
                        is_sylow = False
                    else:
                        G_tuples = set()
                        for g_raw in G:
                            try:
                                G_tuples.add(tuple(sympy.Matrix(g_raw)))
                            except Exception:
                                pass
                        
                        U_tuples = set()
                        for u_raw in U:
                            u = sympy.Matrix(u_raw).applyfunc(lambda x: x % p)
                            if tuple(u) not in G_tuples:
                                is_sylow = False
                                break
                            U_tuples.add(tuple(u))
                        
                        if is_sylow and len(U_tuples) != p_power:
                            is_sylow = False
                        
                        if is_sylow:
                            try:
                                for u_t in U_tuples:
                                    for v_t in U_tuples:
                                        u = sympy.Matrix(n, n, u_t)
                                        v = sympy.Matrix(n, n, v_t)
                                        prod = (u * v).applyfunc(lambda x: x % p)
                                        if tuple(prod) not in U_tuples:
                                            is_sylow = False
                                            break
                                    if not is_sylow:
                                        break
                            except Exception:
                                is_sylow = False
            except Exception:
                is_sylow = False
            
            neg_q = not is_sylow
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: n is a positive integer",
    "H_3: G is the general linear group GL_n(F_p)",
    "¬Q: U is not a Sylow p-subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3