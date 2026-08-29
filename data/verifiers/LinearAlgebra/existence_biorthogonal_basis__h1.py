import sympy
from sympy import eye, zeros, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_ring(matrices):
    has_float = False
    has_rational = False
    has_symbol = False
    for mat in matrices:
        for val in mat:
            val = sympy.sympify(val)
            if val.has(sympy.Float):
                has_float = True
            elif val.has(sympy.Symbol):
                has_symbol = True
            elif val.is_Rational and not val.is_Integer:
                has_rational = True
    if has_float:
        return 'R'
    if has_symbol:
        if has_rational:
            return 'poly_Q'
        return 'poly_Z'
    if has_rational:
        return 'Q'
    return 'Z'

def check_basis(matrix, ring):
    try:
        det = matrix.det()
        if ring in ('R', 'Q'):
            return det != 0
        elif ring == 'Z':
            if not all(sympy.sympify(val).is_Integer for val in matrix):
                return False
            return det == 1 or det == -1
        elif ring.startswith('poly'):
            for val in matrix:
                num, den = sympy.fraction(sympy.cancel(val))
                if not den.is_constant():
                    return False
            det = sympy.cancel(det)
            if not det.is_constant():
                return False
            if ring == 'poly_Z':
                return det == 1 or det == -1
            else:
                return det != 0
    except Exception:
        return False
    return False

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            B_matrix, basis_vectors = witness
            try:
                B_matrix = Matrix(B_matrix)
            except TypeError:
                B_matrix = Matrix([[B_matrix]])
            basis_vectors = [Matrix(v) for v in basis_vectors]
        else:
            try:
                B_matrix = Matrix(witness)
            except TypeError:
                B_matrix = Matrix([[witness]])
            n = B_matrix.shape[0]
            basis_vectors = [eye(n)[:, i] for i in range(n)]
            
        n = B_matrix.shape[0]
        if B_matrix.shape != (n, n):
            return [False, False, False]
            
        E = Matrix.hstack(*basis_vectors)
        if E.shape != (n, n):
            return [False, False, False]
            
        ring = get_ring([B_matrix, E])
        
        # H1: B is a non-degenerate bilinear form on V
        try:
            det_B = B_matrix.det()
            h1 = (det_B != 0)
        except Exception:
            h1 = False
            
        # H2: {e_1, e_2, ..., e_n} is a basis of V
        try:
            h2 = check_basis(E, ring)
        except Exception:
            h2 = False
            
        # Conclusion: There exists a unique basis {f_1, f_2, ..., f_n} of V such that B(e_i, f_j) = \delta_{ij}
        try:
            # The condition B(e_i, f_j) = \delta_{ij} translates to E^T * B * F = I
            # Therefore, F = (E^T * B)^{-1}
            F = (E.T * B_matrix).inv()
            is_basis = check_basis(F, ring)
            neg_q = not is_basis
        except Exception:
            # If not invertible over the field of fractions, F doesn't exist
            neg_q = True
            
    except Exception:
        h1 = False
        h2 = False
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: B is a non-degenerate bilinear form on V",
    "H_2: {e_1, e_2, ..., e_n} is a basis of V",
    "¬Q: There does not exist a unique biorthogonal basis {f_1, f_2, ..., f_n} of V"
]

N_HYP = 2
NEG_Q_INDEX = 2