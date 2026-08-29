import z3
import math
import itertools
import functools
from sympy.matrices import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            N = witness.get('N')
            add = witness.get('add')
            mul = witness.get('mul')
            I = witness.get('I')
            J = witness.get('J')
        else:
            N = getattr(witness, 'N', None)
            add = getattr(witness, 'add', None)
            mul = getattr(witness, 'mul', None)
            I = getattr(witness, 'I', None)
            J = getattr(witness, 'J', None)
            
        if N is None or add is None or mul is None or I is None or J is None:
            return [False, False, False, False]
            
        if N > 32:
            return [False, False, False, False]
            
        I = list(set(I))
        J = list(set(J))
            
        # 1. Check ring axioms
        is_valid_ring = True
        for i in range(N):
            if not is_valid_ring: break
            for j in range(N):
                if not is_valid_ring: break
                if add[i][j] != add[j][i]: 
                    is_valid_ring = False
                    break
                for k in range(N):
                    if add[add[i][j]][k] != add[i][add[j][k]]: is_valid_ring = False
                    elif mul[mul[i][j]][k] != mul[i][mul[j][k]]: is_valid_ring = False
                    elif mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: is_valid_ring = False
                    elif mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: is_valid_ring = False
                    if not is_valid_ring: break
                    
        zero = None
        for i in range(N):
            if all(add[i][j] == j for j in range(N)):
                zero = i
                break
        if zero is None: 
            is_valid_ring = False
        else:
            for j in range(N):
                if not any(add[j][k] == zero for k in range(N)):
                    is_valid_ring = False
                    break
                    
        has_one = False
        for i in range(N):
            if all(mul[i][j] == j and mul[j][i] == j for j in range(N)):
                has_one = True
                break
        if not has_one: 
            is_valid_ring = False
        
        if not is_valid_ring:
            return [False, False, False, False]
            
        def is_ideal(S):
            if not S: return False
            S_set = set(S)
            if zero not in S_set: return False
            for x in S:
                for y in S:
                    if add[x][y] not in S_set: return False
                for r in range(N):
                    if mul[r][x] not in S_set: return False
                    if mul[x][r] not in S_set: return False
            return True
            
        h1 = is_ideal(I) and is_ideal(J)
        
        I_plus_J = set()
        for i in I:
            for j in J:
                I_plus_J.add(add[i][j])
        h2 = (len(I_plus_J) == N)
        
        uid = id(object())
        Add = z3.Function(f'Add_{uid}', z3.IntSort(), z3.IntSort(), z3.IntSort())
        Mul = z3.Function(f'Mul_{uid}', z3.IntSort(), z3.IntSort(), z3.IntSort())
        
        base_solver = z3.Solver()
        for i in range(N):
            for j in range(N):
                base_solver.add(Add(i, j) == add[i][j])
                base_solver.add(Mul(i, j) == mul[i][j])
                
        def is_projective_left(M):
            if len(M) <= 1: return True
            solver = z3.Solver()
            solver.add(base_solver.assertions())
            f = {}
            mid = id(M)
            for m in M:
                f[m] = {}
                for x in M:
                    f[m][x] = z3.Int(f"fl_{uid}_{mid}_{m}_{x}")
                    solver.add(f[m][x] >= 0, f[m][x] < N)
            for m in M:
                for x in M:
                    for y in M:
                        solver.add(f[m][add[x][y]] == Add(f[m][x], f[m][y]))
                    for r in range(N):
                        rx = mul[r][x]
                        if rx in M:
                            solver.add(f[m][rx] == Mul(r, f[m][x]))
            for x in M:
                expr = zero
                for m in M:
                    expr = Add(expr, Mul(f[m][x], m))
                solver.add(expr == x)
            return solver.check() == z3.sat

        def is_projective_right(M):
            if len(M) <= 1: return True
            solver = z3.Solver()
            solver.add(base_solver.assertions())
            f = {}
            mid = id(M)
            for m in M:
                f[m] = {}
                for x in M:
                    f[m][x] = z3.Int(f"fr_{uid}_{mid}_{m}_{x}")
                    solver.add(f[m][x] >= 0, f[m][x] < N)
            for m in M:
                for x in M:
                    for y in M:
                        solver.add(f[m][add[x][y]] == Add(f[m][x], f[m][y]))
                    for r in range(N):
                        xr = mul[x][r]
                        if xr in M:
                            solver.add(f[m][xr] == Mul(f[m][x], r))
            for x in M:
                expr = zero
                for m in M:
                    expr = Add(expr, Mul(m, f[m][x]))
                solver.add(expr == x)
            return solver.check() == z3.sat

        left_proj_I = is_projective_left(I)
        left_proj_J = is_projective_left(J)
        right_proj_I = is_projective_right(I)
        right_proj_J = is_projective_right(J)
        
        h3_left = left_proj_I and left_proj_J
        h3_right = right_proj_I and right_proj_J
        h3 = h3_left or h3_right
        
        I_cap_J = list(set(I).intersection(set(J)))
        left_proj_cap = is_projective_left(I_cap_J)
        right_proj_cap = is_projective_right(I_cap_J)
        
        if h3_left and not h3_right:
            neg_q = not left_proj_cap
        elif h3_right and not h3_left:
            neg_q = not right_proj_cap
        elif h3_left and h3_right:
            neg_q = not left_proj_cap and not right_proj_cap
        else:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: I and J are comaximal",
    "H_3: I and J are projective as R-modules",
    "¬Q: I \\cap J is not a projective R-module"
]
N_HYP = 3
NEG_Q_INDEX = 3