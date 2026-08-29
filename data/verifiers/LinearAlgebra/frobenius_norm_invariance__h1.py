import sympy
from sympy import eye, zeros, Matrix
import math

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_unitary(obj):
    try:
        if not (hasattr(obj, 'is_Matrix') and obj.is_Matrix):
            return False
        if obj.shape[0] != obj.shape[1]:
            return False
        n = obj.shape[0]
        I = sympy.eye(n)
        diff = obj * obj.H - I
        
        for x in diff:
            if isinstance(x, (int, float, complex)):
                if abs(complex(x)) > 1e-9:
                    return False
            elif hasattr(x, 'is_number') and x.is_number:
                if abs(complex(x.evalf())) > 1e-9:
                    return False
            else:
                if sympy.simplify(x) != 0:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    # Extract U, V, A
    U, V, A = None, None, None
    if isinstance(witness, dict):
        U = witness.get('U')
        V = witness.get('V')
        A = witness.get('A')
    elif isinstance(witness, (list, tuple)) and len(witness) == 3:
        unitary_matrices = []
        other_objects = []
        for obj in witness:
            if is_unitary(obj):
                unitary_matrices.append(obj)
            else:
                other_objects.append(obj)
        
        if len(unitary_matrices) >= 2:
            U = unitary_matrices[0]
            V = unitary_matrices[1]
            if len(unitary_matrices) == 3:
                A = unitary_matrices[2]
            else:
                A = other_objects[0]
        else:
            U, V, A = witness
    else:
        return [False, False]

    # H1: U and V are n x n unitary matrices
    try:
        h1 = False
        if is_unitary(U) and is_unitary(V):
            if U.shape == V.shape:
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: ||UAV||_F != ||A||_F
    try:
        UAV = U * A * V
    except Exception:
        # If UAV is undefined (e.g. shape mismatch), they cannot be equal
        neg_q = True
    else:
        try:
            if hasattr(UAV, 'norm'):
                norm_UAV = UAV.norm()
            elif hasattr(UAV, 'is_Matrix') and UAV.is_Matrix:
                norm_UAV = sympy.sqrt(sum(sympy.Abs(x)**2 for x in UAV))
            elif isinstance(UAV, (list, tuple)):
                norm_UAV = sympy.Matrix(UAV).norm()
            else:
                norm_UAV = sympy.Abs(UAV)
                
            if hasattr(A, 'norm'):
                norm_A = A.norm()
            elif hasattr(A, 'is_Matrix') and A.is_Matrix:
                norm_A = sympy.sqrt(sum(sympy.Abs(x)**2 for x in A))
            elif isinstance(A, (list, tuple)):
                norm_A = sympy.Matrix(A).norm()
            else:
                norm_A = sympy.Abs(A)
                
            diff = norm_UAV - norm_A
            
            if isinstance(diff, (int, float)):
                neg_q = abs(diff) > 1e-9
            elif diff == 0:
                neg_q = False
            elif hasattr(diff, 'is_zero') and diff.is_zero:
                neg_q = False
            else:
                if hasattr(diff, 'is_number') and diff.is_number:
                    neg_q = abs(complex(diff.evalf())) > 1e-9
                else:
                    diff_simp = sympy.simplify(diff)
                    if diff_simp == 0 or (hasattr(diff_simp, 'is_zero') and diff_simp.is_zero):
                        neg_q = False
                    else:
                        try:
                            val = diff_simp.evalf()
                            if hasattr(val, 'is_number') and val.is_number:
                                neg_q = abs(complex(val)) > 1e-9
                            else:
                                neg_q = True
                        except Exception:
                            neg_q = True
        except Exception:
            neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U and V are n x n unitary matrices",
    "¬Q: ||UAV||_F != ||A||_F"
]

N_HYP = 1
NEG_Q_INDEX = 1