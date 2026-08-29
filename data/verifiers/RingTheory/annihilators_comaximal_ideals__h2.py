import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import z3
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are comaximal ideals of R",
    "H_3: M is an R-module",
    "¬Q: Ann_M(I \\cap J) != Ann_M(I) + Ann_M(J)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    witness must be a tuple: (R_size, R_add, R_mult, I, J, M_size, M_add, M_action)
    where:
      R_size, M_size are ints
      R_add, R_mult are list[list[int]] of size R_size x R_size
      I, J are list[int]
      M_add is list[list[int]] of size M_size x M_size
      M_action is list[list[int]] of size R_size x M_size
    """
    res = [False, False, False, False]
    try:
        if not isinstance(witness, tuple) or len(witness) != 8:
            return res
        R_size, R_add, R_mult, I, J, M_size, M_add, M_action = witness
        
        # Helper for abelian group
        def is_abelian_group(size, add):
            if not isinstance(size, int) or size <= 0: return False
            if len(add) != size: return False
            for row in add:
                if len(row) != size: return False
                for val in row:
                    if not (0 <= val < size): return False
            for i in range(size):
                for j in range(size):
                    for k in range(size):
                        if add[add[i][j]][k] != add[i][add[j][k]]: return False
            for i in range(size):
                for j in range(size):
                    if add[i][j] != add[j][i]: return False
            id_elem = -1
            for i in range(size):
                if all(add[i][j] == j for j in range(size)):
                    id_elem = i
                    break
            if id_elem == -1: return False
            for i in range(size):
                if not any(add[i][j] == id_elem for j in range(size)): return False
            return True

        # H1: R is a commutative ring
        try:
            h1 = False
            if is_abelian_group(R_size, R_add) and len(R_mult) == R_size:
                valid_mult = True
                for row in R_mult:
                    if len(row) != R_size: valid_mult = False
                    else:
                        for val in row:
                            if not (0 <= val < R_size): valid_mult = False
                if valid_mult:
                    assoc = True
                    comm = True
                    dist = True
                    for i in range(R_size):
                        for j in range(R_size):
                            if R_mult[i][j] != R_mult[j][i]: comm = False
                            for k in range(R_size):
                                if R_mult[R_mult[i][j]][k] != R_mult[i][R_mult[j][k]]: assoc = False
                                if R_mult[i][R_add[j][k]] != R_add[R_mult[i][j]][R_mult[i][k]]: dist = False
                    if assoc and comm and dist:
                        h1 = True
            res[0] = h1
        except Exception:
            pass

        # H2: I and J are comaximal ideals of R
        try:
            h2 = False
            I_set = set(I)
            J_set = set(J)
            if I_set and J_set and all(0 <= x < R_size for x in I_set) and all(0 <= x < R_size for x in J_set):
                def is_ideal(S):
                    for x in S:
                        for y in S:
                            if R_add[x][y] not in S: return False
                    for x in S:
                        for r in range(R_size):
                            if R_mult[r][x] not in S: return False
                    zero = -1
                    for i in range(R_size):
                        if all(R_add[i][j] == j for j in range(R_size)):
                            zero = i
                            break
                    if zero not in S: return False
                    for x in S:
                        inv = -1
                        for y in range(R_size):
                            if R_add[x][y] == zero:
                                inv = y
                                break
                        if inv not in S: return False
                    return True

                if is_ideal(I_set) and is_ideal(J_set):
                    sums = set()
                    for i in I_set:
                        for j in J_set:
                            sums.add(R_add[i][j])
                    if len(sums) == R_size:
                        h2 = True
            res[1] = h2
        except Exception:
            pass

        # H3: M is an R-module
        try:
            h3 = False
            if is_abelian_group(M_size, M_add) and len(M_action) == R_size:
                valid_action = True
                for row in M_action:
                    if len(row) != M_size: valid_action = False
                    else:
                        for val in row:
                            if not (0 <= val < M_size): valid_action = False
                if valid_action:
                    act_add_m = True
                    act_add_r = True
                    act_mult = True
                    for r in range(R_size):
                        for m1 in range(M_size):
                            for m2 in range(M_size):
                                if M_action[r][M_add[m1][m2]] != M_add[M_action[r][m1]][M_action[r][m2]]: act_add_m = False
                    for r1 in range(R_size):
                        for r2 in range(R_size):
                            for m in range(M_size):
                                if M_action[R_add[r1][r2]][m] != M_add[M_action[r1][m]][M_action[r2][m]]: act_add_r = False
                                if M_action[R_mult[r1][r2]][m] != M_action[r1][M_action[r2][m]]: act_mult = False
                    if act_add_m and act_add_r and act_mult:
                        h3 = True
            res[2] = h3
        except Exception:
            pass

        # neg_Q: Ann_M(I \cap J) != Ann_M(I) + Ann_M(J)
        try:
            neg_q = False
            I_set = set(I)
            J_set = set(J)
            I_cap_J = I_set.intersection(J_set)
            
            zero_M = -1
            for i in range(M_size):
                if all(M_add[i][j] == j for j in range(M_size)):
                    zero_M = i
                    break
                    
            def annihilator(S):
                ann = set()
                for m in range(M_size):
                    if all(M_action[s][m] == zero_M for s in S):
                        ann.add(m)
                return ann

            ann_I_cap_J = annihilator(I_cap_J)
            ann_I = annihilator(I_set)
            ann_J = annihilator(J_set)
            
            sum_ann = set()
            for m1 in ann_I:
                for m2 in ann_J:
                    sum_ann.add(M_add[m1][m2])
                    
            if ann_I_cap_J != sum_ann:
                neg_q = True
            res[3] = neg_q
        except Exception:
            pass

    except Exception:
        pass

    return res