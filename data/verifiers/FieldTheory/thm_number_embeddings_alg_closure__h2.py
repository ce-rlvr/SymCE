import sympy
from sympy import Symbol, Poly

# Top-level setup for potential witness expressions
t = Symbol('t')
x = Symbol('x')

def is_pth_power(expr, p):
    """Check if a rational function is a p-th power in characteristic p."""
    if p == 0:
        return False
    num, den = sympy.fraction(sympy.cancel(expr))
    
    def check_poly(poly_expr):
        if poly_expr.is_number:
            return True
        try:
            poly = sympy.Poly(poly_expr, domain=sympy.GF(p))
            for monom in poly.monoms():
                if any(e % p != 0 for e in monom):
                    return False
            return True
        except Exception:
            return False

    return check_poly(num) and check_poly(den)

def conditions(witness) -> list[bool]:
    try:
        f = None
        n = None
        
        # Extract the minimal polynomial f (representing L over K) and integer n
        if isinstance(witness, dict):
            vals = list(witness.values())
        elif isinstance(witness, (tuple, list)):
            vals = list(witness)
        else:
            vals = [witness]
            
        for item in vals:
            if isinstance(item, sympy.Poly):
                f = item
            elif isinstance(item, int) or (hasattr(item, 'is_Integer') and item.is_Integer):
                n = int(item)
                
        if f is None:
            K = None
            for item in vals:
                if hasattr(item, 'is_Field') and item.is_Field:
                    K = item
                elif hasattr(item, 'frac_field'):
                    K = item
            
            for item in vals:
                if isinstance(item, sympy.Expr) and not item.is_Integer and not item.is_Symbol:
                    try:
                        if K is not None:
                            f = sympy.Poly(item, domain=K)
                        else:
                            f = sympy.Poly(item)
                        if f.degree() > 0:
                            break
                    except Exception:
                        pass
                        
        if f is None or n is None:
            return [False, False, False]
            
        # H_1: K is a field
        h1 = f.domain.is_Field
        
        # H_2: E is an algebraically closed field containing K
        # The algebraic closure of a field always exists and contains it.
        h2 = h1  
        
        # Determine if f is irreducible over K (so L = K[x]/(f) is a field)
        try:
            is_irred = f.is_irreducible
            if is_irred is None:
                raise ValueError("Cannot determine irreducibility")
        except Exception:
            if f.degree() == 1:
                is_irred = True
            else:
                is_irred = False
                char = f.domain.char
                if char > 0:
                    deg = f.degree()
                    p_k = 1
                    while p_k < deg:
                        p_k *= char
                    # Fallback for inseparable polynomials like x^(p^k) - a
                    if p_k == deg:
                        monoms = f.monoms()
                        if [deg] in monoms and [0] in monoms and len(monoms) == 2:
                            c = f.nth(0)
                            c_expr = sympy.sympify(c)
                            if not is_pth_power(c_expr, char):
                                is_irred = True
                                
        if not is_irred:
            # If L is not a field, there are 0 field homomorphisms from L to E
            num_homomorphisms = 0
        else:
            # If L is a field, the number of embeddings into the algebraic closure
            # is the number of distinct roots of its minimal polynomial.
            char = f.domain.char
            if char == 0:
                num_homomorphisms = f.degree()
            else:
                exponents = [monom[0] for monom in f.monoms()]
                p_k = 1
                while all(e % (p_k * char) == 0 for e in exponents):
                    p_k *= char
                num_homomorphisms = f.degree() // p_k
                
        # ¬Q: The number of distinct field homomorphisms is NOT exactly n
        neg_q = (num_homomorphisms != n)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: E is an algebraically closed field containing K",
    "¬Q: The number of distinct field homomorphisms from L to E fixing K is not exactly n"
]

N_HYP = 2
NEG_Q_INDEX = 2