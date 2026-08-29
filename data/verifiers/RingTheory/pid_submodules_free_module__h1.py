import sympy
from sympy import gcd, groebner, reduced, Expr, Symbol, Poly, QQ, ZZ
from sympy.abc import x, y, z, t
import functools

# Top-level setup for Ring Theory
# Variables are available for the witness to use
# A typical counterexample witness for this conjecture: ([x, y], [x, y])
# which represents the ideal <x, y> in Q[x, y], or ([x], [2, x]) in Z[x].

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Submodules of Finitely Generated Free Modules over any ring are free of rank m <= n."
    (The true theorem requires the ring to be a PID).
    
    Expected witness format: (vars, N_gens) or (vars, n, N_gens)
    where:
      - vars is a list of SymPy symbols (e.g., [x, y])
      - n is the rank of the free module F = R^n (we only evaluate n = 1)
      - N_gens is a list of generators for the submodule N
    """
    try:
        if len(witness) == 2:
            vars, N_gens = witness
            n = 1
        elif len(witness) == 3:
            vars, n, N_gens = witness
            if not isinstance(n, int):
                return [False, False, False]
        else:
            return [False, False, False]
            
        if not isinstance(vars, (list, tuple)) or not all(isinstance(v, Symbol) for v in vars):
            return [False, False, False]
            
        if not isinstance(N_gens, (list, tuple)):
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

    # H_1: F is a free R-module of finite rank n
    try:
        h1_ok = (isinstance(n, int) and n >= 1 and len(vars) >= 1)
    except Exception:
        h1_ok = False

    # H_2: N is a submodule of F
    try:
        h2_ok = False
        if n == 1:
            h2_ok = all(isinstance(g, (Expr, int)) for g in N_gens)
        else:
            h2_ok = all(isinstance(g, (list, tuple)) and len(g) == n for g in N_gens)
    except Exception:
        h2_ok = False

    # neg_Q: N is NOT a free R-module of rank m <= n
    try:
        neg_q_ok = False
        if n == 1 and h1_ok and h2_ok:
            gens = [sympy.sympify(g) for g in N_gens if g != 0]
            if not gens:
                # N = {0}, which is free of rank 0 <= 1
                neg_q_ok = False
            else:
                # Determine the domain (ZZ if all generators have integer coefficients, else QQ)
                domain = 'ZZ'
                for g in gens:
                    p = Poly(g, *vars)
                    if not p.domain.is_ZZ:
                        domain = 'QQ'
                        break
                
                # In an integral domain, a free ideal must be of rank 1, hence principal.
                # N is principal iff the GCD of its generators is in N.
                g_gcd = functools.reduce(gcd, gens)
                GB = groebner(gens, *vars, domain=domain)
                rem = reduced(g_gcd, GB, *vars, domain=domain)[1]
                
                is_principal = (rem == 0)
                neg_q_ok = not is_principal
        elif n > 1:
            # Evaluation for n > 1 is not supported in this simple verifier
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a free R-module of finite rank n",
    "H_2: N is a submodule of F",
    "¬Q: N is NOT a free R-module of rank m <= n"
]

N_HYP = 2
NEG_Q_INDEX = 2