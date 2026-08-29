import sympy
from sympy import Matrix, MatrixBase, Symbol, simplify, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    
    Conjecture:
      Hypotheses:
        - Let J be the n x n matrix over a field F in which every entry is 1.
      Conclusion:
        - The characteristic polynomial of J is p(x) = x^{n-1}(x - n).
        
    (The dropped hypothesis is n >= 1. For n = 0, the 0x0 matrix has characteristic 
     polynomial 1, but the formula gives x^{-1}(x), which is not a valid polynomial.)
    """
    # H_1: J is a square matrix
    try:
        h1_ok = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1_ok = False

    # H_2: Every entry of J is 1
    try:
        if h1_ok:
            # For a 0x0 matrix, this vacuously evaluates to True, which is correct.
            h2_ok = all(val == 1 for val in witness)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The characteristic polynomial of J is NOT p(x) = x^{n-1}(x - n)
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            n = witness.rows
            if n == 0:
                # For n=0, the formula x^{n-1}(x-n) evaluates to x^{-1}(x), 
                # which is not a valid polynomial expression in F[x].
                neg_q_ok = True
            else:
                x = Symbol('x')
                cp = witness.charpoly(x).as_expr()
                expected = x**(n-1) * (x - n)
                diff = (cp - expected).expand()
                # If the difference is not zero, the conclusion fails (neg_Q is True)
                neg_q_ok = not (diff == 0 or diff.is_zero)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: J is a square matrix",
    "H_2: Every entry of J is 1",
    "¬Q: The characteristic polynomial of J is not p(x) = x^{n-1}(x - n)"
]

N_HYP = 2
NEG_Q_INDEX = 2