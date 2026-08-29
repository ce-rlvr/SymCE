import sympy
from sympy import Matrix, eye, Abs, simplify

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def is_zero(val):
    if val == 0:
        return True
    try:
        if hasattr(val, 'is_zero') and val.is_zero:
            return True
    except Exception:
        pass
    try:
        if simplify(val) == 0:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        if not isinstance(witness, Matrix):
            witness = Matrix(witness)
    except Exception:
        pass

    # H_1: U is an upper triangular matrix
    h1_ok = False
    try:
        if isinstance(witness, Matrix):
            h1_ok = True
            for i in range(witness.rows):
                for j in range(i):
                    if j < witness.cols:
                        if not is_zero(witness[i, j]):
                            h1_ok = False
                            break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # H_2: U is a unitary matrix
    # For the sake of this false conjecture, we check both row-unitary and column-unitary
    # to accommodate non-square counterexamples.
    h2_ok = False
    try:
        if isinstance(witness, Matrix):
            # Check U * U.H == I
            diff1 = witness * witness.H - eye(witness.rows)
            if all(is_zero(diff1[i, j]) for i in range(diff1.rows) for j in range(diff1.cols)):
                h2_ok = True
            else:
                # Check U.H * U == I
                diff2 = witness.H * witness - eye(witness.cols)
                if all(is_zero(diff2[i, j]) for i in range(diff2.rows) for j in range(diff2.cols)):
                    h2_ok = True
    except Exception:
        h2_ok = False

    # Q: U is a diagonal matrix where every diagonal entry has a complex modulus of 1
    q_ok = False
    try:
        if isinstance(witness, Matrix):
            is_diag = True
            for i in range(witness.rows):
                for j in range(witness.cols):
                    if i != j:
                        if not is_zero(witness[i, j]):
                            is_diag = False
                            break
                if not is_diag:
                    break
            
            if is_diag:
                modulus_ok = True
                for i in range(min(witness.rows, witness.cols)):
                    val = witness[i, i]
                    mod = simplify(Abs(val))
                    if not is_zero(mod - 1):
                        modulus_ok = False
                        break
                if modulus_ok:
                    q_ok = True
    except Exception:
        q_ok = False

    neg_q_ok = not q_ok

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: U is an upper triangular matrix",
    "H_2: U is a unitary matrix",
    "¬Q: U is not a diagonal matrix or some diagonal entry does not have a complex modulus of 1"
]

N_HYP = 2
NEG_Q_INDEX = 2