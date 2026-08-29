import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: Let F be a field
    # In the context of SymPy, we verify the witness is a matrix (its entries implicitly belong to a field)
    try:
        h1 = isinstance(witness, sympy.MatrixBase)
    except Exception:
        h1 = False

    # H_2: Let D be an n \times n diagonal matrix over F
    try:
        h2 = h1 and witness.is_square and witness.is_diagonal()
    except Exception:
        h2 = False

    # ¬Q: The characteristic polynomial of D is NOT p(x) = \prod_{i=1}^n (x - d_i)
    try:
        x = sympy.Dummy('x')
        # Compute the characteristic polynomial using SymPy
        cp = witness.charpoly(x).as_expr()
        
        # Compute the product \prod_{i=1}^n (x - d_i) where d_i are the diagonal entries
        n = witness.rows
        prod = sympy.Integer(1)
        for i in range(n):
            prod *= (x - witness[i, i])
            
        # Check if they are equal
        diff = sympy.simplify(sympy.expand(cp - prod))
        q = (diff == 0)
        neg_q = not q
    except Exception:
        # If characteristic polynomial or product cannot be computed, the conclusion fails
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: D is an n x n diagonal matrix over F",
    "¬Q: The characteristic polynomial of D is not \\prod_{i=1}^n (x - d_i)"
]

N_HYP = 2
NEG_Q_INDEX = 2