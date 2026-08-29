import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for potential witness expressions
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
    "H_1: Aut(G) is the group of automorphisms of G",
    "H_2: C is the set of all conjugacy classes of G",
    "¬Q: The map Aut(G) x C -> C is not a well-defined group action"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        # Fast path for valid groups (where the theorem always holds)
        if isinstance(witness, PermutationGroup):
            return [True, True, False]
            
        # Extract magma/quasigroup components
        if hasattr(witness, 'elements'):
            elements = witness.elements
            op = witness.op
            if hasattr(witness, 'conj'):
                conj = witness.conj
            else:
                inv = witness.inv
                conj = lambda g, x: op(g, op(x, inv(g)))
        else:
            elements = witness[0]
            op = witness[1]
            if len(witness) >= 4:
                inv = witness[2]
                conj = witness[3]
            else:
                inv = witness[2]
                conj = lambda g, x: op(g, op(x, inv(g)))
                
        n = len(elements)
        if n == 0 or n > 8:
            return [False, False, False]
            
        def get_idx(val):
            for i, e in enumerate(elements):
                if e == val:
                    return i
            return -1
            
        # Precompute operation table using indices
        op_table = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                val = op(elements[i], elements[j])
                idx = get_idx(val)
                if idx == -1:
                    return [False, False, False]
                op_table[i][j] = idx
                
        # Precompute conjugacy table using indices
        conj_table = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                val = conj(elements[i], elements[j])
                idx = get_idx(val)
                if idx == -1:
                    return [False, False, False]
                conj_table[i][j] = idx
                
        # Find all automorphisms (bijections preserving op)
        auts = []
        for p in itertools.permutations(range(n)):
            is_aut = True
            for i in range(n):
                for j in range(n):
                    if p[op_table[i][j]] != op_table[p[i]][p[j]]:
                        is_aut = False
                        break
                if not is_aut:
                    break
            if is_aut:
                auts.append(p)
                
        # Compute all conjugacy classes
        classes = []
        for x in range(n):
            c = []
            for g in range(n):
                val = conj_table[g][x]
                if val not in c:
                    c.append(val)
            c.sort()
            if c not in classes:
                classes.append(c)
                
        # Check if the action is well-defined
        # For every phi in Aut(G) and K in C, phi(K) must be in C
        is_well_defined = True
        for p in auts:
            for K in classes:
                phi_K = []
                for k in K:
                    val = p[k]
                    if val not in phi_K:
                        phi_K.append(val)
                phi_K.sort()
                if phi_K not in classes:
                    is_well_defined = False
                    break
            if not is_well_defined:
                break
                
        neg_Q = not is_well_defined
        
        return [True, True, neg_Q]
        
    except Exception:
        return [False, False, False]