import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
import itertools
import math
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

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: I and J are comaximal, meaning I + J = R",
    "¬Q: The tensor product R/I \\otimes_R R/J is not isomorphic to the zero module"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness can be provided in several formats:
      - A dictionary with 'n', 'add', 'mul', 'I', 'J' (tables format)
      - A dictionary with 'R', 'I', 'J' and optionally 'add', 'mul' functions
      - An object with attributes R, I, J, add, mul
      - A tuple (R_elems, I_elems, J_elems)
      - A tuple (R_elems, add_func, mul_func, I_elems, J_elems)
      - A tuple (n, add_table, mul_table, I_indices, J_indices)
    """
    try:
        parsed = False
        if isinstance(witness, dict):
            if 'R' in witness:
                R_elems = witness['R']
                I_elems = witness['I']
                J_elems = witness['J']
                add_func = witness.get('add', lambda a, b: a + b)
                mul_func = witness.get('mul', lambda a, b: a * b)
                parsed = True
            elif 'n' in witness:
                n = witness['n']
                add = witness['add']
                mul = witness['mul']
                I = witness['I']
                J = witness['J']
                parsed = 'tables'
        elif hasattr(witness, 'R') and hasattr(witness, 'I') and hasattr(witness, 'J'):
            R_elems = witness.R
            I_elems = witness.I
            J_elems = witness.J
            add_func = getattr(witness, 'add', lambda a, b: a + b)
            mul_func = getattr(witness, 'mul', lambda a, b: a * b)
            parsed = True
        elif isinstance(witness, tuple) or isinstance(witness, list):
            if len(witness) == 3:
                R_elems, I_elems, J_elems = witness
                add_func = lambda a, b: a + b
                mul_func = lambda a, b: a * b
                parsed = True
            elif len(witness) == 5:
                if callable(witness[1]):
                    R_elems, add_func, mul_func, I_elems, J_elems = witness
                    parsed = True
                else:
                    n, add, mul, I, J = witness
                    parsed = 'tables'
                    
        if parsed is True:
            n = len(R_elems)
            def get_idx(e):
                for i, x in enumerate(R_elems):
                    if x == e: return i
                raise ValueError("Element not found")
            add = [[0]*n for _ in range(n)]
            mul = [[0]*n for _ in range(n)]
            for i, a in enumerate(R_elems):
                for j, b in enumerate(R_elems):
                    add[i][j] = get_idx(add_func(a, b))
                    mul[i][j] = get_idx(mul_func(a, b))
            I = [get_idx(e) for e in I_elems]
            J = [get_idx(e) for e in J_elems]
        elif parsed != 'tables':
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

    try:
        def is_ring():
            for i in range(n):
                for j in range(n):
                    if add[i][j] != add[j][i]: return False
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if add[add[i][j]][k] != add[i][add[j][k]]: return False
            id_add = -1
            for i in range(n):
                if all(add[i][j] == j and add[j][i] == j for j in range(n)):
                    id_add = i
                    break
            if id_add == -1: return False
            for i in range(n):
                if not any(add[i][j] == id_add for j in range(n)): return False
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                        if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False
            return id_add

        id_add = is_ring()
        if id_add is False:
            h1_ok = False
        else:
            def is_ideal(S):
                if not S: return False
                if id_add not in S: return False
                for x in S:
                    for y in S:
                        if add[x][y] not in S: return False
                for x in S:
                    for r in range(n):
                        if mul[x][r] not in S: return False
                        if mul[r][x] not in S: return False
                for x in S:
                    has_inv = False
                    for y in range(n):
                        if add[x][y] == id_add:
                            if y not in S: return False
                            has_inv = True
                            break
                    if not has_inv: return False
                return True
            
            h1_ok = is_ideal(I) and is_ideal(J)
            
    except Exception:
        h1_ok = False

    try:
        if not h1_ok:
            h2_ok = False
        else:
            sums = set()
            for i in I:
                for j in J:
                    sums.add(add[i][j])
            h2_ok = (len(sums) == n)
    except Exception:
        h2_ok = False

    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            def get_quotient_maps(S):
                cosets = []
                element_to_coset = {}
                for i in range(n):
                    if i not in element_to_coset:
                        c_idx = len(cosets)
                        coset = []
                        for s in S:
                            val = add[i][s]
                            if val not in element_to_coset:
                                element_to_coset[val] = c_idx
                                coset.append(val)
                        cosets.append(coset)
                return cosets, element_to_coset

            cosets_I, map_I = get_quotient_maps(I)
            cosets_J, map_J = get_quotient_maps(J)
            
            N_I = len(cosets_I)
            N_J = len(cosets_J)
            V = N_I * N_J
            
            if V <= 1:
                is_zero = True
            else:
                relations = []
                for i1 in range(N_I):
                    for i2 in range(N_I):
                        rep1 = cosets_I[i1][0]
                        rep2 = cosets_I[i2][0]
                        sum_rep = add[rep1][rep2]
                        i_sum = map_I[sum_rep]
                        for j in range(N_J):
                            row = [0] * V
                            row[i_sum * N_J + j] += 1
                            row[i1 * N_J + j] -= 1
                            row[i2 * N_J + j] -= 1
                            relations.append(row)
                            
                for j1 in range(N_J):
                    for j2 in range(N_J):
                        rep1 = cosets_J[j1][0]
                        rep2 = cosets_J[j2][0]
                        sum_rep = add[rep1][rep2]
                        j_sum = map_J[sum_rep]
                        for i in range(N_I):
                            row = [0] * V
                            row[i * N_J + j_sum] += 1
                            row[i * N_J + j1] -= 1
                            row[i * N_J + j2] -= 1
                            relations.append(row)
                            
                for i in range(N_I):
                    for j in range(N_J):
                        for r in range(n):
                            rep_i = cosets_I[i][0]
                            rep_j = cosets_J[j][0]
                            ur_rep = mul[rep_i][r]
                            rv_rep = mul[r][rep_j]
                            i_ur = map_I[ur_rep]
                            j_rv = map_J[rv_rep]
                            row = [0] * V
                            row[i_ur * N_J + j] += 1
                            row[i * N_J + j_rv] -= 1
                            relations.append(row)
                            
                def is_trivial_group(rels, V):
                    rows = len(rels)
                    cols = V
                    A = [list(row) for row in rels]
                    for i in range(V):
                        while True:
                            pivot_r, pivot_c = -1, -1
                            for r in range(i, rows):
                                for c in range(i, cols):
                                    if A[r][c] != 0:
                                        if pivot_r == -1 or abs(A[r][c]) < abs(A[pivot_r][pivot_c]):
                                            pivot_r, pivot_c = r, c
                            if pivot_r == -1:
                                break
                            A[i], A[pivot_r] = A[pivot_r], A[i]
                            for r in range(rows):
                                A[r][i], A[r][pivot_c] = A[r][pivot_c], A[r][i]
                            changed = False
                            for r in range(i + 1, rows):
                                if A[r][i] != 0:
                                    q = A[r][i] // A[i][i]
                                    for c in range(i, cols):
                                        A[r][c] -= q * A[i][c]
                                    changed = True
                            for c in range(i + 1, cols):
                                if A[i][c] != 0:
                                    q = A[i][c] // A[i][i]
                                    for r in range(i, rows):
                                        A[r][c] -= q * A[r][i]
                                    changed = True
                            if not changed:
                                break
                        if A[i][i] == 0 or abs(A[i][i]) != 1:
                            return False
                    return True

                is_zero = is_trivial_group(relations, V)
            
            neg_q_ok = not is_zero
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]