import sympy
from sympy.polys import cyclotomic_poly
from sympy.ntheory import totient

# Top-level setup for potential witness expressions
x = sympy.Symbol('x')

def conditions(witness):
    n = None
    x_val = None
    phi_n = None

    # Extract n, x, and optionally phi_n from the witness
    if isinstance(witness, dict):
        n = witness.get('n')
        x_val = witness.get('x')
        phi_n = witness.get('phi_n', witness.get('phi'))
    elif isinstance(witness, (list, tuple)):
        if len(witness) == 2:
            n, x_val = witness
        elif len(witness) == 3:
            n, phi_n, x_val = witness
        elif len(witness) >= 1:
            n = witness[0]
    else:
        n = witness

    # H_1: n is an integer strictly greater than 1
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 1
    except Exception:
        h1 = False

    # H_2: phi(n) is Euler's totient function evaluated at n
    try:
        if phi_n is not None:
            h2 = bool(phi_n == totient(n))
        else:
            # If not explicitly provided, the definition trivially holds
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: The polynomial satisfies the identity x^{\phi(n)}\Phi_n(1/x) = \Phi_n(x)
    # We check if this identity FAILS at the witness.
    try:
        if x_val is None:
            # If no specific x is provided, evaluate the identity symbolically
            X = sympy.Symbol('X')
            tot = totient(n)
            poly = cyclotomic_poly(n, X)
            lhs = (X ** tot) * poly.subs(X, 1/X)
            rhs = poly
            q_ok = sympy.simplify(lhs - rhs) == 0
        else:
            # Evaluate the identity at the specific x provided in the witness
            tot = totient(n)
            X = sympy.Symbol('X')
            poly = cyclotomic_poly(n, X)
            
            rhs = poly.subs(X, x_val)
            
            # Attempt to compute 1/x, handling division by zero (e.g., Lean semantics where 1/0 = 0)
            try:
                is_zero = False
                try:
                    is_zero = bool(x_val == 0)
                except Exception:
                    pass
                
                if is_zero:
                    inv_x = 0
                elif hasattr(x_val, 'inv'):
                    inv_x = x_val.inv()
                else:
                    inv_x = 1 / x_val
            except Exception:
                inv_x = 0
                
            lhs = (x_val ** tot) * poly.subs(X, inv_x)
            
            if isinstance(lhs, sympy.Basic) or isinstance(rhs, sympy.Basic):
                q_ok = sympy.simplify(lhs - rhs) == 0
            else:
                q_ok = (lhs == rhs)
                
        neg_q = not q_ok
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: phi(n) is Euler's totient function evaluated at n",
    "¬Q: The identity x^phi(n) * Phi_n(1/x) = Phi_n(x) fails at the witness"
]

N_HYP = 2
NEG_Q_INDEX = 2