import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    "H_1: f is a group homomorphism from G to H",
    "H_2: Z(G) is the center of G",
    "H_3: C_H(f(G)) is the centralizer of f(G) in H",
    "¬Q: f(Z(G)) is not a subset of C_H(f(G))"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if len(witness) == 3:
            G, H, f = witness
            Z_wit = None
            C_wit = None
        elif len(witness) == 5:
            G, H, f, Z_wit, C_wit = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        try:
            elements_G = list(G.generate())
        except AttributeError:
            elements_G = list(G)
            
        try:
            elements_H = list(H.generate())
        except AttributeError:
            elements_H = list(H)
    except Exception:
        return [False, False, False, False]

    if isinstance(f, dict):
        def f_eval(x): return f[x]
    elif isinstance(f, list):
        try:
            f_dict = dict(f)
            def f_eval(x): return f_dict[x]
        except Exception:
            return [False, False, False, False]
    else:
        f_eval = f

    h1 = False
    try:
        h1 = True
        for g in elements_G:
            if f_eval(g) not in elements_H:
                h1 = False
                break
        if h1:
            for g1 in elements_G:
                for g2 in elements_G:
                    if f_eval(g1 * g2) != f_eval(g1) * f_eval(g2):
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    Z_actual = []
    try:
        for z in elements_G:
            if all(z * g == g * z for g in elements_G):
                Z_actual.append(z)
    except Exception:
        pass

    C_actual = []
    try:
        f_G = []
        for g in elements_G:
            val = f_eval(g)
            if val not in f_G:
                f_G.append(val)
                
        for h in elements_H:
            if all(h * x == x * h for x in f_G):
                C_actual.append(h)
    except Exception:
        pass

    h2 = False
    try:
        if Z_wit is not None:
            z_wit_list = list(Z_wit)
            if len(z_wit_list) == len(Z_actual) and all(z in Z_actual for z in z_wit_list):
                h2 = True
        else:
            h2 = True
    except Exception:
        h2 = False

    h3 = False
    try:
        if C_wit is not None:
            c_wit_list = list(C_wit)
            if len(c_wit_list) == len(C_actual) and all(c in C_actual for c in c_wit_list):
                h3 = True
        else:
            h3 = True
    except Exception:
        h3 = False

    neg_q = False
    try:
        Z_to_use = Z_wit if Z_wit is not None else Z_actual
        C_to_use = C_wit if C_wit is not None else C_actual
        
        for z in Z_to_use:
            if f_eval(z) not in C_to_use:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]