import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_ring(elements, add, mul, zero, one):
    n = len(elements)
    for i in range(n):
        if add[i][zero] != i or add[zero][i] != i: return False
    for i in range(n):
        if mul[i][one] != i or mul[one][i] != i: return False
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False
            for k in range(n):
                if add[i][add[j][k]] != add[add[i][j]][k]: return False
    for i in range(n):
        has_inv = False
        for j in range(n):
            if add[i][j] == zero:
                has_inv = True
                break
        if not has_inv: return False
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[i][mul[j][k]] != mul[mul[i][j]][k]: return False
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False
    return True

def is_n_graded(elements, add, mul, zero, components):
    n = len(elements)
    for i in range(n):
        s = zero
        for d, x_d in components[i].items():
            s = add[s][x_d]
        if s != i: return False
        
    R_d = {}
    for i in range(n):
        for d, x_d in components[i].items():
            if x_d != zero:
                if d not in R_d:
                    R_d[d] = set()
                R_d[d].add(x_d)
                
    for d, subset in R_d.items():
        for x in subset:
            for cd, cx in components[x].items():
                if cx != zero and cd != d:
                    return False
                    
    for d, subset in R_d.items():
        for x in subset:
            for y in subset:
                s = add[x][y]
                if s != zero:
                    for cd, cx in components[s].items():
                        if cx != zero and cd != d:
                            return False
                            
    for c, subset_c in R_d.items():
        for d, subset_d in R_d.items():
            for x in subset_c:
                for y in subset_d:
                    p = mul[x][y]
                    if p != zero:
                        for pd, px in components[p].items():
                            if px != zero and pd != c + d:
                                return False
    return True

def conditions(witness):
    h1_ok = False
    neg_q_ok = False
    
    try:
        if isinstance(witness, dict):
            elements = witness['elements']
            add = witness['add']
            mul = witness['mul']
            zero = witness['zero']
            one = witness['one']
            components = witness['components']
        else:
            elements = witness.elements
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            one = witness.one
            components = witness.components

        if isinstance(elements, int):
            elements = list(range(elements))
            
        n = len(elements)
        
        norm_components = []
        for i in range(n):
            comp = components[i]
            norm_comp = {}
            for d, x_d in comp.items():
                d_int = int(d)
                if d_int < 0:
                    raise ValueError("Degrees must be non-negative")
                norm_comp[d_int] = x_d
            norm_components.append(norm_comp)
            
        if is_ring(elements, add, mul, zero, one):
            if is_n_graded(elements, add, mul, zero, norm_components):
                h1_ok = True
    except Exception:
        h1_ok = False

    try:
        if isinstance(witness, dict):
            elements = witness['elements']
            mul = witness['mul']
            zero = witness['zero']
            one = witness['one']
            components = witness['components']
        else:
            elements = witness.elements
            mul = witness.mul
            zero = witness.zero
            one = witness.one
            components = witness.components

        if isinstance(elements, int):
            elements = list(range(elements))
            
        n = len(elements)
        
        norm_components = []
        for i in range(n):
            comp = components[i]
            norm_comp = {}
            for d, x_d in comp.items():
                d_int = int(d)
                if d_int < 0:
                    raise ValueError("Degrees must be non-negative")
                norm_comp[d_int] = x_d
            norm_components.append(norm_comp)
            
        units = []
        for i in range(n):
            for j in range(n):
                if mul[i][j] == one and mul[j][i] == one:
                    units.append(i)
                    break
        
        for u in units:
            in_R0 = True
            for d, x_d in norm_components[u].items():
                if x_d != zero and d != 0:
                    in_R0 = False
                    break
            if not in_R0:
                neg_q_ok = True
                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is an N-graded ring",
    "¬Q: U(R) is not contained entirely within R_0"
]

N_HYP = 1
NEG_Q_INDEX = 1