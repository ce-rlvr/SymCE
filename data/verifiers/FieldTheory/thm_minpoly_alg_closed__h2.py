import sympy
from sympy import Matrix, Symbol, I, pi, E, eye, zeros

# Top-level setup
C = 'C'
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                F_name, alpha = witness
            else:
                return [False, False, False]
        elif isinstance(witness, dict):
            F_name = witness.get('F', 'C')
            alpha = witness.get('alpha')
        else:
            F_name = 'C'
            alpha = witness

        if isinstance(alpha, (int, float, complex)):
            alpha = sympy.sympify(alpha)
        elif isinstance(alpha, list):
            try:
                alpha = Matrix(alpha)
            except Exception:
                pass

        # H1: F is an algebraically closed field
        h1 = False
        if str(F_name) in ['C', 'Complexes', 'CC', 'AlgebraicNumbers'] or F_name in [sympy.S.Complexes, sympy.S.AlgebraicNumbers]:
            h1 = True

        # H2: \alpha \in K is algebraic over F
        h2 = False
        if isinstance(alpha, Matrix):
            if alpha.is_square and all(hasattr(sympy.sympify(e), 'is_number') and sympy.sympify(e).is_number for e in alpha):
                h2 = True
        elif hasattr(alpha, 'is_number') and alpha.is_number:
            h2 = True

        # Conclusion: The minimal polynomial of \alpha over F is x - \alpha.
        # For a matrix over C, the minimal polynomial has degree 1 if and only if it is a scalar matrix.
        concl = False
        if isinstance(alpha, Matrix):
            if alpha.is_square:
                n = alpha.shape[0]
                if n == 0:
                    concl = False
                else:
                    # Check if alpha is a scalar matrix (i.e., alpha == c * I)
                    if alpha == alpha[0,0] * eye(n):
                        concl = True
                    else:
                        concl = False
            else:
                concl = False
        else:
            # For a scalar in C, the minimal polynomial over C is x - \alpha (degree 1).
            concl = True

        neg_q = not concl

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is an algebraically closed field",
    "H_2: \\alpha \\in K is algebraic over F",
    "¬Q: The minimal polynomial of \\alpha over F is not x - \\alpha"
]

N_HYP = 2
NEG_Q_INDEX = 2