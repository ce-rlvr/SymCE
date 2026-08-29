import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    try:
        G, f = witness
    except Exception:
        return [False, False, False]
        
    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        elif hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        e = None
        for x in elements:
            if x * x == x:
                e = x
                break
        if e is None:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: f is a group endomorphism
    try:
        h1 = True
        # Check closure
        for x in elements:
            for y in elements:
                if x * y not in elements:
                    h1 = False
                    break
            if not h1:
                break
        # Check inverses
        if h1:
            for x in elements:
                has_inv = False
                for y in elements:
                    if x * y == e and y * x == e:
                        has_inv = True
                        break
                if not has_inv:
                    h1 = False
                    break
        # Check homomorphism and codomain
        if h1:
            for x in elements:
                if f(x) not in elements:
                    h1 = False
                    break
                for y in elements:
                    if f(x * y) != f(x) * f(y):
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False
        
    # H2: f o f = f
    try:
        h2 = True
        for x in elements:
            if f(f(x)) != f(x):
                h2 = False
                break
    except Exception:
        h2 = False
        
    # Q: G is the internal semidirect product of ker f and im f
    try:
        K = []
        H = []
        for x in elements:
            fx = f(x)
            if fx == e:
                if x not in K:
                    K.append(x)
            if fx not in H:
                H.append(fx)
                
        # Check K is normal
        k_normal = True
        for k in K:
            for g in elements:
                g_inv = None
                for y in elements:
                    if g * y == e and y * g == e:
                        g_inv = y
                        break
                if g_inv is None:
                    k_normal = False
                    break
                conj = g * k * g_inv
                if conj not in K:
                    k_normal = False
                    break
            if not k_normal:
                break
                
        # Check H is subgroup
        h_subgroup = True
        for h1_elem in H:
            for h2_elem in H:
                if h1_elem * h2_elem not in H:
                    h_subgroup = False
                    break
            if not h_subgroup:
                break
                
        # Check K intersect H = {e}
        k_int_h = [x for x in K if x in H]
        int_trivial = (len(k_int_h) == 1 and k_int_h[0] == e)
        
        # Check K H = G
        KH = []
        for k in K:
            for h_elem in H:
                prod = k * h_elem
                if prod not in KH:
                    KH.append(prod)
        kh_equals_g = (len(KH) == len(elements))
        
        q = k_normal and h_subgroup and int_trivial and kh_equals_g
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a group endomorphism",
    "H_2: f o f = f",
    "¬Q: G is not the internal semidirect product of the kernel of f and the image of f"
]

N_HYP = 2
NEG_Q_INDEX = 2