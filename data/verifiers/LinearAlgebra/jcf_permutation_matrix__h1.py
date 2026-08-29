import sympy
from sympy import Matrix, eye, zeros, I, pi, Abs, arg, simplify
from sympy.matrices import MatrixBase

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: The underlying field is C
    # We verify this by checking if the witness is a square matrix in SymPy,
    # which inherently supports complex entries.
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    # ¬Q: The Jordan canonical form of P is NOT a diagonal matrix whose diagonal entries are roots of unity
    try:
        P, J = witness.jordan_form()
        if not J.is_diagonal():
            neg_q = True
        else:
            all_roots_of_unity = True
            for i in range(J.rows):
                val = J[i, i]
                # A root of unity must have an absolute value of 1
                if simplify(Abs(val)) != 1:
                    all_roots_of_unity = False
                    break
                # A root of unity must have an argument that is a rational multiple of pi
                a = simplify(arg(val) / pi)
                if not a.is_rational:
                    all_roots_of_unity = False
                    break
            neg_q = not all_roots_of_unity
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The underlying field is C",
    "¬Q: The Jordan canonical form of P is not a diagonal matrix whose diagonal entries are roots of unity"
]

N_HYP = 1
NEG_Q_INDEX = 1