import itertools
import functools
import math
import sympy
from sympy import symbols, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
            R = witness['R']
            add = witness['add']
            mul = witness['mul']
            I_list = witness['I']
            x_list = witness['x']
            zero = witness['zero']
        else:
            R = witness.R
            add = witness.add
            mul = witness.mul
            I_list = witness.I
            x_list = witness.x
            zero = witness.zero
            
        R_list = list(R)
        if len(R_list) > 200:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    def is_ring():
        if zero not in R_list: return False
        R_set = set(R_list)
        
        add_t = {}
        mul_t = {}
        for a in R_list:
            add_t[a] = {}
            mul_t[a] = {}
            for b in R_list:
                try:
                    s = add(a, b)
                    p = mul(a, b)
                except Exception:
                    return False
                if s not in R_set or p not in R_set:
                    return False
                add_t[a][b] = s
                mul_t[a][b] = p

        for a in R_list:
            if add_t[a][zero] != a or add_t[zero][a] != a: return False
            has_inv = False
            for b in R_list:
                if add_t[a][b] == zero and add_t[b][a] == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
            for b in R_list:
                if add_t[a][b] != add_t[b][a]: return False
                for c in R_list:
                    if add_t[add_t[a][b]][c] != add_t[a][add_t[b][c]]: return False
                    if mul_t[mul_t[a][b]][c] != mul_t[a][mul_t[b][c]]: return False
                    if mul_t[a][add_t[b][c]] != add_t[mul_t[a][b]][mul_t[a][c]]: return False
                    if mul_t[add_t[a][b]][c] != add_t[mul_t[a][c]][mul_t[b][c]]: return False
        return True

    h1 = False
    try:
        if is_ring():
            h1 = True
            R_set = set(R_list)
            for I in I_list:
                if not I: 
                    h1 = False
                    break
                I_set = set(I)
                for a in I:
                    if a not in R_set:
                        h1 = False
                        break
                    has_inv = False
                    for b in I:
                        if add(a, b) == zero:
                            has_inv = True
                            break
                    if not has_inv:
                        h1 = False
                        break
                    for b in I:
                        if add(a, b) not in I_set:
                            h1 = False
                            break
                    for r in R_list:
                        if mul(a, r) not in I_set:
                            h1 = False
                            break
                        if mul(r, a) not in I_set:
                            h1 = False
                            break
                if not h1:
                    break
    except Exception:
        h1 = False

    h2 = False
    try:
        h2 = True
        n = len(I_list)
        R_set = set(R_list)
        for i in range(n):
            for j in range(n):
                if i != j:
                    sum_ideal = set()
                    for a in I_list[i]:
                        for b in I_list[j]:
                            sum_ideal.add(add(a, b))
                    if R_set != sum_ideal:
                        h2 = False
                        break
            if not h2:
                break
    except Exception:
        h2 = False

    h3 = False
    try:
        h3 = True
        if len(x_list) != len(I_list):
            h3 = False
        else:
            R_set = set(R_list)
            for x in x_list:
                if x not in R_set:
                    h3 = False
                    break
    except Exception:
        h3 = False

    neg_q = False
    try:
        exists_x = False
        for x in R_list:
            works_for_all = True
            for k in range(len(I_list)):
                xk = x_list[k]
                Ik = I_list[k]
                coset = set(add(xk, a) for a in Ik)
                if x not in coset:
                    works_for_all = False
                    break
            if works_for_all:
                exists_x = True
                break
        neg_q = not exists_x
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: I_1, ..., I_n are ideals of R",
    "H_2: I_i + I_j = R for all i != j",
    "H_3: x_1, ..., x_n are elements of R",
    "¬Q: There is no x in R such that x = x_k (mod I_k) for all k"
]

N_HYP = 3
NEG_Q_INDEX = 3