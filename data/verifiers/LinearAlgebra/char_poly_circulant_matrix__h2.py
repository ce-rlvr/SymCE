import sympy
from functools import reduce

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    # H_1: Let n be a positive integer (implies witness is a square matrix of size n >= 1)
    try:
        if not isinstance(witness, sympy.MatrixBase):
            witness = sympy.Matrix(witness)
        h1 = bool(witness.is_square and witness.shape[0] >= 1)
    except Exception:
        h1 = False

    # H_2: Let \omega = e^{2\pi i / n} be a primitive n-th root of unity
    # This is a definitional hypothesis that always holds for any valid n >= 1
    try:
        h2 = h1
    except Exception:
        h2 = False

    # ¬Q: The roots of the characteristic polynomial of C are NOT given by the formula
    try:
        if not h1:
            neg_q = False
        else:
            n = witness.shape[0]
            _x = sympy.Symbol('__x__')
            char_poly = witness.charpoly(_x).as_expr()
            
            omega = sympy.exp(2 * sympy.pi * sympy.I / n)
            c = [witness[0, k] for k in range(n)]
            
            # \lambda_j = \sum_{k=0}^{n-1} c_k \omega^{jk}
            lambdas = [sum(c[k] * (omega ** (j * k)) for k in range(n)) for j in range(n)]
            
            # The expected characteristic polynomial if the roots were exactly \lambda_j
            expected_poly = reduce(lambda a, b: a * b, [_x - L for L in lambdas], 1)
            
            diff = sympy.expand(char_poly - expected_poly)
            
            if diff == 0:
                neg_q = False
            else:
                diff_simp = sympy.simplify(diff)
                if diff_simp == 0:
                    neg_q = False
                else:
                    # Numerical verification to catch unsimplified symbolic zeroes
                    try:
                        symbols = list(diff.free_symbols)
                        subs_dict = {}
                        for i, s in enumerate(symbols):
                            # Substitute arbitrary complex numbers to avoid accidental roots
                            subs_dict[s] = (1.234 + i * 0.567) + (2.345 - i * 0.123) * sympy.I
                        
                        val = complex(diff.subs(subs_dict).evalf())
                        neg_q = abs(val) >= 1e-7
                    except Exception:
                        # If numerical evaluation fails but symbolic diff is non-zero, assume they are different
                        neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: omega is a primitive n-th root of unity",
    "¬Q: The roots of the characteristic polynomial of C are not given by the formula"
]

N_HYP = 2
NEG_Q_INDEX = 2