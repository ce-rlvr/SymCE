import sympy
from sympy import Matrix, oo
import itertools

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    T = None
    A = None
    x = None
    p = None

    # Parse the witness
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            A = witness.get('A')
            x = witness.get('x')
            p = witness.get('p')
        elif isinstance(witness, tuple):
            T = witness[0]
            for item in witness[1:]:
                if isinstance(item, Matrix):
                    if item.shape == T.shape:
                        A = item
                    elif item.shape[1] == 1:
                        x = item
                else:
                    p = item
        else:
            T = witness
    except Exception:
        pass

    # Default norm: 2-norm if a custom inner product A is provided, else 1-norm
    if p is None:
        p = 2 if A is not None else 1
    if p == 'inf':
        p = oo

    # H_1: T is a linear operator on V
    try:
        h1 = isinstance(T, Matrix) and T.is_square
    except Exception:
        h1 = False

    # H_2: T is a normal operator, meaning TT^* = T^*T
    try:
        if not h1:
            h2 = False
        else:
            if A is not None:
                # Adjoint with respect to the inner product <x, y>_A = x^H A y
                T_star = A.inv() * T.H * A
            else:
                # Standard conjugate transpose
                T_star = T.H
            
            diff = T * T_star - T_star * T
            h2 = bool(diff == sympy.zeros(*diff.shape))
    except Exception:
        h2 = False

    # ¬Q: ||T(x)|| != ||T^*(x)|| for some x in V
    neg_q = False
    try:
        if h1 and h2:
            vectors_to_test = [x] if x is not None else []
            if x is None:
                n = T.shape[0]
                # Generate a grid of small integer vectors to find a counterexample
                for vals in itertools.product([-2, -1, 0, 1, 2], repeat=n):
                    if all(v == 0 for v in vals): 
                        continue
                    vectors_to_test.append(Matrix(vals))
            
            for vec in vectors_to_test:
                Tx = T * vec
                T_star_x = T_star * vec
                val1 = Tx.norm(p)
                val2 = T_star_x.norm(p)
                
                if val1 != val2:
                    diff_val = val1 - val2
                    is_zero = False
                    try:
                        if hasattr(diff_val, 'is_zero') and diff_val.is_zero:
                            is_zero = True
                        elif diff_val.equals(0):
                            is_zero = True
                    except Exception:
                        pass
                    
                    if not is_zero:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V (represented as a square matrix)",
    "H_2: T is a normal operator, meaning TT^* = T^*T",
    "¬Q: ||T(x)|| != ||T^*(x)|| for some x in V"
]

N_HYP = 2
NEG_Q_INDEX = 2