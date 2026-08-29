import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import Matrix
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        matrices = list(witness)
    except Exception:
        return [False, False]
    
    if not matrices:
        return [False, False]
        
    h1 = True
    try:
        for m in matrices:
            if not hasattr(m, 'shape') or m.shape != (3, 3):
                h1 = False
                break
            if m[1, 0] != m[2, 0] or m[1, 0] != m[2, 1]:
                h1 = False
                break
            if m[0, 0] != m[1, 1] or m[0, 0] != m[2, 2]:
                h1 = False
                break
    except Exception:
        h1 = False
        
    h2 = False
    if h1:
        try:
            m0 = matrices[0]
            zero = m0[1, 0]
            one = m0[0, 0]
            
            F_elements = []
            for m in matrices:
                if m[0, 1] not in F_elements:
                    F_elements.append(m[0, 1])
                    
            if len(matrices) == len(F_elements) ** 3:
                valid_form = True
                for m in matrices:
                    if m[0, 1] not in F_elements or m[1, 2] not in F_elements or m[0, 2] not in F_elements:
                        valid_form = False
                        break
                    if m[0, 0] != one or m[1, 1] != one or m[2, 2] != one:
                        valid_form = False
                        break
                    if m[1, 0] != zero or m[2, 0] != zero or m[2, 1] != zero:
                        valid_form = False
                        break
                        
                if valid_form:
                    def get_idx(val):
                        for i, v in enumerate(F_elements):
                            if v == val:
                                return i
                        return -1
                        
                    mat_to_tup = []
                    h2_temp = True
                    for m in matrices:
                        ix = get_idx(m[0, 1])
                        iy = get_idx(m[1, 2])
                        iz = get_idx(m[0, 2])
                        if ix == -1 or iy == -1 or iz == -1:
                            h2_temp = False
                            break
                        mat_to_tup.append((ix, iy, iz))
                        
                    if h2_temp:
                        tup_to_mat_idx = {tup: i for i, tup in enumerate(mat_to_tup)}
                        if len(tup_to_mat_idx) == len(matrices):
                            h2 = True
                            
            if h2:
                add_table = {}
                mul_table = {}
                for i, x in enumerate(F_elements):
                    for j, y in enumerate(F_elements):
                        try:
                            s = x + y
                            s_idx = get_idx(s)
                        except Exception:
                            s_idx = -1
                        add_table[(i, j)] = s_idx
                        
                        try:
                            p = x * y
                            p_idx = get_idx(p)
                        except Exception:
                            p_idx = -1
                        mul_table[(i, j)] = p_idx
                        
                for i in range(len(F_elements)):
                    for j in range(len(F_elements)):
                        if add_table[(i, j)] == -1 or mul_table[(i, j)] == -1:
                            h2 = False
                            break
                    if not h2: break
                    
            if h2:
                idx_zero = get_idx(zero)
                if idx_zero == -1:
                    h2 = False
                    
            if h2:
                for i in range(len(F_elements)):
                    if add_table[(i, idx_zero)] != i or add_table[(idx_zero, i)] != i:
                        h2 = False
                        break
                        
            if h2:
                for i in range(len(F_elements)):
                    for j in range(len(F_elements)):
                        for k in range(len(F_elements)):
                            if add_table[(add_table[(i, j)], k)] != add_table[(i, add_table[(j, k)])]:
                                h2 = False
                                break
                        if not h2: break
                    if not h2: break
                    
            if h2:
                for i in range(len(F_elements)):
                    for j in range(len(F_elements)):
                        for k in range(len(F_elements)):
                            if mul_table[(mul_table[(i, j)], k)] != mul_table[(i, mul_table[(j, k)])]:
                                h2 = False
                                break
                        if not h2: break
                    if not h2: break
                    
            if h2:
                for i in range(len(F_elements)):
                    for j in range(len(F_elements)):
                        for k in range(len(F_elements)):
                            left = mul_table[(i, add_table[(j, k)])]
                            right = add_table[(mul_table[(i, j)], mul_table[(i, k)])]
                            if left != right:
                                h2 = False
                                break
                            left2 = mul_table[(add_table[(i, j)], k)]
                            right2 = add_table[(mul_table[(i, k)], mul_table[(j, k)])]
                            if left2 != right2:
                                h2 = False
                                break
                        if not h2: break
                    if not h2: break
                    
            if h2:
                for i in range(len(F_elements)):
                    for j in range(len(F_elements)):
                        if add_table[(i, j)] != add_table[(j, i)]:
                            h2 = False
                            break
                    if not h2: break
                    
            if h2:
                for i in range(len(F_elements)):
                    has_inv = False
                    for j in range(len(F_elements)):
                        if add_table[(i, j)] == idx_zero:
                            has_inv = True
                            break
                    if not has_inv:
                        h2 = False
                        break
        except Exception:
            h2 = False
            
    neg_q = False
    if h1 and h2:
        try:
            def mul_tup(t1, t2):
                x3 = add_table[(t1[0], t2[0])]
                y3 = add_table[(t1[1], t2[1])]
                z1_plus_z2 = add_table[(t1[2], t2[2])]
                x1_times_y2 = mul_table[(t1[0], t2[1])]
                z3 = add_table[(z1_plus_z2, x1_times_y2)]
                return (x3, y3, z3)
                
            add_inv = {}
            for i in range(len(F_elements)):
                for j in range(len(F_elements)):
                    if add_table[(i, j)] == idx_zero:
                        add_inv[i] = j
                        break
                        
            def get_inv_tup(t):
                ix, iy, iz = t
                neg_x = add_inv[ix]
                neg_y = add_inv[iy]
                neg_z = add_inv[iz]
                xy = mul_table[(ix, iy)]
                z_inv = add_table[(neg_z, xy)]
                return (neg_x, neg_y, z_inv)
                
            generators = []
            for i in range(len(F_elements)):
                generators.append((i, idx_zero, idx_zero))
                generators.append((idx_zero, i, idx_zero))
                
            Z_tups = []
            for c in tup_to_mat_idx.keys():
                is_center = True
                for g in generators:
                    if mul_tup(c, g) != mul_tup(g, c):
                        is_center = False
                        break
                if is_center:
                    Z_tups.append(c)
                    
            C_tups = set()
            xy_elements = []
            for i in range(len(F_elements)):
                for j in range(len(F_elements)):
                    xy_elements.append((i, j, idx_zero))
                    
            for g in xy_elements:
                for h in xy_elements:
                    g_inv = get_inv_tup(g)
                    h_inv = get_inv_tup(h)
                    p1 = mul_tup(g_inv, h_inv)
                    p2 = mul_tup(p1, g)
                    comm = mul_tup(p2, h)
                    C_tups.add(comm)
                    
            commutator_subgroup = set(C_tups)
            added = True
            max_iters = len(tup_to_mat_idx)
            iters = 0
            while added and iters < max_iters:
                iters += 1
                added = False
                new_elements = set()
                for a in commutator_subgroup:
                    for b in C_tups:
                        prod = mul_tup(a, b)
                        if prod not in commutator_subgroup and prod not in new_elements:
                            new_elements.add(prod)
                if new_elements:
                    commutator_subgroup.update(new_elements)
                    added = True
                    
            neg_q = set(Z_tups) != commutator_subgroup
        except Exception:
            neg_q = False
            
    return [bool(h1 and h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: The witness is the Heisenberg group H(F) over some ring F",
    "¬Q: The commutator subgroup of H(F) is not equal to the center Z(H(F))"
]
N_HYP = 1
NEG_Q_INDEX = 1