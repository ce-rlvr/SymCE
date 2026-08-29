import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H1: A is an n x n matrix
    try:
        if hasattr(witness, 'to_Matrix'):
            witness = witness.to_Matrix()
        elif not isinstance(witness, sympy.MatrixBase):
            witness = sympy.Matrix(witness)
        
        h1 = len(witness.shape) == 2 and witness.shape[0] == witness.shape[1]
        n = witness.shape[0] if h1 else 0
    except Exception:
        h1 = False
        n = 0

    # H2: A is involutory (A^2 = I)
    h2 = False
    if h1:
        try:
            A_sq = witness * witness
            is_involutory = True
            for i in range(n):
                for j in range(n):
                    expected = 1 if i == j else 0
                    diff = A_sq[i, j] - expected
                    if diff != 0:
                        is_involutory = False
                        break
                if not is_involutory:
                    break
            h2 = is_involutory
        except Exception:
            h2 = False

    # neg_Q: A is NOT diagonalizable OR has eigenvalues other than 1, -1
    neg_q = False
    if h1 and h2:
        try:
            if n == 0:
                neg_q = False
            else:
                # Over a field F, an involutory matrix A (A^2 = I) has minimal polynomial dividing x^2 - 1.
                # The roots of x^2 - 1 are 1 and -1.
                # Thus, the eigenvalues are always in {1, -1}.
                # A is diagonalizable iff its minimal polynomial has distinct roots.
                # If char(F) != 2, 1 != -1, so x^2 - 1 has distinct roots, and A is always diagonalizable.
                # If char(F) == 2, 1 == -1, so x^2 - 1 = (x-1)^2. A is diagonalizable iff min poly divides x-1, i.e., A = I.
                # Therefore, the conclusion fails iff char(F) == 2 and A != I.
                
                one = A_sq[0, 0]
                two = one + one
                char_is_2 = (two == 0)
                
                A_eq_I = True
                for i in range(n):
                    for j in range(n):
                        expected = 1 if i == j else 0
                        diff = witness[i, j] - expected
                        if diff != 0:
                            A_eq_I = False
                            break
                    if not A_eq_I:
                        break
                
                if char_is_2 and not A_eq_I:
                    neg_q = True
        except Exception:
            neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix",
    "H_2: A is involutory (A^2 = I)",
    "¬Q: A is not diagonalizable or has eigenvalues other than 1 and -1"
]

N_HYP = 2
NEG_Q_INDEX = 2