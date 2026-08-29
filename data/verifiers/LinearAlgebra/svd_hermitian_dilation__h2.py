import sympy
from sympy import Matrix, eye, zeros, simplify, sqrt
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_nonzero(val):
    """Safely check if a sympy value is non-zero, handling floating point inaccuracies."""
    if val == 0:
        return False
    try:
        v = complex(val.evalf())
        if abs(v) < 1e-7:
            simp_val = sympy.simplify(val)
            if simp_val == 0:
                return False
            if isinstance(simp_val, (sympy.Float, float)) or simp_val.has(sympy.Float):
                return False
            return True
        return True
    except Exception:
        return sympy.simplify(val) != 0

def conditions(witness) -> list[bool]:
    # Extract A and H from the witness
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            H = witness.get('H')
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            A, H = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # Convert to sympy Matrices if they are lists
    try:
        from sympy import MatrixBase, Matrix
        if not isinstance(A, MatrixBase):
            A = Matrix(A)
        if not isinstance(H, MatrixBase):
            H = Matrix(H)
    except Exception:
        pass

    # H_1: A is an m x n matrix over C
    try:
        h1 = isinstance(A, MatrixBase) and isinstance(H, MatrixBase)
    except Exception:
        h1 = False

    # neg_Q: The non-zero eigenvalues of H are NOT exactly the pairs \pm \sigma_i
    try:
        if not h1:
            return [False, False]
        
        # Compute non-zero singular values of A
        M = A.H * A
        eigenvals_A = M.eigenvals()
        svs = []
        for val, mult in eigenvals_A.items():
            if is_nonzero(val):
                sv = sqrt(val)
                svs.extend([sv] * mult)
        
        expected_evs = []
        for sv in svs:
            expected_evs.extend([sv, -sv])
            
        if not H.is_square:
            neg_q = True
        else:
            # Compute non-zero eigenvalues of H
            eigenvals_H = H.eigenvals()
            actual_evs = []
            for val, mult in eigenvals_H.items():
                if is_nonzero(val):
                    actual_evs.extend([val] * mult)
                    
            def match(l1, l2):
                if len(l1) != len(l2): 
                    return False
                try:
                    # Try numerical matching first
                    c1 = [complex(v.evalf()) for v in l1]
                    c2 = [complex(v.evalf()) for v in l2]
                    l2_copy = list(c2)
                    for v1 in c1:
                        found = False
                        for i, v2 in enumerate(l2_copy):
                            if abs(v1 - v2) < 1e-7:
                                l2_copy.pop(i)
                                found = True
                                break
                        if not found:
                            return False
                    return True
                except Exception:
                    # Fallback to symbolic matching
                    l2_copy = list(l2)
                    for v1 in l1:
                        found = False
                        for i, v2 in enumerate(l2_copy):
                            if sympy.simplify(v1 - v2) == 0:
                                l2_copy.pop(i)
                                found = True
                                break
                        if not found:
                            return False
                    return True

            q = match(expected_evs, actual_evs)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a matrix over C",
    "¬Q: The non-zero eigenvalues of H are not exactly the pairs ±σ_i"
]
N_HYP = 1
NEG_Q_INDEX = 1