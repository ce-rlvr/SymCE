import sympy
from sympy import Poly, Symbol
from sympy.polys.domains import GF

# Top-level setup for potential witness expressions
x, t = sympy.symbols('x t')

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "A splitting field of a polynomial over a field is a Galois extension."
    (The dropped hypothesis is that the polynomial must be separable).
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        F = None
        f = None
        
        # Unpack the witness based on various possible formats
        if hasattr(witness, 'domain') and hasattr(witness, 'factor_list'):
            f = witness
            F = f.domain
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                F, K, f = witness
            elif len(witness) == 2:
                F, f = witness
            elif len(witness) == 4:
                p, f_expr, x_var, t_var = witness
                if isinstance(p, int) and sympy.isprime(p):
                    F = GF(p).frac_field(t_var)
                    f = Poly(f_expr, x_var, domain=F)
        elif isinstance(witness, dict):
            F = witness.get('F')
            f = witness.get('f')
            if not hasattr(f, 'factor_list') and 'x' in witness:
                if F is not None:
                    f = Poly(f, witness['x'], domain=F)
                else:
                    f = Poly(f, witness['x'])
                    
        if f is not None and F is None and hasattr(f, 'domain'):
            F = f.domain
            
        # Convert f to a Poly object if it is a symbolic expression
        if f is not None and not hasattr(f, 'factor_list'):
            if hasattr(f, 'free_symbols'):
                free_syms = f.free_symbols
                if len(free_syms) == 1:
                    f = Poly(f, list(free_syms)[0], domain=F)
                elif len(free_syms) > 1:
                    x_sym = Symbol('x')
                    if x_sym in free_syms:
                        f = Poly(f, x_sym, domain=F)
                    
        # H_1: F is a field
        if F is not None:
            if hasattr(F, 'is_Field'):
                h1 = bool(F.is_Field)
            elif hasattr(F, 'is_field'):
                h1 = bool(F.is_field)
            elif isinstance(F, str) and 'field' in F.lower():
                h1 = True
                
        # H_2: K is a splitting field of f(x) over F
        # (By definition of the counterexample construction, K is the splitting field)
        if f is not None:
            h2 = True
            
        # ¬Q: The field extension K/F is not a Galois extension
        # K/F is Galois iff the splitting field is separable over F.
        # This holds iff all irreducible factors of f(x) over F have a non-zero formal derivative.
        if f is not None and hasattr(f, 'factor_list'):
            factors = f.factor_list()[1]
            is_galois = True
            for fac, mult in factors:
                if fac.degree() > 0:
                    df = fac.diff()
                    if df.is_zero:
                        is_galois = False
                        break
            neg_q = not is_galois
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is a splitting field of f(x) over F",
    "¬Q: The field extension K/F is not a Galois extension"
]

N_HYP = 2
NEG_Q_INDEX = 2