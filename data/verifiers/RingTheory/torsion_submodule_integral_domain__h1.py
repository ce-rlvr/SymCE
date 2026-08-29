import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def is_abelian_group(add_table):
    n = len(add_table)
    for i in range(n):
        if len(add_table[i]) != n: return False, -1
        for j in range(n):
            if not (0 <= add_table[i][j] < n): return False, -1
    for i in range(n):
        for j in range(n):
            if add_table[i][j] != add_table[j][i]: return False, -1
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return False, -1
    id_elem = -1
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)):
            id_elem = i
            break
    if id_elem == -1: return False, -1
    for i in range(n):
        if not any(add_table[i][j] == id_elem for j in range(n)): return False, -1
    return True, id_elem

def is_ring(add_table, mult_table):
    n = len(add_table)
    if len(mult_table) != n: return False, -1, -1
    is_ab, zero = is_abelian_group(add_table)
    if not is_ab: return False, -1, -1
    for i in range(n):
        if len(mult_table[i]) != n: return False, -1, -1
        for j in range(n):
            if not (0 <= mult_table[i][j] < n): return False, -1, -1
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mult_table[mult_table[i][j]][k] != mult_table[i][mult_table[j][k]]: return False, -1, -1
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mult_table[i][add_table[j][k]] != add_table[mult_table[i][j]][mult_table[i][k]]: return False, -1, -1
                if mult_table[add_table[i][j]][k] != add_table[mult_table[i][k]][mult_table[j][k]]: return False, -1, -1
    one = -1
    for i in range(n):
        if all(mult_table[i][j] == j and mult_table[j][i] == j for j in range(n)):
            one = i
            break
    if one == -1: return False, -1, -1
    return True, zero, one

def is_module(R_add, R_mult, M_add, action):
    ring_ok, zero_R, one_R = is_ring(R_add, R_mult)
    if not ring_ok: return False, -1, -1, -1
    M_ok, zero_M = is_abelian_group(M_add)
    if not M_ok: return False, -1, -1, -1
    nR = len(R_add)
    nM = len(M_add)
    if len(action) != nR: return False, -1, -1, -1
    for row in action:
        if len(row) != nM: return False, -1, -1, -1
        for val in row:
            if not (0 <= val < nM): return False, -1, -1, -1
    for r in range(nR):
        for m1 in range(nM):
            for m2 in range(nM):
                if action[r][M_add[m1][m2]] != M_add[action[r][m1]][action[r][m2]]: return False, -1, -1, -1
    for r1 in range(nR):
        for r2 in range(nR):
            for m in range(nM):
                if action[R_add[r1][r2]][m] != M_add[action[r1][m]][action[r2][m]]: return False, -1, -1, -1
                if action[R_mult[r1][r2]][m] != action[r1][action[r2][m]]: return False, -1, -1, -1
    for m in range(nM):
        if action[one_R][m] != m: return False, -1, -1, -1
    return True, zero_R, zero_M, one_R

def conditions(witness):
    try:
        # Allow a simple integer n to represent the ring Z/nZ and module Z/nZ
        if isinstance(witness, int):
            n = witness
            if n <= 0:
                return [False, False, False]
            R_add = [[(i+j)%n for j in range(n)] for i in range(n)]
            R_mult = [[(i*j)%n for j in range(n)] for i in range(n)]
            M_add = R_add
            action = R_mult
            
            true_T = set()
            for m in range(n):
                for r in range(n):
                    if r != 0 and action[r][m] == 0:
                        true_T.add(m)
                        break
            witness = {
                'R_add': R_add,
                'R_mult': R_mult,
                'M_add': M_add,
                'action': action,
                'T': list(true_T)
            }
            
        if not isinstance(witness, dict):
            return [False, False, False]
            
        R_add = witness.get('R_add')
        R_mult = witness.get('R_mult')
        M_add = witness.get('M_add')
        action = witness.get('action')
        T_list = witness.get('T')
        
        if R_add is None or R_mult is None or M_add is None or action is None or T_list is None:
            return [False, False, False]
            
        # H_1: M is an R-module
        mod_ok, zero_R, zero_M, one_R = is_module(R_add, R_mult, M_add, action)
        h1 = mod_ok
        
        # H_2: T is the set of all m \in M such that there exists a non-zero r \in R with rm = 0
        h2 = False
        if mod_ok:
            nR = len(R_add)
            nM = len(M_add)
            true_T = set()
            for m in range(nM):
                for r in range(nR):
                    if r != zero_R and action[r][m] == zero_M:
                        true_T.add(m)
                        break
            h2 = (set(T_list) == true_T)
            
        # ¬Q: T is NOT a submodule of M
        neg_q = False
        if mod_ok:
            T = set(T_list)
            if not T.issubset(set(range(len(M_add)))):
                neg_q = True
            elif zero_M not in T:
                neg_q = True
            else:
                is_submod = True
                for m1 in T:
                    for m2 in T:
                        if M_add[m1][m2] not in T:
                            is_submod = False
                            break
                    if not is_submod:
                        break
                if is_submod:
                    for r in range(len(R_add)):
                        for m in T:
                            if action[r][m] not in T:
                                is_submod = False
                                break
                        if not is_submod:
                            break
                neg_q = not is_submod
                
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: M is an R-module",
    "H_2: T is the set of all m in M such that there exists a non-zero r in R with rm = 0",
    "¬Q: T is not a submodule of M"
]

N_HYP = 2
NEG_Q_INDEX = 2