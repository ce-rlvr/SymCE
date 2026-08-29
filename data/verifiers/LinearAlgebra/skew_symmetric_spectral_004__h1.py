import sympy as sp
from sympy import MatrixBase, I, eye, zeros
from sympy.abc import x, y, z

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H1: The entries of A are real numbers
    try:
        if not isinstance(witness, MatrixBase):
            h1 = False
        else:
            h1 = all(e.is_real for e in witness)
    except Exception:
        h1 = False

    # H2: A is a skew-symmetric matrix (A^T = -A)
    try:
        if not isinstance(witness, MatrixBase):
            h2 = False
        else:
            h2 = witness.is_square and bool(witness.T == -witness)
    except Exception:
        h2 = False

    # Conclusion: There exists a real orthogonal matrix Q such that Q^T A Q is a block diagonal matrix 
    # where each diagonal block is either a 1x1 zero matrix or a 2x2 matrix of the form [[0, a], [-a, 0]] 
    # for some non-zero real number a.
    # Mathematically, this is equivalent to A being diagonalizable over C with purely imaginary or zero eigenvalues.
    try:
        if not isinstance(witness, MatrixBase) or not witness.is_square:
            neg_q = True
        else:
            is_real = all(e.is_real for e in witness)
            is_normal = bool(witness * witness.T == witness.T * witness)
            
            if not (is_real and is_normal):
                neg_q = True
            else:
                evs = witness.eigenvals()
                conclusion_holds = True
                for ev in evs:
                    try:
                        re, im = ev.as_real_imag()
                        if re.is_zero:
                            continue
                        if re.is_number:
                            if abs(float(re)) > 1e-9:
                                conclusion_holds = False
                                break
                        else:
                            # If symbolic and not explicitly zero, we cannot guarantee it satisfies the condition
                            conclusion_holds = False
                            break
                    except Exception:
                        conclusion_holds = False
                        break
                neg_q = not conclusion_holds
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The entries of A are real numbers",
    "H_2: A is a skew-symmetric matrix (A^T = -A)",
    "¬Q: A cannot be block-diagonalized into 1x1 zero matrices and 2x2 skew-symmetric blocks via a real orthogonal matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2