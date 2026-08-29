import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
import itertools

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

def get_elements(witness):
    if hasattr(witness, 'elements'):
        if callable(witness.elements):
            return list(witness.elements())
        return list(witness.elements)
    return list(witness)

def get_identity(witness):
    if hasattr(witness, 'identity'):
        if callable(witness.identity):
            return witness.identity()
        return witness.identity
    if hasattr(witness, 'e'):
        return witness.e
    elements = get_elements(witness)
    for e in elements:
        if all(op(witness, e, x) == x and op(witness, x, e) == x for x in elements):
            return e
    return None

def op(witness, a, b):
    if hasattr(witness, 'op'):
        return witness.op(a, b)
    return a * b

def inv(witness, a):
    if hasattr(witness, 'inv'):
        return witness.inv(a)
    if hasattr(witness, 'inverse'):
        return witness.inverse(a)
    if hasattr(a, 'inv'):
        if callable(a.inv):
            return a.inv()
        return a.inv
    if hasattr(a, 'inverse'):
        if callable(a.inverse):
            return a.inverse()
        return a.inverse
    try:
        return ~a
    except Exception:
        pass
    try:
        return a**-1
    except Exception:
        pass
    raise ValueError("No inverse found")

def conditions(witness):
    try:
        elements = list(get_elements(witness))
        n = len(elements)
        
        try:
            elem_to_idx = {e: i for i, e in enumerate(elements)}
            def get_idx(e):
                return elem_to_idx[e]
        except TypeError:
            def get_idx(e):
                for i, el in enumerate(elements):
                    if el == e:
                        return i
                raise ValueError("Element not found")
    except Exception:
        return [False, False, False]

    try:
        e_val = get_identity(witness)
        e_idx = get_idx(e_val)
    except Exception:
        return [False, False, False]

    try:
        op_table = [[0]*n for _ in range(n)]
        for i, a in enumerate(elements):
            for j, b in enumerate(elements):
                res = op(witness, a, b)
                op_table[i][j] = get_idx(res)
    except Exception:
        return [False, False, False]

    try:
        inv_idx = [0]*n
        for i, a in enumerate(elements):
            res = inv(witness, a)
            inv_idx[i] = get_idx(res)
    except Exception:
        return [False, False, False]

    try:
        action_table = [[[0]*n for _ in range(n)] for _ in range(n)]
        for g in range(n):
            for h in range(n):
                h_inv = inv_idx[h]
                for x in range(n):
                    action_table[g][h][x] = op_table[op_table[g][x]][h_inv]
    except Exception:
        return [False, False, False]

    # H1: G x G acts on G via (g, h) . x = g x h^-1
    h1_ok = True
    try:
        for x in range(n):
            if action_table[e_idx][e_idx][x] != x:
                h1_ok = False
                break
        
        if h1_ok:
            for g1 in range(n):
                for h1 in range(n):
                    act1 = action_table[g1][h1]
                    for g2 in range(n):
                        for h2 in range(n):
                            act2 = action_table[g2][h2]
                            g1g2 = op_table[g1][g2]
                            h1h2 = op_table[h1][h2]
                            act12 = action_table[g1g2][h1h2]
                            
                            if [act1[act2[x]] for x in range(n)] != act12:
                                h1_ok = False
                                break
                        if not h1_ok: break
                    if not h1_ok: break
                if not h1_ok: break
    except Exception:
        h1_ok = False

    # H2: e is the identity element of G
    h2_ok = True
    try:
        for x in range(n):
            if op_table[e_idx][x] != x or op_table[x][e_idx] != x:
                h2_ok = False
                break
    except Exception:
        h2_ok = False

    # Neg_Q: The stabilizer of e is NOT the diagonal subgroup
    neg_q = False
    try:
        for g in range(n):
            if action_table[g][g][e_idx] != e_idx:
                neg_q = True
                break
        
        if not neg_q:
            for g in range(n):
                for h in range(n):
                    if action_table[g][h][e_idx] == e_idx:
                        if g != h:
                            neg_q = True
                            break
                if neg_q: break
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G x G acts on G via (g, h) . x = g x h^-1",
    "H_2: e is the identity element of G",
    "¬Q: The stabilizer of e in G x G is not the diagonal subgroup Delta(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2