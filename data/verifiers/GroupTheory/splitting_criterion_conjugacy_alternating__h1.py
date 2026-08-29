import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness):
    try:
        C = list(witness)
    except Exception:
        return [False, False, False]
        
    if not C:
        return [False, False, False]
        
    try:
        if not all(isinstance(p, Permutation) for p in C):
            return [False, False, False]
        
        n = C[0].size
        if not all(p.size == n for p in C):
            return [False, False, False]
            
        p0 = C[0]
        struct = p0.cycle_structure
        
        h1 = True
        for p in C:
            if p.cycle_structure != struct:
                h1 = False
                break
        
        if h1:
            fixed_points = n - sum(k * m for k, m in struct.items())
            cent_size = math.factorial(fixed_points)
            for k, m in struct.items():
                cent_size *= (k ** m) * math.factorial(m)
            
            expected_size = math.factorial(n) // cent_size
            
            if len(C) == expected_size and len(set(C)) == expected_size:
                h1 = True
            else:
                h1 = False
    except Exception:
        h1 = False

    try:
        p0 = C[0]
        n = p0.size
        struct = p0.cycle_structure
        fixed_points = n - sum(k * m for k, m in struct.items())
        
        h2 = True
        if fixed_points > 1:
            h2 = False
        for k, m in struct.items():
            if k % 2 == 0:
                h2 = False
            if m > 1:
                h2 = False
    except Exception:
        h2 = False

    try:
        p0 = C[0]
        n = p0.size
        
        if n <= 1:
            neg_Q = True
        else:
            if p0.is_even:
                struct = p0.cycle_structure
                fixed_points = n - sum(k * m for k, m in struct.items())
                
                has_odd_perm_in_cent = False
                if fixed_points >= 2:
                    has_odd_perm_in_cent = True
                for k, m in struct.items():
                    if k % 2 == 0:
                        has_odd_perm_in_cent = True
                    if m >= 2 and k % 2 != 0:
                        has_odd_perm_in_cent = True
                
                if has_odd_perm_in_cent:
                    splits_into_two = False
                else:
                    splits_into_two = True
                
                neg_Q = not splits_into_two
            else:
                neg_Q = True
    except Exception:
        neg_Q = False

    return [h1, h2, neg_Q]

CONDITION_LABELS = [
    "H_1: C is a conjugacy class of the symmetric group S_n",
    "H_2: The cycle lengths in the disjoint cycle decomposition of the elements in C are distinct odd integers, including cycles of length 1",
    "¬Q: C is not a disjoint union of exactly two conjugacy classes of A_n of the same size"
]

N_HYP = 2
NEG_Q_INDEX = 2