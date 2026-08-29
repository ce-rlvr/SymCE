import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G \\to H is a group homomorphism",
    "H_3: p is a prime number",
    "H_4: The kernel of f is a finite p-group",
    "¬Q: G is not a finite p-group"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        G, H, f, p = witness
    except Exception:
        return [False] * 5

    # H1: G and H are groups
    try:
        h1 = hasattr(G, 'generate') and hasattr(H, 'generate') and hasattr(G, 'order') and hasattr(H, 'order')
    except Exception:
        h1 = False

    # H2: f is a homomorphism
    try:
        G_elems = list(G.generate())
        if isinstance(f, dict):
            func = lambda x: f.get(x, None)
        elif callable(f):
            func = f
        else:
            func = None
            
        if func is None:
            h2 = False
        else:
            h2 = True
            for x in G_elems:
                fx = func(x)
                if fx is None or not H.contains(fx):
                    h2 = False
                    break
            if h2:
                for x in G_elems:
                    for y in G_elems:
                        if func(x * y) != func(x) * func(y):
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H3: p is a prime number
    try:
        h3 = bool(isprime(p))
    except Exception:
        h3 = False

    def is_p_group(order, p_val):
        try:
            order = int(order)
            p_val = int(p_val)
        except Exception:
            return False
        if p_val <= 1:
            return False
        if order == 1:
            return True
        if order <= 0:
            return False
        while order % p_val == 0:
            order //= p_val
        return order == 1

    # H4: The kernel of f is a finite p-group
    try:
        if func is None:
            h4 = False
        else:
            id_H = None
            for h_elem in list(H.generate()):
                if h_elem * h_elem == h_elem:
                    id_H = h_elem
                    break
            
            if id_H is None:
                h4 = False
            else:
                ker_size = 0
                for x in G_elems:
                    if func(x) == id_H:
                        ker_size += 1
                
                h4 = is_p_group(ker_size, p)
    except Exception:
        h4 = False

    # neg_Q: G is not a finite p-group
    try:
        neg_q = not is_p_group(G.order(), p)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]