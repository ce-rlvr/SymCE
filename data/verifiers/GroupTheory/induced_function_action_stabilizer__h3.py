import sympy
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Standard algebra objects
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

class FuncWrapper:
    def __init__(self, d):
        self.d = d
    def __getitem__(self, item):
        return self.d[item]
    def __call__(self, item):
        return self.d[item]
    def __contains__(self, item):
        return item in self.d

def apply_func(func, x):
    if callable(func):
        return func(x)
    return func[x]

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            X = witness['X']
            Y = witness['Y']
            action_X = witness['action_X']
            action_Y_X = witness['action_Y_X']
            f = witness['f']
            mul = witness['mul']
            inv = witness['inv']
            id_G = witness['id']
        else:
            G = witness.G
            X = witness.X
            Y = witness.Y
            action_X = witness.action_X
            action_Y_X = witness.action_Y_X
            f = witness.f
            mul = witness.mul
            inv = witness.inv
            id_G = witness.id
    except Exception:
        return [False, False, False, False, False]

    # H1: G is a group acting on a set X
    h1_ok = False
    try:
        is_group = True
        if id_G not in G: 
            is_group = False
        else:
            for g in G:
                if mul(g, id_G) != g or mul(id_G, g) != g: is_group = False
                if mul(g, inv(g)) != id_G or mul(inv(g), g) != id_G: is_group = False
                for h in G:
                    if mul(g, h) not in G: is_group = False
                    for k in G:
                        if mul(mul(g, h), k) != mul(g, mul(h, k)): is_group = False
        
        is_action = True
        for x in X:
            if action_X(id_G, x) != x: is_action = False
            for g in G:
                for h in G:
                    if action_X(mul(g, h), x) != action_X(g, action_X(h, x)): is_action = False
        
        h1_ok = is_group and is_action
    except Exception:
        h1_ok = False

    # H2: Y is a set
    h2_ok = False
    try:
        h2_ok = isinstance(Y, (list, set, tuple)) and len(Y) > 0
    except Exception:
        h2_ok = False

    # H3: G acts on Y^X via (g \cdot f)(x) = f(g^{-1} \cdot x)
    h3_ok = False
    try:
        all_funcs = []
        X_list = list(X)
        for p in itertools.product(Y, repeat=len(X_list)):
            all_funcs.append(FuncWrapper(dict(zip(X_list, p))))
        
        h3_ok = True
        for g in G:
            g_inv = inv(g)
            for func in all_funcs:
                g_func = action_Y_X(g, func)
                for x in X_list:
                    if apply_func(g_func, x) != func[action_X(g_inv, x)]:
                        h3_ok = False
                        break
                if not h3_ok: break
            if not h3_ok: break
    except Exception:
        h3_ok = False

    # H4: f is a function in Y^X
    h4_ok = False
    try:
        h4_ok = True
        for x in X:
            try:
                val = apply_func(f, x)
                if val not in Y:
                    h4_ok = False
                    break
            except Exception:
                h4_ok = False
                break
    except Exception:
        h4_ok = False

    # Conclusion: The stabilizer of f in G is the subgroup {g \in G | f(g^{-1} \cdot x) = f(x) for all x \in X}
    neg_q = False
    try:
        Stab_f = []
        for g in G:
            g_f = action_Y_X(g, f)
            is_eq = True
            for x in X:
                if apply_func(g_f, x) != apply_func(f, x):
                    is_eq = False
                    break
            if is_eq:
                Stab_f.append(g)
        
        Set_f = []
        for g in G:
            g_inv = inv(g)
            is_eq = True
            for x in X:
                if apply_func(f, action_X(g_inv, x)) != apply_func(f, x):
                    is_eq = False
                    break
            if is_eq:
                Set_f.append(g)
        
        Stab_f_unique = []
        for g in Stab_f:
            if g not in Stab_f_unique:
                Stab_f_unique.append(g)
                
        Set_f_unique = []
        for g in Set_f:
            if g not in Set_f_unique:
                Set_f_unique.append(g)
                
        is_subgroup = True
        if id_G not in Set_f_unique:
            is_subgroup = False
        else:
            for g in Set_f_unique:
                if inv(g) not in Set_f_unique:
                    is_subgroup = False
                    break
                for h in Set_f_unique:
                    if mul(g, h) not in Set_f_unique:
                        is_subgroup = False
                        break
                        
        q_ok = (len(Stab_f_unique) == len(Set_f_unique) and all(g in Set_f_unique for g in Stab_f_unique)) and is_subgroup
        neg_q = not q_ok
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: Y is a set",
    "H_3: G acts on Y^X via (g \cdot f)(x) = f(g^{-1} \cdot x)",
    "H_4: f is a function in Y^X",
    "¬Q: The stabilizer of f in G is NOT the subgroup {g \in G | f(g^{-1} \cdot x) = f(x) for all x \in X}"
]

N_HYP = 4
NEG_Q_INDEX = 4