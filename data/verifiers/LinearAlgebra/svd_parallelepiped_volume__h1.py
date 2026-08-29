import sympy as sp
from sympy import eye, zeros, I, Rational, Integer, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, sp.Matrix):
            witness = sp.Matrix(witness)
            
        # H_1: P is the n-dimensional parallelepiped spanned by the n columns of A
        # This hypothesis is structural; it holds if the witness is a valid matrix.
        h1 = True
        
        n = witness.cols
        
        # Calculate the n-dimensional volume of the parallelepiped spanned by the columns.
        # The volume squared is the determinant of the Gram matrix (A^T * A).
        gram_matrix = witness.T * witness
        vol_sq = gram_matrix.det()
        vol = sp.sqrt(vol_sq)
        
        # Calculate the product of the n singular values of A.
        # SymPy's singular_values() returns min(m, n) singular values.
        svs = witness.singular_values()
        
        if len(svs) < n:
            # If there are fewer than n singular values (e.g., m < n),
            # the remaining singular values are 0, so the product of n singular values is 0.
            prod_sv = sp.Integer(0)
        else:
            prod_sv = sp.Integer(1)
            for sv in svs[:n]:
                prod_sv *= sv
                
        # Check if the volume is equal to the product of the singular values
        diff = sp.simplify(vol - prod_sv)
        
        if diff == 0:
            neg_q = False
        elif hasattr(diff, 'equals') and diff.equals(0):
            neg_q = False
        else:
            neg_q = True
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: P is the n-dimensional parallelepiped spanned by the n columns of A",
    "not Q: The n-dimensional volume of P is NOT equal to the product of the n singular values of A"
]

N_HYP = 1
NEG_Q_INDEX = 1