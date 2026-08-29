import math
from sympy import Matrix, MatrixBase, Abs, simplify, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, MatrixBase)
        if h1:
            # Verify that singular values can be computed
            sv = witness.singular_values()
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            try:
                d = witness.det()
                sv = witness.singular_values()
                prod_sv = 1
                for s in sv:
                    prod_sv *= s
                
                diff = simplify(Abs(d) - prod_sv)
                if diff == 0:
                    conclusion = True
                else:
                    try:
                        conclusion = abs(complex(diff.evalf())) < 1e-9
                    except Exception:
                        conclusion = False
                neg_q = not conclusion
            except Exception:
                # If det() fails (e.g., because A is a non-square matrix),
                # the conclusion that |det(A)| == prod(sigma_i) is false.
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: sigma_1, ..., sigma_n are the singular values of A",
    "¬Q: |det(A)| != prod_{i=1}^n sigma_i (or det(A) is undefined)"
]

N_HYP = 1
NEG_Q_INDEX = 1