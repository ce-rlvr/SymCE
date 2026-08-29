import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    "H_1: f_1: G_1 -> H is a group homomorphism",
    "H_2: f_2: G_2 -> H is a group homomorphism",
    "¬Q: The set {(x, y) in G_1 x G_2 | f_1(x) = f_2(y)} is not a subgroup of G_1 x G_2"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_group(elements, op, check_associativity=True):
    unique_elements = []
    for e in elements:
        if e not in unique_elements:
            unique_elements.append(e)
    elements = unique_elements
    if not elements:
        return False
    n = len(elements)
    
    table = [[None]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            try:
                c = op(elements[i], elements[j])
            except Exception:
                return False
            try:
                idx = elements.index(c)
            except ValueError:
                return False
            table[i][j] = idx
            
    if check_associativity:
        for i in range(n):
            for j in range(n):
                ij = table[i][j]
                for k in range(n):
                    if table[ij][k] != table[i][table[j][k]]:
                        return False
                    
    id_idx = None
    for i in range(n):
        is_id = True
        for j in range(n):
            if table[i][j] != j or table[j][i] != j:
                is_id = False
                break
        if is_id:
            id_idx = i
            break
            
    if id_idx is None:
        return False
        
    for i in range(n):
        has_inv = False
        for j in range(n):
            if table[i][j] == id_idx and table[j][i] == id_idx:
                has_inv = True
                break
        if not has_inv:
            return False
            
    return True

def conditions(witness):
    try:
        G1 = witness['G1']
        G2 = witness['G2']
        H = witness['H']
        f1 = witness['f1']
        f2 = witness['f2']
    except Exception:
        return [False, False, False]
        
    op1 = witness.get('op1', lambda x, y: x * y)
    op2 = witness.get('op2', lambda x, y: x * y)
    opH = witness.get('opH', lambda x, y: x * y)
    
    try:
        G1_elems = list(G1.elements) if hasattr(G1, 'elements') else list(G1)
        G2_elems = list(G2.elements) if hasattr(G2, 'elements') else list(G2)
        H_elems = list(H.elements) if hasattr(H, 'elements') else list(H)
    except Exception:
        return [False, False, False]

    def apply_f(f, x):
        if isinstance(f, dict):
            return f[x]
        return f(x)

    # H1: f1 is a homomorphism
    h1_ok = False
    try:
        h1_ok = True
        for x in G1_elems:
            for y in G1_elems:
                xy = op1(x, y)
                fx = apply_f(f1, x)
                fy = apply_f(f1, y)
                fxy = apply_f(f1, xy)
                if opH(fx, fy) != fxy:
                    h1_ok = False
                    break
                if fx not in H_elems or fy not in H_elems or fxy not in H_elems:
                    h1_ok = False
                    break
            if not h1_ok:
                break
    except Exception:
        h1_ok = False

    # H2: f2 is a homomorphism
    h2_ok = False
    try:
        h2_ok = True
        for x in G2_elems:
            for y in G2_elems:
                xy = op2(x, y)
                fx = apply_f(f2, x)
                fy = apply_f(f2, y)
                fxy = apply_f(f2, xy)
                if opH(fx, fy) != fxy:
                    h2_ok = False
                    break
                if fx not in H_elems or fy not in H_elems or fxy not in H_elems:
                    h2_ok = False
                    break
            if not h2_ok:
                break
    except Exception:
        h2_ok = False

    # neg_Q: P is NOT a subgroup of G1 x G2
    neg_q = False
    try:
        P = []
        for x in G1_elems:
            for y in G2_elems:
                if apply_f(f1, x) == apply_f(f2, y):
                    P.append((x, y))
                    
        def op_prod(a, b):
            return (op1(a[0], b[0]), op2(a[1], b[1]))
            
        is_sub = True
        if not is_group(G1_elems, op1, True):
            is_sub = False
        elif not is_group(G2_elems, op2, True):
            is_sub = False
        elif not is_group(P, op_prod, False):
            is_sub = False
            
        neg_q = not is_sub
    except Exception:
        neg_q = True

    return [h1_ok, h2_ok, neg_q]