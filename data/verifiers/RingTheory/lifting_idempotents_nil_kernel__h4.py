import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

from sympy import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def normalize_table(table):
    if hasattr(table, 'tolist'):
        return table.tolist()
    return [list(row) for row in table]

def is_ring(add, mul):
    try:
        n = len(add)
        if n == 0: return False, None
        if any(len(row) != n for row in add): return False, None
        if len(mul) != n or any(len(row) != n for row in mul): return False, None
        
        zero = None
        for i in range(n):
            if all(add[i][j] == j and add[j][i] == j for j in range(n)):
                zero = i
                break
        if zero is None: return False, None
        
        has_mul_id = False
        for i in range(n):
            if all(mul[i][j] == j and mul[j][i] == j for j in range(n)):
                has_mul_id = True
                break
        if not has_mul_id: return False, None
        
        for i in range(n):
            if not any(add[i][j] == zero and add[j][i] == zero for j in range(n)):
                return False, None
            for j in range(n):
                if add[i][j] != add[j][i]: return False, None
                for k in range(n):
                    if add[add[i][j]][k] != add[i][add[j][k]]: return False, None
                    if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False, None
                    if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False, None
                    if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False, None
        return True, zero
    except Exception:
        return False, None

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R_add = witness['R_add']
            R_mul = witness['R_mul']
            S_add = witness['S_add']
            S_mul = witness['S_mul']
            f_input = witness['f']
            e = witness['e']
        else:
            R_add = witness[0]
            R_mul = witness[1]
            S_add = witness[2]
            S_mul = witness[3]
            f_input = witness[4]
            e = witness[5]
            
        R_add = normalize_table(R_add)
        R_mul = normalize_table(R_mul)
        S_add = normalize_table(S_add)
        S_mul = normalize_table(S_mul)
        
        n = len(R_add)
        if isinstance(f_input, dict):
            f = [f_input.get(i, -1) for i in range(n)]
        elif callable(f_input):
            f = [f_input(i) for i in range(n)]
        else:
            f = list(f_input)
            
    except Exception:
        return [False, False, False, False]

    # H1: R and S are rings
    try:
        R_ok, zero_R = is_ring(R_add, R_mul)
        S_ok, zero_S = is_ring(S_add, S_mul)
        h1 = bool(R_ok and S_ok)
    except Exception:
        h1 = False

    # H2: f: R -> S is a surjective ring homomorphism
    try:
        if not h1:
            h2 = False
        else:
            m = len(S_add)
            if len(f) != n:
                h2 = False
            elif set(f) != set(range(m)):
                h2 = False
            else:
                h2 = True
                for i in range(n):
                    for j in range(n):
                        if f[R_add[i][j]] != S_add[f[i]][f[j]]:
                            h2 = False
                        if f[R_mul[i][j]] != S_mul[f[i]][f[j]]:
                            h2 = False
    except Exception:
        h2 = False

    # H3: The kernel of f is a nil ideal
    try:
        if not (h1 and h2):
            h3 = False
        else:
            ker = [i for i in range(n) if f[i] == zero_S]
            h3 = True
            for x in ker:
                p = x
                is_nil = False
                for _ in range(n + 1):
                    if p == zero_R:
                        is_nil = True
                        break
                    p = R_mul[p][x]
                if not is_nil:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # neg_Q: There does NOT exist an idempotent E in R such that f(E) = e
    try:
        if not h1:
            neg_q = False
        else:
            exists = False
            for E in range(n):
                if R_mul[E][E] == E and f[E] == e:
                    exists = True
                    break
            neg_q = not exists
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a surjective ring homomorphism from R to S",
    "H_3: The kernel of f is a nil ideal",
    "¬Q: There does not exist an idempotent E in R such that f(E) = e"
]

N_HYP = 3
NEG_Q_INDEX = 3