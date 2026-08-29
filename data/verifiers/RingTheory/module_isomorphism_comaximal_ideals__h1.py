import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import z3
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    Expected witness format: a tuple (R_add, R_mul, I, J) or an object/dict with these attributes,
    where R_add and R_mul are n x n lists of lists of integers representing the addition and 
    multiplication tables of a finite ring (or rng) R on the set {0, 1, ..., n-1}, 
    and I, J are lists of integers representing the ideals.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            R_add, R_mul, I, J = witness
        elif isinstance(witness, dict):
            R_add = witness['R_add']
            R_mul = witness['R_mul']
            I = witness['I']
            J = witness['J']
        else:
            R_add = witness.R_add
            R_mul = witness.R_mul
            I = witness.I
            J = witness.J
            
        n = len(R_add)
        I = list(set(I))
        J = list(set(J))
        
        # H1: R is a ring (or rng) and I, J are comaximal ideals
        is_rng = True
        for i in range(n):
            for j in range(n):
                if R_add[i][j] != R_add[j][i]: 
                    is_rng = False
                for k in range(n):
                    if R_add[R_add[i][j]][k] != R_add[i][R_add[j][k]]: is_rng = False
                    if R_mul[R_mul[i][j]][k] != R_mul[i][R_mul[j][k]]: is_rng = False
                    if R_mul[i][R_add[j][k]] != R_add[R_mul[i][j]][R_mul[i][k]]: is_rng = False
                    if R_mul[R_add[i][j]][k] != R_add[R_mul[i][k]][R_mul[j][k]]: is_rng = False
                    
        zero = -1
        for i in range(n):
            if all(R_add[i][j] == j for j in range(n)):
                zero = i
                break
        if zero == -1: 
            is_rng = False
        
        if is_rng:
            for i in range(n):
                if not any(R_add[i][j] == zero for j in range(n)): 
                    is_rng = False
                
        def is_ideal(S):
            if not S: return False
            for x in S:
                for y in S:
                    if R_add[x][y] not in S: return False
            for r in range(n):
                for x in S:
                    if R_mul[r][x] not in S: return False
                    if R_mul[x][r] not in S: return False
            return True
            
        h1_ideals = is_ideal(I) and is_ideal(J)
        
        I_plus_J = set()
        for i in I:
            for j in J:
                I_plus_J.add(R_add[i][j])
        h1_comaximal = (I_plus_J == set(range(n)))
        
        h1 = is_rng and h1_ideals and h1_comaximal
        
        # neg_Q: I \oplus J is not isomorphic to R \oplus (I \cap J) as R-modules
        I_cap_J = list(set(I) & set(J))
        M1 = [(i, j) for i in I for j in J]
        M2 = [(r, k) for r in range(n) for k in I_cap_J]
        
        if len(M1) != len(M2):
            neg_q = True
        else:
            solver = z3.Solver()
            solver.set("timeout", 4000)
            f = [z3.Int(f'f_{i}') for i in range(len(M1))]
            for v in f:
                solver.add(v >= 0, v < len(M2))
            solver.add(z3.Distinct(f))
            
            M1_idx = {m: idx for idx, m in enumerate(M1)}
            M2_idx = {m: idx for idx, m in enumerate(M2)}
            
            # Preserve addition
            add2 = z3.Function('add2', z3.IntSort(), z3.IntSort(), z3.IntSort())
            for i, a in enumerate(M2):
                for j, b in enumerate(M2):
                    s = (R_add[a[0]][b[0]], R_add[a[1]][b[1]])
                    solver.add(add2(i, j) == M2_idx[s])
            for i, a in enumerate(M1):
                for j, b in enumerate(M1):
                    s = (R_add[a[0]][b[0]], R_add[a[1]][b[1]])
                    solver.add(add2(f[i], f[j]) == f[M1_idx[s]])
                    
            # Preserve left scalar multiplication
            lmul2 = z3.Function('lmul2', z3.IntSort(), z3.IntSort(), z3.IntSort())
            for r in range(n):
                for i, a in enumerate(M2):
                    p = (R_mul[r][a[0]], R_mul[r][a[1]])
                    solver.add(lmul2(r, i) == M2_idx[p])
            for r in range(n):
                for i, a in enumerate(M1):
                    p = (R_mul[r][a[0]], R_mul[r][a[1]])
                    solver.add(lmul2(r, f[i]) == f[M1_idx[p]])
                    
            # Preserve right scalar multiplication (bimodule isomorphism check)
            rmul2 = z3.Function('rmul2', z3.IntSort(), z3.IntSort(), z3.IntSort())
            for r in range(n):
                for i, a in enumerate(M2):
                    p = (R_mul[a[0]][r], R_mul[a[1]][r])
                    solver.add(rmul2(i, r) == M2_idx[p])
            for r in range(n):
                for i, a in enumerate(M1):
                    p = (R_mul[a[0]][r], R_mul[a[1]][r])
                    solver.add(rmul2(f[i], r) == f[M1_idx[p]])
                    
            res = solver.check()
            neg_q = (res == z3.unsat)
            
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: I and J are comaximal ideals of R",
    "¬Q: I ⊕ J is not isomorphic to R ⊕ (I ∩ J) as R-modules"
]

N_HYP = 1
NEG_Q_INDEX = 1