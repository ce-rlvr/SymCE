import itertools
import math
import functools
import sympy
from sympy.matrices import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    "H_1: R is a commutative ring with identity",
    "H_2: I + J = R",
    "¬Q: The sum of the radical of I and the radical of J is not equal to R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            elements = witness['elements']
            add = witness['add']
            mul = witness['mul']
            I = witness['I']
            J = witness['J']
        elif isinstance(witness, tuple) and len(witness) == 5:
            elements, add, mul, I, J = witness
        else:
            elements = witness.elements
            add = witness.add
            mul = witness.mul
            I = witness.I
            J = witness.J
            
        n = len(elements)
        if n == 0:
            return [False, False, False]
            
        # H1: Commutative ring with identity
        is_ring = True
        
        if len(add) != n or len(mul) != n:
            is_ring = False
        for row in add:
            if len(row) != n: is_ring = False
        for row in mul:
            if len(row) != n: is_ring = False
            
        if not is_ring:
            return [False, False, False]
            
        for i in range(n):
            for j in range(n):
                if add[i][j] != add[j][i]: is_ring = False
                if mul[i][j] != mul[j][i]: is_ring = False
                
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if add[add[i][j]][k] != add[i][add[j][k]]: is_ring = False
                    if mul[mul[i][j]][k] != mul[i][mul[j][k]]: is_ring = False
                    
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: is_ring = False
                    
        zero = None
        for i in range(n):
            if all(add[i][j] == j for j in range(n)):
                zero = i
                break
        if zero is None:
            is_ring = False
            
        if zero is not None:
            for i in range(n):
                if not any(add[i][j] == zero for j in range(n)):
                    is_ring = False
                    
        one = None
        for i in range(n):
            if all(mul[i][j] == j for j in range(n)):
                one = i
                break
        if one is None:
            is_ring = False
            
        h1 = is_ring
        
        elem_list = list(elements)
        I_idx = [elem_list.index(x) for x in I]
        J_idx = [elem_list.index(x) for x in J]
        
        I_plus_J = set()
        for i in I_idx:
            for j in J_idx:
                I_plus_J.add(add[i][j])
                
        h2 = (len(I_plus_J) == n)
        
        def radical(S_idx):
            rad = set()
            for x in range(n):
                curr = x
                for _ in range(n):
                    if curr in S_idx:
                        rad.add(x)
                        break
                    curr = mul[curr][x]
            return rad
            
        rad_I = radical(I_idx)
        rad_J = radical(J_idx)
        
        rad_I_plus_rad_J = set()
        for i in rad_I:
            for j in rad_J:
                rad_I_plus_rad_J.add(add[i][j])
                
        neg_q = (len(rad_I_plus_rad_J) != n)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]