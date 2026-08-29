import sympy
from sympy import Matrix, I, Abs, simplify, im

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Given a witness object, checks if it is a valid counterexample to the conjecture.
    Returns a list of booleans: [H_1_ok, neg_Q_ok].
    """
    # H1: There exists a real number M > 0 such that the matrix norm \|A^k\| \le M for all integers k \in \mathbb{Z}
    # This holds iff A is invertible, diagonalizable over C, and all its eigenvalues have absolute value 1.
    h1_ok = False
    try:
        if isinstance(witness, Matrix) and witness.is_square:
            if witness.det() != 0:
                if witness.is_diagonalizable():
                    evs = witness.eigenvals()
                    all_abs_one = True
                    for ev in evs:
                        is_one = False
                        if Abs(ev) == 1:
                            is_one = True
                        elif simplify(Abs(ev)) == 1:
                            is_one = True
                        else:
                            try:
                                if abs(float(Abs(ev)) - 1.0) < 1e-9:
                                    is_one = True
                            except Exception:
                                pass
                        if not is_one:
                            all_abs_one = False
                            break
                    h1_ok = all_abs_one
    except Exception:
        h1_ok = False

    # neg_Q: A is NOT a diagonalizable matrix
    # For a real matrix, "diagonalizable" in this context means diagonalizable over R.
    # It is not diagonalizable over R if it is not diagonalizable over C, or if it has non-real eigenvalues.
    neg_q_ok = False
    try:
        if isinstance(witness, Matrix) and witness.is_square:
            is_real_matrix = True
            for val in witness:
                if val.is_real is False:
                    is_real_matrix = False
                    break
                if val.is_real is None:
                    try:
                        if abs(float(im(val))) > 1e-9:
                            is_real_matrix = False
                            break
                    except Exception:
                        pass
            
            if is_real_matrix:
                if not witness.is_diagonalizable():
                    neg_q_ok = True
                else:
                    evs = witness.eigenvals()
                    has_non_real = False
                    for ev in evs:
                        if ev.is_real is False:
                            has_non_real = True
                            break
                        if ev.is_real is None:
                            try:
                                if abs(float(im(ev))) > 1e-9:
                                    has_non_real = True
                                    break
                            except Exception:
                                pass
                    neg_q_ok = has_non_real
            else:
                # If it's a complex matrix, we just check diagonalizability over C
                neg_q_ok = not witness.is_diagonalizable()
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: There exists M > 0 such that ||A^k|| <= M for all k in Z",
    "¬Q: A is not a diagonalizable matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1