import sympy as sp

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks whether the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: A is an n \times n matrix over the complex numbers \mathbb{C}
    try:
        if not isinstance(witness, sp.MatrixBase):
            h1 = False
        elif not witness.is_square:
            h1 = False
        else:
            h1 = True
            for val in witness:
                # Ensure entries are not explicitly non-complex
                if val.is_complex is False:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # neg_Q: Conclusion fails
    # Conclusion: A is diagonalizable if and only if all poles of the meromorphic matrix-valued function R(z, A) are simple poles
    try:
        if h1:
            # Convert floats to rationals for exact algebraic computation
            A_exact = witness.applyfunc(lambda x: sp.nsimplify(x) if x.is_Float else x)
            
            # LHS: A is diagonalizable
            lhs = A_exact.is_diagonalizable()
            
            # RHS: all poles of R(z, A) = (zI - A)^{-1} are simple poles.
            # The order of the pole at an eigenvalue lambda is the size of the largest Jordan block for lambda.
            # Thus, all poles are simple if and only if all Jordan blocks have size 1 (i.e., the Jordan form is diagonal).
            _, J = A_exact.jordan_form()
            rhs = J.is_diagonal()
            
            # The conclusion is the equivalence of LHS and RHS
            q = (lhs == rhs)
            
            # We want the negated conclusion (True if the equivalence fails)
            neg_q = not q
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n \\times n matrix over the complex numbers \\mathbb{C}",
    "¬Q: A is diagonalizable is NOT equivalent to all poles of R(z, A) being simple poles"
]

N_HYP = 1
NEG_Q_INDEX = 1