import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
import itertools
import functools
import math

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
            n = witness['n']
            add = witness['add']
            mul = witness['mul']
            I = set(witness['I'])
        else:
            n, add, mul, I_list = witness
            I = set(I_list)
            
        zero = None
        for i in range(n):
            if all(add[i][j] == j for j in range(n)) and all(add[j][i] == j for j in range(n)):
                zero = i
                break
        if zero is None:
            return [False, False, False]
            
        h1 = True
        if not I:
            h1 = False
        else:
            for a in I:
                for b in I:
                    if add[a][b] not in I:
                        h1 = False
                has_inv = False
                for b in I:
                    if add[a][b] == zero and add[b][a] == zero:
                        has_inv = True
                if not has_inv:
                    h1 = False
                for r in range(n):
                    if mul[r][a] not in I or mul[a][r] not in I:
                        h1 = False
                        
        h2 = True
        for r in range(n):
            in_rad = False
            curr = r
            for _ in range(n + 1):
                if curr in I:
                    in_rad = True
                    break
                curr = mul[curr][r]
            if not in_rad:
                h2 = False
                break
                
        neg_q = I != set(range(n))
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: The radical of I is equal to R",
    "¬Q: I != R"
]

N_HYP = 2
NEG_Q_INDEX = 2