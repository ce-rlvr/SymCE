import sympy
from sympy import Matrix, eye, zeros, Symbol

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: P is a linear operator on V satisfying P^2 = P
    try:
        h1 = bool(witness**2 == witness)
    except Exception:
        h1 = False

    # H_2: P is not the zero operator
    try:
        from sympy import MatrixBase, zeros
        if isinstance(witness, MatrixBase):
            h2 = bool(witness != zeros(witness.rows, witness.cols))
        elif hasattr(witness, 'is_zero_matrix'):
            h2 = not witness.is_zero_matrix
        elif hasattr(witness, 'is_zero'):
            h2 = not witness.is_zero
        else:
            h2 = bool(witness != 0)
    except Exception:
        h2 = False

    # H_3: P is not the identity operator
    try:
        from sympy import MatrixBase, eye
        if isinstance(witness, MatrixBase):
            h3 = bool(witness != eye(witness.rows))
        elif hasattr(witness, 'is_Identity'):
            h3 = not witness.is_Identity
        elif hasattr(witness, 'is_identity'):
            h3 = not witness.is_identity
        else:
            h3 = bool(witness != 1)
    except Exception:
        h3 = False

    # ¬Q: The minimal polynomial of P is not m(x) = x^2 - x
    try:
        from sympy import Symbol
        x = Symbol('x')
        mp = None
        
        # Attempt to get the minimal polynomial from the witness directly
        if hasattr(witness, 'minpoly'):
            try:
                mp = witness.minpoly(x)
            except Exception:
                try:
                    mp = witness.minpoly()
                except Exception:
                    pass
                    
        # Fallback to sympy's minpoly function
        if mp is None:
            from sympy import minpoly
            mp = minpoly(witness, x)
            
        # Convert Poly objects to Expr if necessary
        if hasattr(mp, 'as_expr'):
            mp = mp.as_expr()
            
        # Normalize the variable to 'x' if there is exactly one free symbol
        free_syms = mp.free_symbols
        if len(free_syms) == 1:
            sym = list(free_syms)[0]
            mp = mp.subs(sym, x)
            
        # Check if the minimal polynomial is structurally different from x^2 - x
        neg_q = bool((mp - (x**2 - x)).expand() != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: P is a linear operator on V satisfying P^2 = P",
    "H_2: P is not the zero operator",
    "H_3: P is not the identity operator",
    "¬Q: The minimal polynomial of P is not m(x) = x^2 - x"
]

N_HYP = 3
NEG_Q_INDEX = 3