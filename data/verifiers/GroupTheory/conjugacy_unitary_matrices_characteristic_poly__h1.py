import sympy as sp
import itertools

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def is_unitary(M):
    if not isinstance(M, sp.MatrixBase):
        return False
    n = M.shape[0]
    if M.shape != (n, n):
        return False
        
    # Check if over a finite field
    p = None
    for x in M:
        if hasattr(x, 'mod'):
            p = x.mod
            break
        if hasattr(x, 'p'):
            p = x.p
            break
            
    if p is not None:
        M_MT = M * M.T
        for i in range(n):
            for j in range(n):
                val = M_MT[i, j]
                if hasattr(val, 'val'):
                    val = val.val
                if i == j:
                    if val % p != 1:
                        return False
                else:
                    if val % p != 0:
                        return False
        return True
    else:
        res = M * M.H
        diff = res - sp.eye(n)
        if diff.is_zero_matrix:
            return True
        return sp.simplify(diff).is_zero_matrix

def are_conjugate(A, B):
    if A == B:
        return True
    n = A.shape[0]
    
    # Check if over a finite field
    p = None
    for x in A:
        if hasattr(x, 'mod'):
            p = x.mod
            break
        if hasattr(x, 'p'):
            p = x.p
            break
            
    if p is not None:
        elements = list(range(p))
        for entries in itertools.product(elements, repeat=n*n):
            U = sp.Matrix(n, n, entries)
            U_UT = U * U.T
            is_ortho = True
            for i in range(n):
                for j in range(n):
                    val = U_UT[i, j]
                    if hasattr(val, 'val'): val = val.val
                    if i == j:
                        if val % p != 1: is_ortho = False
                    else:
                        if val % p != 0: is_ortho = False
            if is_ortho:
                UA = U * A
                BU = B * U
                is_conj = True
                for i in range(n):
                    for j in range(n):
                        v1 = UA[i, j]
                        v2 = BU[i, j]
                        if hasattr(v1, 'val'): v1 = v1.val
                        if hasattr(v2, 'val'): v2 = v2.val
                        if v1 % p != v2 % p:
                            is_conj = False
                if is_conj:
                    return True
        return False

    # Check if over Z
    is_Z = all(isinstance(x, (int, sp.Integer)) for x in A) and all(isinstance(x, (int, sp.Integer)) for x in B)
    if is_Z:
        for p_perm in itertools.permutations(range(n)):
            for signs in itertools.product([1, -1], repeat=n):
                U = sp.zeros(n, n)
                for i, j in enumerate(p_perm):
                    U[i, j] = signs[i]
                if U * A * U.T == B:
                    return True
        return False

    # Check if over Q
    is_Q = all(isinstance(x, (int, sp.Integer, sp.Rational)) for x in A) and all(isinstance(x, (int, sp.Integer, sp.Rational)) for x in B)
    if is_Q:
        if n == 2:
            a, b = sp.symbols('a b')
            # Rotations
            U = sp.Matrix([[a, b], [-b, a]])
            eqs = list(U * A - B * U) + [a**2 + b**2 - 1]
            sols = sp.solve(eqs, (a, b), dict=True)
            for sol in sols:
                if all(v.is_Rational for v in sol.values()):
                    return True
            # Reflections
            U = sp.Matrix([[a, b], [b, -a]])
            eqs = list(U * A - B * U) + [a**2 + b**2 - 1]
            sols = sp.solve(eqs, (a, b), dict=True)
            for sol in sols:
                if all(v.is_Rational for v in sol.values()):
                    return True
            return False
        else:
            vars = sp.symbols(f'u0:{n*n}')
            U = sp.Matrix(n, n, vars)
            eqs = list(U * A - B * U) + list(U * U.T - sp.eye(n))
            sols = sp.solve(eqs, vars, dict=True)
            for sol in sols:
                is_rational = True
                for v in vars:
                    if v in sol:
                        val = sol[v]
                        free_syms = val.free_symbols
                        if free_syms:
                            val = val.subs({s: 0 for s in free_syms})
                        if not val.is_Rational:
                            is_rational = False
                            break
                if is_rational:
                    return True
            return False

    # Default to C
    return A.charpoly() == B.charpoly()

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            n_dim, A, B = witness
        elif len(witness) == 2:
            A, B = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: A and B are square matrices of the same size
    try:
        h1 = (isinstance(A, sp.MatrixBase) and isinstance(B, sp.MatrixBase) and 
              A.is_square and B.is_square and A.shape == B.shape)
    except Exception:
        h1 = False
        
    # H_2: A and B are unitary matrices
    try:
        h2 = is_unitary(A) and is_unitary(B)
    except Exception:
        h2 = False
        
    # neg_Q: The equivalence between conjugacy in U(n) and having the same characteristic polynomial fails
    try:
        same_charpoly = (A.charpoly() == B.charpoly())
        conjugate = are_conjugate(A, B)
        conclusion = (conjugate == same_charpoly)
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are square matrices of the same size",
    "H_2: A and B are unitary matrices",
    "¬Q: A and B have the same characteristic polynomial but are not conjugate in U(n), or vice versa"
]

N_HYP = 2
NEG_Q_INDEX = 2