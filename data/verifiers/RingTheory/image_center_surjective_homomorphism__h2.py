import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools
import math
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_witness_parts(witness):
    if isinstance(witness, dict):
        return witness['R_add'], witness['R_mul'], witness['S_add'], witness['S_mul'], witness['f']
    elif isinstance(witness, (list, tuple)):
        if len(witness) == 5:
            return witness[0], witness[1], witness[2], witness[3], witness[4]
        elif len(witness) == 3:
            R, S, f = witness
            if isinstance(R, dict):
                return R['add'], R['mul'], S['add'], S['mul'], f
            elif isinstance(R, (list, tuple)) and len(R) == 2:
                return R[0], R[1], S[0], S[1], f
            else:
                return R.add, R.mul, S.add, S.mul, f
    else:
        return witness.R_add, witness.R_mul, witness.S_add, witness.S_mul, witness.f

def is_ring(add, mul):
    n = len(add)
    if n == 0: return False
    if len(mul) != n: return False
    for i in range(n):
        if len(add[i]) != n or len(mul[i]) != n: return False
        for j in range(n):
            if type(add[i][j]) is not int: return False
            if type(mul[i][j]) is not int: return False
            if not (0 <= add[i][j] < n): return False
            if not (0 <= mul[i][j] < n): return False
            if add[i][j] != add[j][i]: return False
            
    # associativity of +
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False
                
    # identity for +
    zero = -1
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero == -1: return False
    
    # inverses for +
    for i in range(n):
        if not any(add[i][j] == zero for j in range(n)): return False
        
    return True

def get_center(mul):
    n = len(mul)
    center = []
    for i in range(n):
        if all(mul[i][j] == mul[j][i] for j in range(n)):
            center.append(i)
    return center

def get_f_val(f, x):
    if callable(f):
        return f(x)
    if isinstance(f, dict):
        return f[x]
    return f[x]

def conditions(witness) -> list[bool]:
    try:
        R_add, R_mul, S_add, S_mul, f = get_witness_parts(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_ring(R_add, R_mul)
    except Exception:
        h1 = False
        
    try:
        h2 = is_ring(S_add, S_mul)
    except Exception:
        h2 = False
        
    try:
        R_size = len(R_add)
        S_size = len(S_add)
        
        # Check if f is a valid function from R to S
        valid_f = True
        for i in range(R_size):
            val = get_f_val(f, i)
            if type(val) is not int or not (0 <= val < S_size):
                valid_f = False
                break
                
        if not valid_f:
            neg_q = False
        else:
            # Check if f is a homomorphism
            is_hom = True
            for i in range(R_size):
                for j in range(R_size):
                    fi = get_f_val(f, i)
                    fj = get_f_val(f, j)
                    if get_f_val(f, R_add[i][j]) != S_add[fi][fj]:
                        is_hom = False
                    if get_f_val(f, R_mul[i][j]) != S_mul[fi][fj]:
                        is_hom = False
            
            if not is_hom:
                neg_q = False
            else:
                Z_R = get_center(R_mul)
                Z_S = get_center(S_mul)
                
                neg_q = False
                for x in Z_R:
                    fx = get_f_val(f, x)
                    if fx not in Z_S:
                        neg_q = True
                        break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: S is a ring",
    "¬Q: The image f(Z(R)) is not contained in the center of S"
]

N_HYP = 2
NEG_Q_INDEX = 2