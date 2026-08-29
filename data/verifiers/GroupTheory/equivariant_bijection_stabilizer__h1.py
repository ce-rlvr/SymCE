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

def get_field(w, name, default=None):
    if isinstance(w, dict):
        return w.get(name, default)
    return getattr(w, name, default)

def apply_f(f, a):
    if isinstance(f, dict):
        return f[a]
    elif isinstance(f, (list, tuple)):
        return f[a]
    return f(a)

def apply_action(action, g, a):
    if action is not None:
        if isinstance(action, dict):
            return action[(g, a)]
        return action(g, a)
    else:
        try:
            return g(a)
        except TypeError:
            return g * a

def conditions(witness) -> list[bool]:
    try:
        X = get_field(witness, 'X')
        Y = get_field(witness, 'Y')
        f = get_field(witness, 'f')
        G = get_field(witness, 'G')
        action = get_field(witness, 'action')
        x = get_field(witness, 'x')
        
        if X is None or Y is None or f is None or G is None or x is None:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: f is a bijection from X to Y
    h1_ok = False
    try:
        images = []
        valid = True
        for a in X:
            img = apply_f(f, a)
            if img not in Y:
                valid = False
                break
            images.append(img)
        if valid:
            # Check injectivity
            if len(images) == len(X) and len(set(images)) == len(X):
                # Check surjectivity
                if set(images) == set(Y):
                    h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: f is G-equivariant
    h2_ok = False
    try:
        valid = True
        for g in G:
            for a in X:
                g_a = apply_action(action, g, a)
                f_g_a = apply_f(f, g_a)
                f_a = apply_f(f, a)
                g_f_a = apply_action(action, g, f_a)
                if f_g_a != g_f_a:
                    valid = False
                    break
            if not valid:
                break
        h2_ok = valid
    except Exception:
        h2_ok = False

    # H_3: x is an element of X
    h3_ok = False
    try:
        h3_ok = x in X
    except Exception:
        h3_ok = False

    # neg_Q: The stabilizer of x in G is not exactly equal to the stabilizer of f(x) in G
    neg_q_ok = False
    try:
        fx = apply_f(f, x)
        for g in G:
            in_stab_x = (apply_action(action, g, x) == x)
            in_stab_fx = (apply_action(action, g, fx) == fx)
            if in_stab_x != in_stab_fx:
                neg_q_ok = True
                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a bijection from X to Y",
    "H_2: f is G-equivariant (f(g * x) = g * f(x) for all g in G and x in X)",
    "H_3: x is an element of X",
    "¬Q: The stabilizer of x in G is not exactly equal to the stabilizer of f(x) in G"
]

N_HYP = 3
NEG_Q_INDEX = 3