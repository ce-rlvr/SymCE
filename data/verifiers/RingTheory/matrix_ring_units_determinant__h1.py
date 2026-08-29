import sympy as sp
from sympy.abc import x, y, z, t

# Standard bindings
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

# Non-commutative symbols for constructing counterexamples over free algebras
nc_x, nc_y, nc_z = sp.symbols('nc_x nc_y nc_z', commutative=False)

# Quaternions for constructing counterexamples over skew fields
try:
    qi = sp.Quaternion(0, 1, 0, 0)
    qj = sp.Quaternion(0, 0, 1, 0)
    qk = sp.Quaternion(0, 0, 0, 1)
except AttributeError:
    pass

def conditions(witness):
    try:
        if not isinstance(witness, sp.MatrixBase):
            A = sp.Matrix(witness)
        else:
            A = witness
    except Exception:
        return [False, False, False]

    # H_1: M_n(R) is the ring of n x n matrices over R
    # This is a definitional hypothesis, always True in this context.
    h1 = True

    # H_2: A is a matrix in M_n(R)
    try:
        h2 = A.is_square
    except Exception:
        h2 = False

    # ¬Q: A is a unit in M_n(R) iff det(A) is a unit in R fails
    try:
        has_quat = False
        for elem in A:
            if type(elem).__name__ == 'Quaternion':
                has_quat = True
                break

        # Check if the matrix is over a commutative ring.
        # If it is, the theorem is mathematically proven to hold, so it cannot be a counterexample.
        is_commutative = True
        if has_quat:
            is_commutative = False
        else:
            for elem in A:
                if hasattr(elem, 'free_symbols'):
                    for sym in elem.free_symbols:
                        if getattr(sym, 'is_commutative', True) is False:
                            is_commutative = False
                            break
                if not is_commutative:
                    break
            
        if is_commutative:
            return [h1, h2, False]

        # Compute P: A is a unit in M_n(R)
        is_unit_A = False
        if has_quat:
            n = A.rows
            C = sp.Matrix.zeros(2*n, 2*n)
            for i in range(n):
                for j in range(n):
                    q = A[i, j]
                    if type(q).__name__ != 'Quaternion':
                        q = sp.Quaternion(q, 0, 0, 0)
                    a, b, c, d = q.a, q.b, q.c, q.d
                    C[2*i, 2*j] = a + b*sp.I
                    C[2*i, 2*j+1] = c + d*sp.I
                    C[2*i+1, 2*j] = -c + d*sp.I
                    C[2*i+1, 2*j+1] = a - b*sp.I
            is_unit_A = (sp.expand(C.det()) != 0)
        else:
            try:
                B = A.inv()
                I_mat = sp.eye(A.rows)
                if sp.expand(A * B) == I_mat and sp.expand(B * A) == I_mat:
                    has_fraction_A = any(val.as_numer_denom()[1] != 1 for val in A)
                    if all(isinstance(val, (int, sp.Integer)) for val in A):
                        is_unit_A = all(isinstance(val, (int, sp.Integer)) for val in B)
                    else:
                        is_unit_A = True
                        for val in B:
                            num, den = val.as_numer_denom()
                            if len(den.free_symbols) > 0:
                                is_unit_A = False
                                break
                            if not has_fraction_A and den != 1:
                                is_unit_A = False
                                break
                else:
                    is_unit_A = False
            except Exception:
                is_unit_A = False

        # Compute Q: det(A) is a unit in R
        try:
            if A.rows == 1:
                det_A = sp.expand(A[0,0])
            elif A.rows == 2:
                det_A = sp.expand(A[0,0]*A[1,1] - A[0,1]*A[1,0])
            else:
                det_A = sp.expand(A.det())
        except Exception:
            det_A = 0

        is_unit_det = False
        if has_quat:
            if type(det_A).__name__ == 'Quaternion':
                is_unit_det = not (sp.expand(det_A.a) == 0 and sp.expand(det_A.b) == 0 and 
                                   sp.expand(det_A.c) == 0 and sp.expand(det_A.d) == 0)
            else:
                is_unit_det = (sp.expand(det_A) != 0)
        else:
            has_fraction_A = any(val.as_numer_denom()[1] != 1 for val in A)
            if all(isinstance(val, (int, sp.Integer)) for val in A):
                is_unit_det = (abs(det_A) == 1)
            elif isinstance(det_A, sp.Expr):
                if len(det_A.free_symbols) == 0 and det_A != 0:
                    if abs(det_A) == 1:
                        is_unit_det = True
                    else:
                        is_unit_det = has_fraction_A
                else:
                    is_unit_det = False
            else:
                is_unit_det = (det_A != 0)

        neg_q = (is_unit_A != is_unit_det)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M_n(R) is the ring of n x n matrices over R",
    "H_2: A is a matrix in M_n(R)",
    "¬Q: A is a unit in M_n(R) iff det(A) is a unit in R fails"
]

N_HYP = 2
NEG_Q_INDEX = 2