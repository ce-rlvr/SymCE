import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(group):
    if hasattr(group, 'elements'):
        return set(group.elements)
    elif hasattr(group, 'generate'):
        return set(group.generate())
    else:
        return set(group)

def get_identity(elements):
    elements = list(elements)
    if not elements: return None
    x = elements[0]
    for e in elements:
        if e * x == x and x * e == x:
            return e
    return None

def inv(g, elements, identity):
    for x in elements:
        if g * x == identity and x * g == identity:
            return x
    try:
        return g**-1
    except Exception:
        return ~g

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, N, H = witness
        else:
            G, N, H = witness.G, witness.N, witness.H
    except Exception:
        return [False, False, False, False]

    try:
        set_G = get_elements(G)
        set_N = get_elements(N)
        set_H = get_elements(H)
        
        e_G = get_identity(set_G)
        e_N = get_identity(set_N)
        e_H = get_identity(set_H)
    except Exception:
        return [False, False, False, False]

    # H1: G = N \rtimes H is the semidirect product of N and H
    try:
        h1 = True
        if not set_N.issubset(set_G): h1 = False
        if not set_H.issubset(set_G): h1 = False
        
        if h1:
            for g in set_G:
                g_inv = inv(g, set_G, e_G)
                for n in set_N:
                    if g * n * g_inv not in set_N:
                        h1 = False
                        break
                if not h1: break
                
        if h1:
            if set_N.intersection(set_H) != {e_G}: h1 = False
            if len(set_N) * len(set_H) != len(set_G): h1 = False
    except Exception:
        h1 = False

    # H2: G acts on N via the action (n, h) \cdot x = n h x h^{-1}
    try:
        decomp = {}
        for n in set_N:
            for h in set_H:
                decomp[n * h] = (n, h)
                
        def act(g, x):
            n, h = decomp[g]
            h_inv = inv(h, set_H, e_H)
            return n * h * x * h_inv
            
        h2 = True
        if len(decomp) != len(set_G):
            h2 = False
            
        if h2:
            for x in set_N:
                if act(e_G, x) != x:
                    h2 = False
                    break
                    
        if h2:
            for g1 in set_G:
                for g2 in set_G:
                    for x in set_N:
                        if act(g1, act(g2, x)) != act(g1 * g2, x):
                            h2 = False
                            break
                    if not h2: break
                if not h2: break
    except Exception:
        h2 = False

    # H3: e_N is the identity element of N
    try:
        h3 = True
        if e_N is None:
            h3 = False
        else:
            for n in set_N:
                if e_N * n != n or n * e_N != n:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # neg_Q: The stabilizer of e_N under this action is exactly the subgroup H of G
    try:
        neg_q = False
        if len(decomp) > 0:
            stabilizer = set()
            for g in set_G:
                if g in decomp:
                    if act(g, e_N) == e_N:
                        stabilizer.add(g)
            neg_q = (stabilizer != set_H)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is the semidirect product of N and H",
    "H_2: G acts on N via the action (n, h) \cdot x = n h x h^{-1}",
    "H_3: e_N is the identity element of N",
    "¬Q: The stabilizer of e_N under this action is not exactly the subgroup H of G"
]

N_HYP = 3
NEG_Q_INDEX = 3