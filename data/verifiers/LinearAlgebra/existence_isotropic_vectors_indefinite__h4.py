import sympy as sp
from sympy.matrices import MatrixBase, Matrix

# Top-level setup for Linear Algebra
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H1: V is a finite-dimensional vector space over the real numbers
    # We interpret the witness as the Gram matrix of the bilinear form over a basis.
    try:
        if isinstance(witness, (list, tuple)):
            matrix_obj = Matrix(witness)
        else:
            matrix_obj = witness
            
        h1 = isinstance(matrix_obj, MatrixBase) and matrix_obj.is_square and all(e.is_real for e in matrix_obj)
    except Exception:
        h1 = False
        matrix_obj = None

    # H2: The dimension of V is at least 2
    try:
        h2 = bool(h1 and matrix_obj.shape[0] >= 2)
    except Exception:
        h2 = False

    # H3: B is a symmetric bilinear form on V
    try:
        h3 = bool(h1 and matrix_obj.is_symmetric())
    except Exception:
        h3 = False

    # H4: There exists an x \in V such that B(x,x) > 0
    try:
        if h3:
            nsd = matrix_obj.is_negative_semidefinite
            if nsd is False:
                h4 = True
            elif nsd is True:
                h4 = False
            else:
                # Fallback to eigenvalues if definiteness check returns None
                evals = matrix_obj.eigenvals()
                h4 = any(sp.re(e.evalf()) > 1e-12 for e in evals)
        else:
            h4 = False
    except Exception:
        h4 = False

    # H5: There exists a y \in V such that B(y,y) < 0
    try:
        if h3:
            psd = matrix_obj.is_positive_semidefinite
            if psd is False:
                h5 = True
            elif psd is True:
                h5 = False
            else:
                # Fallback to eigenvalues
                evals = matrix_obj.eigenvals()
                h5 = any(sp.re(e.evalf()) < -1e-12 for e in evals)
        else:
            h5 = False
    except Exception:
        h5 = False

    # neg_Q: The conclusion FAILS.
    # Conclusion: There exists a non-zero vector v \in V such that B(v,v) = 0.
    # Over the real numbers, an isotropic vector exists if and only if the symmetric 
    # bilinear form is neither positive definite nor negative definite.
    # Therefore, the conclusion FAILS iff the form IS positive definite OR negative definite.
    try:
        if h3:
            pd = matrix_obj.is_positive_definite
            nd = matrix_obj.is_negative_definite
            if pd is True or nd is True:
                neg_q = True
            elif pd is False and nd is False:
                neg_q = False
            else:
                # Fallback to eigenvalues
                evals = matrix_obj.eigenvals()
                is_pd = all(sp.re(e.evalf()) > 1e-12 for e in evals)
                is_nd = all(sp.re(e.evalf()) < -1e-12 for e in evals)
                neg_q = bool(is_pd or is_nd)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over the real numbers",
    "H_2: The dimension of V is at least 2",
    "H_3: B is a symmetric bilinear form on V",
    "H_4: There exists an x in V such that B(x,x) > 0",
    "H_5: There exists a y in V such that B(y,y) < 0",
    "¬Q: There does NOT exist a non-zero vector v in V such that B(v,v) = 0"
]

N_HYP = 5
NEG_Q_INDEX = 5