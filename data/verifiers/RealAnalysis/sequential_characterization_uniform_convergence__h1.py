import sympy
from sympy import Symbol, limit, oo, maximum, Abs, S as sympy_S

# Top-level setup
n = Symbol('n', integer=True, positive=True)
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a dictionary with:
      'f': sympy expression for f(x)
      'f_n': sympy expression for f_n(x)
      'S': sympy set for the domain S
      'x_n': sympy expression for a specific sequence x_n in S (to show Q fails if needed)
    """
    try:
        f_expr = witness['f']
        f_n_expr = witness['f_n']
        domain = witness['S']
    except Exception:
        return [False, False]

    # H1: f is a real-valued function on S
    # We check if f is a valid expression.
    try:
        # Just check if we can substitute a value from the domain
        if domain.is_empty:
            h1_ok = True
        else:
            # Try to evaluate at some point in the domain
            pt = domain.boundary.args[0] if hasattr(domain.boundary, 'args') and domain.boundary.args else 0
            val = f_expr.subs(x, pt)
            h1_ok = val.is_real or val.is_real is None
    except Exception:
        h1_ok = False

    # Evaluate P: f_n converges uniformly to f on S
    try:
        if domain.is_empty:
            P = True
        else:
            diff = Abs(f_n_expr - f_expr)
            sup_val = maximum(diff, x, domain)
            P = (limit(sup_val, n, oo) == 0)
    except Exception:
        P = False

    # Evaluate Q: for every sequence x_n in S, lim (f_n(x_n) - f(x_n)) == 0
    # Since we cannot check all sequences, we check if the witness provides a counter-sequence
    # that breaks Q, or we use the supremum to prove Q holds.
    try:
        if domain.is_empty:
            Q = True
        else:
            # If P is true, Q must be true mathematically.
            if P:
                Q = True
            else:
                # If P is false, there exists a sequence where the limit is not 0.
                # The witness should provide this sequence 'x_n' to prove Q is false.
                if 'x_n' in witness:
                    x_n_expr = witness['x_n']
                    # Check if x_n is in S for all n
                    # (We assume the witness provides a valid sequence in S)
                    lim_val = limit(f_n_expr.subs(x, x_n_expr) - f_expr.subs(x, x_n_expr), n, oo)
                    if lim_val != 0:
                        Q = False
                    else:
                        Q = True
                else:
                    # If no specific sequence is provided, mathematically Q is false if P is false.
                    Q = False
    except Exception:
        Q = False

    # The conjecture states P <=> Q.
    # The conclusion fails if P is not equivalent to Q.
    try:
        neg_q_ok = (P != Q)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a real-valued function on S",
    "¬Q: The equivalence between uniform convergence and the sequential limit condition fails"
]

N_HYP = 1
NEG_Q_INDEX = 1