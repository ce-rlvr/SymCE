import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        if isinstance(witness, dict):
            n = witness.get('n')
            m = witness.get('m')
            R = witness.get('R')
            S = witness.get('S')
            add_R = witness.get('add_R')
            zero_S = witness.get('zero_S', 0)
            f = witness.get('f')
            s = witness.get('s')
            r = witness.get('r')
        else:
            n = getattr(witness, 'n', None)
            m = getattr(witness, 'm', None)
            R = getattr(witness, 'R', None)
            S = getattr(witness, 'S', None)
            add_R = getattr(witness, 'add_R', None)
            zero_S = getattr(witness, 'zero_S', 0)
            f = getattr(witness, 'f', None)
            s = getattr(witness, 's', None)
            r = getattr(witness, 'r', None)

        if n is not None and m is not None:
            R_set = list(range(n))
            S_set = list(range(m))
            add_func = lambda x, y: (x + y) % n
            zero_S_val = 0
            is_ring = (n > 0 and m > 0)
        else:
            R_set = list(R)
            S_set = list(S)
            if add_R is not None:
                if isinstance(add_R, dict):
                    add_func = lambda x, y: add_R[(x, y)]
                else:
                    add_func = add_R
            else:
                add_func = lambda x, y: x + y
            zero_S_val = zero_S
            is_ring = len(R_set) > 0 and len(S_set) > 0

        if isinstance(f, (dict, list, tuple)):
            f_func = lambda x: f[x]
        else:
            f_func = f
    except Exception:
        return [False, False, False, False]

    # H1: R and S are rings
    try:
        h1 = bool(is_ring)
    except Exception:
        h1 = False

    # H2: s is an element in the image of f
    try:
        image_f = [f_func(x) for x in R_set]
        h2 = bool(s in image_f)
    except Exception:
        h2 = False

    # H3: r in R is an element such that f(r) = s
    try:
        h3 = bool((r in R_set) and (f_func(r) == s))
    except Exception:
        h3 = False

    # neg_Q: The preimage f^(-1)({s}) is not exactly the coset r + K
    try:
        K = [x for x in R_set if f_func(x) == zero_S_val]
        preimage_s = [x for x in R_set if f_func(x) == s]
        
        coset = []
        for k in K:
            val = add_func(r, k)
            if val not in coset:
                coset.append(val)
                
        def is_subset(l1, l2):
            for i1 in l1:
                if i1 not in l2:
                    return False
            return True
            
        neg_q = not (is_subset(preimage_s, coset) and is_subset(coset, preimage_s))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: s is an element in the image of f",
    "H_3: r in R is an element such that f(r) = s",
    "¬Q: The preimage f^(-1)({s}) is not exactly the coset r + K"
]

N_HYP = 3
NEG_Q_INDEX = 3