import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 2:
            G, u = witness
            v = None
        elif len(witness) == 3:
            G, u, v = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(u, dict) and all(isinstance(c, int) for c in u.values())
        u_clean = {g: c for g, c in u.items() if c != 0}
        h1 = h1 and all((g in G) for g in u_clean)
        
        if v is not None:
            h1 = h1 and isinstance(v, dict) and all(isinstance(c, int) for c in v.values())
            v_clean = {g: c for g, c in v.items() if c != 0}
            h1 = h1 and all((g in G) for g in v_clean)
    except Exception:
        h1 = False

    try:
        if v is not None:
            def mul(a, b):
                res = {}
                for g1, c1 in a.items():
                    if c1 == 0: continue
                    for g2, c2 in b.items():
                        if c2 == 0: continue
                        g = g1 * g2
                        res[g] = res.get(g, 0) + c1 * c2
                return {g: c for g, c in res.items() if c != 0}
            
            prod1 = mul(u, v)
            prod2 = mul(v, u)
            
            id_elem = getattr(G, 'identity', None)
            if id_elem is None:
                for g in G.elements:
                    id_elem = g * (~g)
                    break
                    
            id_dict = {id_elem: 1} if id_elem is not None else {}
            h2 = (prod1 == id_dict) and (prod2 == id_dict)
        else:
            elements = list(G.elements)
            n = len(elements)
            idx = {g: i for i, g in enumerate(elements)}
            
            from sympy import Matrix
            M = Matrix.zeros(n, n)
            u_clean = {g: c for g, c in u.items() if c != 0}
            for j, h in enumerate(elements):
                for g_u, c in u_clean.items():
                    gh = g_u * h
                    i = idx[gh]
                    M[i, j] += c
            det = M.det()
            h2 = (det == 1 or det == -1)
    except Exception:
        h2 = False

    try:
        non_zeros = {g: c for g, c in u.items() if c != 0}
        if len(non_zeros) == 1:
            c = list(non_zeros.values())[0]
            neg_q = (c != 1 and c != -1)
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: u is an element of the integral group ring", "H_2: u is an invertible element", "not Q: u is not of the form g or -g"]
N_HYP = 2
NEG_Q_INDEX = 2