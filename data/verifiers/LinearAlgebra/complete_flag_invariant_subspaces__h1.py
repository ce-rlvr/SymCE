import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    'Every linear operator T on V has a complete flag of invariant subspaces.'
    """
    try:
        # H_1: T is a linear operator on V (represented as a square matrix)
        is_linear_operator = isinstance(witness, Matrix) and witness.is_square
    except Exception:
        is_linear_operator = False

    try:
        if not is_linear_operator:
            neg_q = False
        else:
            x = sympy.Symbol('x')
            try:
                # A linear operator has a complete flag of invariant subspaces iff
                # its characteristic polynomial splits completely into linear factors
                # over the base field. We check if it splits over the field generated
                # by its entries.
                
                # Convert to rational to avoid float issues in factor_list
                rational_witness = Matrix(witness.rows, witness.cols, [sympy.nsimplify(val, rational=True) for val in witness])
                p = rational_witness.charpoly(x)
                factors = sympy.factor_list(p.as_expr())
                
                splits_completely = True
                for f, mult in factors[1]:
                    if sympy.Poly(f, x).degree() > 1:
                        splits_completely = False
                        break
                
                # neg_Q is True if it does NOT split completely
                neg_q = not splits_completely
                
            except Exception:
                # Fallback: check if all eigenvalues are real
                eigenvals = witness.eigenvals()
                all_real = True
                for ev in eigenvals.keys():
                    try:
                        if ev.is_real is False:
                            all_real = False
                        elif abs(complex(ev).imag) > 1e-9:
                            all_real = False
                    except Exception:
                        all_real = False
                neg_q = not all_real
    except Exception:
        neg_q = False

    return [is_linear_operator, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "¬Q: T does not have a complete flag of invariant subspaces"
]

N_HYP = 1
NEG_Q_INDEX = 1