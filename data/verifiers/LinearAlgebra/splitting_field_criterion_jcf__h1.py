import sympy
import itertools
import z3

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def z3_det(matrix):
    if len(matrix) == 0:
        return 1
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    res = 0
    for c in range(len(matrix)):
        sub = [row[:c] + row[c+1:] for row in matrix[1:]]
        sign = 1 if c % 2 == 0 else -1
        res += sign * matrix[0][c] * z3_det(sub)
    return res

def conditions(witness):
    try:
        if not isinstance(witness, sympy.MatrixBase):
            return [False]
            
        x = sympy.Symbol('x')
        p = witness.charpoly(x)
        roots = p.roots()
        
        # Determine the domain of the matrix. 
        # The standard counterexample is over a ring like ZZ where the theorem fails.
        is_zz = all(witness[i, j].is_integer for i in range(witness.shape[0]) for j in range(witness.shape[1]))
        
        if is_zz:
            splits = sum(roots.values()) == witness.shape[0] and all(r.is_integer for r in roots.keys())
        else:
            splits = sum(roots.values()) == witness.shape[0] and all(r.is_rational for r in roots.keys())
            
        # Find the Jordan form over the field of fractions (QQ)
        P_QQ, J = witness.jordan_form()
        
        n = J.shape[0]
        blocks = []
        i = 0
        while i < n:
            j = i + 1
            while j < n and J[j-1, j] == 1 and J[j, j] == J[i, i]:
                j += 1
            blocks.append(J[i:j, i:j])
            i = j
            
        # Generate unique permutations of Jordan blocks
        unique_perms = []
        for perm in itertools.permutations(blocks):
            is_new = True
            for up in unique_perms:
                if len(perm) == len(up) and all(perm[k] == up[k] for k in range(len(perm))):
                    is_new = False
                    break
            if is_new:
                unique_perms.append(perm)
                
        is_similar = False
        for perm in unique_perms:
            J_perm = sympy.diag(*perm)
            
            solver = z3.Solver()
            solver.set("timeout", 2000)
            
            if is_zz:
                P_vars = [[z3.Int(f'p_{r}_{c}') for c in range(n)] for r in range(n)]
            else:
                P_vars = [[z3.Real(f'p_{r}_{c}') for c in range(n)] for r in range(n)]
                
            for r in range(n):
                for c in range(n):
                    if is_zz:
                        lhs = sum(P_vars[r][k] * int(J_perm[k, c]) for k in range(n))
                        rhs = sum(int(witness[r, k]) * P_vars[k][c] for k in range(n))
                    else:
                        lhs = sum(P_vars[r][k] * z3.RealVal(str(J_perm[k, c])) for k in range(n))
                        rhs = sum(z3.RealVal(str(witness[r, k])) * P_vars[k][c] for k in range(n))
                    solver.add(lhs == rhs)
                    
            det = z3_det(P_vars)
            if is_zz:
                # For similarity over ZZ, the transition matrix must be invertible over ZZ (det = ±1)
                solver.add(z3.Or(det == 1, det == -1))
            else:
                # For similarity over QQ, the transition matrix must just be invertible
                solver.add(det != 0)
                
            if solver.check() == z3.sat:
                is_similar = True
                break
                
        # The negated conclusion is True if the characteristic polynomial splits completely 
        # over the domain, but the matrix is NOT similar to a Jordan form over that domain.
        neg_q = bool(splits and not is_similar)
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The characteristic polynomial splits completely over F, but A is not similar to a Jordan form over F"
]

N_HYP = 0
NEG_Q_INDEX = 0