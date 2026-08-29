import sympy
from sympy import Symbol, Matrix, S
from sympy.calculus.util import continuous_domain

# Top-level setup
x = Symbol('x', real=True)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness is expected to be a sympy.Matrix, a list/tuple of sympy.Matrix, 
    or a callable returning such, representing a family of matrix-valued functions of x.
    """
    # H_1: X is a metric space
    # We fix X = R with the standard metric.
    h1 = True
    
    # H_2: \mathcal{A} is a family of functions from X to n x n real matrices
    h2 = False
    try:
        # Normalize witness to a list of matrices
        if callable(witness):
            try:
                res = witness(x)
            except Exception:
                res = witness
            if isinstance(res, Matrix):
                witness = [res]
            elif isinstance(res, (list, tuple)):
                witness = res
        elif isinstance(witness, Matrix):
            witness = [witness]
            
        if isinstance(witness, (list, tuple)) and len(witness) > 0:
            h2 = True
            n = None
            for mat in witness:
                if not isinstance(mat, Matrix):
                    h2 = False
                    break
                if mat.rows != mat.cols:
                    h2 = False
                    break
                if n is None:
                    n = mat.rows
                elif mat.rows != n:
                    h2 = False
                    break
                
                # Check if entries are real functions of x
                for i in range(mat.rows):
                    for j in range(mat.cols):
                        entry = sympy.sympify(mat[i, j])
                        if not entry.free_symbols.issubset({x}):
                            h2 = False
                            break
                    if not h2:
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # neg_Q: The family of traces is NOT equicontinuous on X
    # For a finite family, this means at least one trace is discontinuous on R.
    neg_q = False
    try:
        if h2:
            for mat in witness:
                tr = mat.trace()
                try:
                    dom = continuous_domain(tr, x, S.Reals)
                    if dom != S.Reals:
                        neg_q = True
                        break
                except Exception:
                    pass
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: \\mathcal{A} is a family of functions from X to n x n real matrices",
    "¬Q: The family of traces is not equicontinuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2