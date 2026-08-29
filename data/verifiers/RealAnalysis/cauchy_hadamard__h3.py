import sympy
from sympy import Symbol, limit, oo, Abs, sympify

# Top-level setup: named object bindings that the witness expression may reference.
n = Symbol('n', integer=True, positive=True)
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (a_expr, c, L, R)
    where:
      - a_expr is the n-th coefficient of the power series (as a sympy expression in terms of n)
      - c is the center of the power series
      - L is the limsup of |a_n|^(1/n)
      - R is the claimed (but incorrect) radius of convergence
    """
    try:
        if len(witness) != 4:
            return [False, False, False]
        a_expr, c, L, R = witness
    except Exception:
        return [False, False, False]
        
    # H_1: a_n (x-c)^n is a power series
    try:
        a_expr = sympify(a_expr)
        c = sympify(c)
        h1_ok = True
    except Exception:
        h1_ok = False
        
    # H_2: L = \limsup_{n \to \infty} |a_n|^{1/n}
    try:
        L = sympify(L)
        # For the purpose of verification, we check if the limit exists and equals L.
        # A valid counterexample can simply use a sequence where the limit exists.
        L_calc = limit(Abs(a_expr)**(1/n), n, oo)
        if L_calc == L:
            h2_ok = True
        elif sympy.simplify(L_calc - L) == 0:
            h2_ok = True
        else:
            h2_ok = False
    except Exception:
        h2_ok = False
        
    # ¬Q: The radius of convergence of the power series is NOT exactly R.
    # By Cauchy-Hadamard, the actual radius of convergence is 1/L.
    try:
        R = sympify(R)
        if L == 0:
            actual_R = oo
        else:
            actual_R = 1 / L
            
        if actual_R != R and sympy.simplify(actual_R - R) != 0:
            neg_q_ok = True
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a_n (x-c)^n is a power series",
    "H_2: L = limsup |a_n|^(1/n)",
    "¬Q: The radius of convergence is not exactly R"
]

N_HYP = 2
NEG_Q_INDEX = 2