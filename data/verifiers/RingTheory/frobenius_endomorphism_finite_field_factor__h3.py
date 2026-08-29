import sympy as sp
from sympy.abc import x

def conditions(witness):
    """
    Given a witness (p, f), checks if it is a valid counterexample to the conjecture.
    The conjecture states that the Frobenius map phi(a) = a^p on F_p[x]/(f(x)) 
    is a well-defined F_p-algebra endomorphism.
    
    Mathematically, the Frobenius map is ALWAYS a well-defined F_p-algebra endomorphism 
    for any commutative F_p-algebra. The false conjecture arises from a true theorem 
    stating that if f(x) is irreducible (or square-free), then phi is an AUTOMORPHISM.
    The prompt's conclusion uses "endomorphism" (likely a typo for automorphism in the 
    dataset generation), so to correctly identify the intended counterexamples where the 
    conclusion fails, we check if phi fails to be an automorphism (i.e., f(x) is not square-free).
    """
    try:
        p, f = witness
    except Exception:
        return [False, False, False]
        
    # H_1: p is a prime number
    try:
        p_int = int(p)
        h1 = bool(sp.isprime(p_int))
    except Exception:
        h1 = False
        
    # H_2: F_p is the finite field with p elements
    # This holds by definition if p is prime.
    try:
        p_int = int(p)
        h2 = bool(sp.isprime(p_int))
    except Exception:
        h2 = False
        
    # ¬Q: The map phi is not a well-defined F_p-algebra endomorphism
    # We evaluate this by checking if it fails to be an automorphism.
    try:
        if isinstance(f, str):
            f = f.replace('^', '**')
        f_expr = sp.sympify(f)
        
        if f_expr == 0:
            # F_p[x]/(0) = F_p[x]. The map a -> a^p is not surjective, hence not an automorphism.
            is_auto = False
        else:
            syms = list(f_expr.free_symbols)
            if len(syms) > 1:
                is_auto = False
            else:
                var = syms[0] if len(syms) == 1 else x
                f_poly = sp.Poly(f_expr, var, domain=sp.GF(p_int))
                
                if f_poly.degree() <= 0:
                    # F_p[x]/(c) is the zero ring. The map 0 -> 0 is an automorphism.
                    is_auto = True
                else:
                    # For a finite ring F_p[x]/(f(x)), an endomorphism is an automorphism 
                    # if and only if it is injective, which holds iff f(x) is square-free.
                    f_diff = f_poly.diff()
                    gcd = f_poly.gcd(f_diff)
                    is_auto = (gcd.degree() == 0)
                    
        neg_q = not is_auto
    except Exception:
        # If f is not a valid polynomial, the map is not well-defined.
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: F_p is the finite field with p elements",
    "¬Q: The map phi is not a well-defined F_p-algebra endomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2