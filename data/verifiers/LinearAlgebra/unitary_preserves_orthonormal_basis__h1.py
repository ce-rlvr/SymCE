import sympy as sp
from sympy import eye, zeros, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: T is a unitary operator",
    "H_2: {e_1, ..., e_n} is an orthonormal basis for V",
    "¬Q: {T(e_1), ..., T(e_n)} is not an orthonormal basis for W"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Witness can be a tuple (T, E) or just T (in which case E is the standard basis)
        if isinstance(witness, tuple) and len(witness) == 2:
            T, E = witness
        elif isinstance(witness, sp.Matrix):
            T = witness
            n = T.shape[1]
            E = [sp.Matrix([1 if i == j else 0 for i in range(n)]) for j in range(n)]
        else:
            return [False, False, False]
            
        if not isinstance(T, sp.Matrix):
            return [False, False, False]
            
        m, n = T.shape
        
        # Allow E to be provided as a matrix whose columns are the basis vectors
        if isinstance(E, sp.Matrix):
            if E.shape[0] != n:
                return [False, False, False]
            E = [E[:, i] for i in range(E.shape[1])]
            
        if not isinstance(E, list):
            return [False, False, False]
            
        # H1: T is a unitary operator (isometry from V to W)
        # T^H * T == I_n
        diff_H1 = T.H * T - sp.eye(n)
        h1 = all(sp.simplify(sp.expand(diff_H1[i, j])) == 0 for i in range(n) for j in range(n))
        
        # H2: E is an orthonormal basis for V (C^n)
        h2 = True
        if len(E) != n:
            h2 = False
        else:
            for i in range(n):
                if not h2: break
                if not isinstance(E[i], sp.Matrix) or E[i].shape != (n, 1):
                    h2 = False
                    break
                for j in range(n):
                    dot = (E[i].H * E[j])[0, 0]
                    expected = 1 if i == j else 0
                    if sp.simplify(sp.expand(dot - expected)) != 0:
                        h2 = False
                        break
                        
        # Conclusion: T(E) is an orthonormal basis for W (C^m)
        TE = [T * e for e in E if isinstance(e, sp.Matrix) and e.shape == (n, 1)]
        
        is_orthonormal = True
        for i in range(len(TE)):
            if not is_orthonormal: break
            for j in range(len(TE)):
                dot = (TE[i].H * TE[j])[0, 0]
                expected = 1 if i == j else 0
                if sp.simplify(sp.expand(dot - expected)) != 0:
                    is_orthonormal = False
                    break
                    
        # It is a basis for W iff it spans W, which requires exactly m vectors
        is_basis = is_orthonormal and len(TE) == m
        
        neg_q = not is_basis
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]