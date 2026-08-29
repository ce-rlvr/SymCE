import itertools
import math
import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import functools

# Top-level setup
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

def get_all_matrices_tuple(S, n):
    rows = list(itertools.product(S, repeat=n))
    matrices = list(itertools.product(rows, repeat=n))
    return matrices

def check_dict_witness(w):
    try:
        req_keys = ['R_size', 'add', 'mul', 'n', 'I', 'J']
        if not all(k in w for k in req_keys): return [False, False, False, False]
        
        size = w['R_size']
        add = w['add']
        mul = w['mul']
        
        h1 = True
        if not isinstance(size, int) or size <= 0: h1 = False
        if h1 and (len(add) != size or any(len(row) != size for row in add)): h1 = False
        if h1 and (len(mul) != size or any(len(row) != size for row in mul)): h1 = False
        
        if h1:
            for i in range(size):
                for j in range(size):
                    if not (0 <= add[i][j] < size): h1 = False
                    if not (0 <= mul[i][j] < size): h1 = False
                    if add[i][j] != add[j][i]: h1 = False
                    
        if h1:
            for i in range(size):
                for j in range(size):
                    for k in range(size):
                        if add[add[i][j]][k] != add[i][add[j][k]]: h1 = False
                        if mul[mul[i][j]][k] != mul[i][mul[j][k]]: h1 = False
                        if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: h1 = False
                        if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: h1 = False
                        
        if h1:
            zero = -1
            for i in range(size):
                if all(add[i][j] == j for j in range(size)):
                    zero = i
                    break
            if zero == -1: h1 = False
            else:
                for i in range(size):
                    if not any(add[i][j] == zero for j in range(size)): h1 = False
                    
        if h1:
            for subset in (w['I'], w['J']):
                if not isinstance(subset, list): h1 = False
                elif not all(isinstance(x, int) and 0 <= x < size for x in subset): h1 = False
    except Exception:
        h1 = False

    try:
        h2 = isinstance(w.get('n'), int) and w['n'] > 0
    except Exception:
        h2 = False

    try:
        h3 = h1 and h2
    except Exception:
        h3 = False

    neg_q = False
    try:
        if h1 and h2:
            n = w['n']
            I = w['I']
            J = w['J']
            
            if len(I)**(n*n) > 4096 or len(J)**(n*n) > 4096:
                return [h1, h2, h3, False]
                
            products_IJ = set()
            for x in I:
                for y in J:
                    products_IJ.add(mul[x][y])
            IJ = set(products_IJ)
            changed = True
            while changed:
                changed = False
                new_elements = set()
                for a in IJ:
                    for b in IJ:
                        s = add[a][b]
                        if s not in IJ:
                            new_elements.add(s)
                if new_elements:
                    IJ.update(new_elements)
                    changed = True
            IJ = list(IJ)
            
            Mn_IJ = set(get_all_matrices_tuple(IJ, n))
            
            MnI = get_all_matrices_tuple(I, n)
            MnJ = get_all_matrices_tuple(J, n)
            
            products_Mn = set()
            for A in MnI:
                for B in MnJ:
                    C = []
                    for i in range(n):
                        row = []
                        for j in range(n):
                            s = mul[A[i][0]][B[0][j]]
                            for k in range(1, n):
                                s = add[s][mul[A[i][k]][B[k][j]]]
                            row.append(s)
                        C.append(tuple(row))
                    products_Mn.add(tuple(C))
                    
            MnI_MnJ = set(products_Mn)
            changed = True
            while changed:
                changed = False
                new_elements = set()
                for A in MnI_MnJ:
                    for B in MnI_MnJ:
                        C = []
                        for i in range(n):
                            row = []
                            for j in range(n):
                                row.append(add[A[i][j]][B[i][j]])
                            C.append(tuple(row))
                        S = tuple(C)
                        if S not in MnI_MnJ:
                            new_elements.add(S)
                if new_elements:
                    MnI_MnJ.update(new_elements)
                    changed = True
                    
            neg_q = (MnI_MnJ != Mn_IJ)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        return check_dict_witness(witness)
    else:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: n is a positive integer",
    "H_3: M_n(R) is the ring of n \\times n matrices over R",
    "¬Q: M_n(I) M_n(J) != M_n(IJ)"
]

N_HYP = 3
NEG_Q_INDEX = 3