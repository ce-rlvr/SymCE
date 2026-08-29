import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness) -> list[bool]:
    try:
        R_add = witness['R_add']
        R_mult = witness['R_mult']
        I = list(witness['I'])
        M_add = witness['M_add']
        M_action = witness['M_action']
    except Exception:
        return [False, False, False]

    def is_abelian_group(add_table):
        n = len(add_table)
        if n == 0: return False
        for row in add_table:
            if len(row) != n: return False
            if any(type(x) is not int or x < 0 or x >= n for x in row): return False
        for i in range(n):
            for j in range(n):
                if add_table[i][j] != add_table[j][i]: return False
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return False
        id_elem = -1
        for i in range(n):
            if all(add_table[i][j] == j for j in range(n)):
                id_elem = i
                break
        if id_elem != 0: return False
        for i in range(n):
            if not any(add_table[i][j] == 0 for j in range(n)): return False
        return True

    def is_ring(R_add, R_mult):
        if not is_abelian_group(R_add): return False
        n = len(R_add)
        if len(R_mult) != n: return False
        for row in R_mult:
            if len(row) != n: return False
            if any(type(x) is not int or x < 0 or x >= n for x in row): return False
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if R_mult[R_mult[i][j]][k] != R_mult[i][R_mult[j][k]]: return False
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if R_mult[i][R_add[j][k]] != R_add[R_mult[i][j]][R_mult[i][k]]: return False
                    if R_mult[R_add[i][j]][k] != R_add[R_mult[i][k]][R_mult[j][k]]: return False
        return True

    def is_left_module(R_add, R_mult, M_add, M_action):
        if not is_abelian_group(M_add): return False
        nR = len(R_add)
        nM = len(M_add)
        if len(M_action) != nR: return False
        for row in M_action:
            if len(row) != nM: return False
            if any(type(x) is not int or x < 0 or x >= nM for x in row): return False
        for r in range(nR):
            for m1 in range(nM):
                for m2 in range(nM):
                    if M_action[r][M_add[m1][m2]] != M_add[M_action[r][m1]][M_action[r][m2]]: return False
        for r1 in range(nR):
            for r2 in range(nR):
                for m in range(nM):
                    if M_action[R_add[r1][r2]][m] != M_add[M_action[r1][m]][M_action[r2][m]]: return False
                    if M_action[R_mult[r1][r2]][m] != M_action[r1][M_action[r2][m]]: return False
        return True

    def is_ideal(R_add, R_mult, I):
        if not I: return False
        n = len(R_add)
        if any(type(x) is not int or x < 0 or x >= n for x in I): return False
        for i in I:
            for j in I:
                if R_add[i][j] not in I: return False
        for i in I:
            inv = -1
            for j in range(n):
                if R_add[i][j] == 0:
                    inv = j
                    break
            if inv not in I: return False
        for i in I:
            for r in range(n):
                if R_mult[r][i] not in I: return False
                if R_mult[i][r] not in I: return False
        return True

    try:
        h1 = is_ring(R_add, R_mult) and is_left_module(R_add, R_mult, M_add, M_action)
    except Exception:
        h1 = False

    try:
        h2 = is_ideal(R_add, R_mult, I)
    except Exception:
        h2 = False

    try:
        nR = len(R_add)
        nM = len(M_add)
        valid_fs = []
        
        def search(r, current_f):
            if r > 0:
                last = r - 1
                for x in range(r):
                    if R_add[x][last] < r:
                        if current_f[R_add[x][last]] != M_add[current_f[x]][current_f[last]]: return
                    if R_add[last][x] < r:
                        if current_f[R_add[last][x]] != M_add[current_f[last]][current_f[x]]: return
                    if R_mult[last][x] < r:
                        if current_f[R_mult[last][x]] != M_action[last][current_f[x]]: return
                for s in range(nR):
                    if R_mult[s][last] < r:
                        if current_f[R_mult[s][last]] != M_action[s][current_f[last]]: return
            
            if r == nR:
                for x in range(nR):
                    for y in range(nR):
                        if current_f[R_add[x][y]] != M_add[current_f[x]][current_f[y]]: return
                for s in range(nR):
                    for x in range(nR):
                        if current_f[R_mult[s][x]] != M_action[s][current_f[x]]: return
                valid_fs.append(tuple(current_f))
                return
                
            if r in I:
                search(r + 1, current_f + [0])
            else:
                for m in range(nM):
                    search(r + 1, current_f + [m])
                    
        search(0, [])
        
        ann_ms = []
        for m in range(nM):
            is_ann = True
            for i in I:
                if M_action[i][m] != 0:
                    is_ann = False
                    break
            if is_ann:
                ann_ms.append(m)
                
        def get_orders(elements, add_func):
            orders = []
            max_order = len(elements) + 1
            for e in elements:
                curr = e
                order = 1
                while True:
                    if isinstance(curr, tuple) and all(x == 0 for x in curr):
                        break
                    if type(curr) is int and curr == 0:
                        break
                    curr = add_func(curr, e)
                    order += 1
                    if order > max_order:
                        break
                orders.append(order)
            return sorted(orders)
            
        def hom_add(f1, f2):
            return tuple(M_add[f1[i]][f2[i]] for i in range(len(f1)))
            
        def ann_add(m1, m2):
            return M_add[m1][m2]
            
        orders1 = get_orders(valid_fs, hom_add)
        orders2 = get_orders(ann_ms, ann_add)
        
        neg_q = (orders1 != orders2)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring and M is a left R-module",
    "H_2: I is a two-sided ideal of R",
    "¬Q: Hom_R(R/I, M) is not isomorphic to Ann_M(I)"
]

N_HYP = 2
NEG_Q_INDEX = 2