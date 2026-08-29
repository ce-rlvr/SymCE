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

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness['n']
            elements = list(witness['elements'])
            zero = witness['zero']
            add_op = witness['add']
            mul_op = witness['mul']
            I = list(witness['I'])
            J = list(witness['J'])
        else:
            n = witness.n
            elements = list(witness.elements)
            zero = witness.zero
            add_op = witness.add
            mul_op = witness.mul
            I = list(witness.I)
            J = list(witness.J)
            
        def add(a, b):
            if callable(add_op): return add_op(a, b)
            if isinstance(add_op, dict): return add_op[(a, b)]
            return add_op[elements.index(a)][elements.index(b)]
            
        def mul(a, b):
            if callable(mul_op): return mul_op(a, b)
            if isinstance(mul_op, dict): return mul_op[(a, b)]
            return mul_op[elements.index(a)][elements.index(b)]
            
    except Exception:
        return [False, False, False, False]

    h1 = True
    try:
        if zero not in elements:
            h1 = False
        else:
            n_elem = len(elements)
            try:
                elem_idx = {e: i for i, e in enumerate(elements)}
                get_idx = lambda e: elem_idx[e]
            except TypeError:
                get_idx = lambda e: elements.index(e)
                
            z_idx = get_idx(zero)
            
            add_table = []
            mul_table = []
            for a in elements:
                add_row = []
                mul_row = []
                for b in elements:
                    add_row.append(get_idx(add(a, b)))
                    mul_row.append(get_idx(mul(a, b)))
                add_table.append(add_row)
                mul_table.append(mul_row)
                
            for i in range(n_elem):
                if add_table[i][z_idx] != i or add_table[z_idx][i] != i:
                    h1 = False; break
            
            if h1:
                for i in range(n_elem):
                    has_inv = False
                    for j in range(n_elem):
                        if add_table[i][j] == z_idx and add_table[j][i] == z_idx:
                            has_inv = True
                            break
                    if not has_inv:
                        h1 = False; break
            
            if h1:
                for i in range(n_elem):
                    for j in range(n_elem):
                        if add_table[i][j] != add_table[j][i]:
                            h1 = False; break
                    if not h1: break
            
            if h1:
                for i in range(n_elem):
                    for j in range(n_elem):
                        for k in range(n_elem):
                            if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]:
                                h1 = False; break
                            if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]:
                                h1 = False; break
                            if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]:
                                h1 = False; break
                            if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]:
                                h1 = False; break
                        if not h1: break
                    if not h1: break
    except Exception:
        h1 = False

    try:
        h2 = isinstance(n, int) and not isinstance(n, bool) and n > 0
    except Exception:
        h2 = False

    try:
        if not h1:
            h3 = False
        else:
            def is_ideal(S_list):
                if not S_list: return False
                S_idx = set()
                for x in S_list:
                    try:
                        idx = get_idx(x)
                    except (ValueError, KeyError):
                        return False
                    S_idx.add(idx)
                
                for i in S_idx:
                    for j in S_idx:
                        if add_table[i][j] not in S_idx: return False
                    
                    has_inv = False
                    for j in S_idx:
                        if add_table[i][j] == z_idx and add_table[j][i] == z_idx:
                            has_inv = True
                            break
                    if not has_inv: return False
                    
                    for r in range(n_elem):
                        if mul_table[r][i] not in S_idx: return False
                        if mul_table[i][r] not in S_idx: return False
                return True

            h3 = is_ideal(I) and is_ideal(J)
    except Exception:
        h3 = False

    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            I_idx = [get_idx(x) for x in I]
            J_idx = [get_idx(x) for x in J]
            
            IJ_prods = set()
            for i in I_idx:
                for j in J_idx:
                    IJ_prods.add(mul_table[i][j])
            
            IJ = set(IJ_prods)
            while True:
                new_IJ = set(IJ)
                for x in IJ:
                    for y in IJ:
                        new_IJ.add(add_table[x][y])
                if len(new_IJ) == len(IJ):
                    break
                IJ = new_IJ
                
            Mn_IJ = set(itertools.product(IJ, repeat=n*n))
            
            MnI = list(itertools.product(I_idx, repeat=n*n))
            MnJ = list(itertools.product(J_idx, repeat=n*n))
            
            def mat_mul(A, B):
                C = []
                for i in range(n):
                    for j in range(n):
                        val = z_idx
                        for k in range(n):
                            val = add_table[val][mul_table[A[i*n+k]][B[k*n+j]]]
                        C.append(val)
                return tuple(C)
                
            AB_prods = set()
            for A in MnI:
                for B in MnJ:
                    AB_prods.add(mat_mul(A, B))
                    
            neg_q = (AB_prods != Mn_IJ)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: n is a positive integer",
    "H_3: I and J are ideals of R",
    "¬Q: M_n(I) M_n(J) != M_n(IJ)"
]

N_HYP = 3
NEG_Q_INDEX = 3