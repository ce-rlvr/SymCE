import sympy
from sympy import Poly, integer_nthroot, cyclotomic_poly
from sympy.abc import x, y, z

# Top-level setup
# x, y, z are provided for convenience in defining polynomials for the extensions

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is that K and L are subfields of a common field.
    Without a common overfield, the composite field KL and intersection K \cap L are undefined.
    
    Expected witness format: a tuple (f, g) of two SymPy expressions/polynomials 
    representing the abstract extensions K = Q[x]/(f) and L = Q[y]/(g).
    """
    try:
        f = witness[0]
        g = witness[1]
        
        # H_1: K/F is a finite Galois extension
        try:
            f_poly = Poly(f, domain='QQ')
            h1 = f_poly.degree() > 0 and f_poly.is_irreducible
            if h1:
                d = f_poly.degree()
                if d <= 2:
                    h1 = True
                elif d == 3:
                    disc = f_poly.discriminant()
                    if disc > 0:
                        num, den = sympy.Rational(disc).as_numer_denom()
                        _, exact_num = integer_nthroot(int(num), 2)
                        _, exact_den = integer_nthroot(int(den), 2)
                        h1 = exact_num and exact_den
                    else:
                        h1 = False
                else:
                    gen = f_poly.gen
                    is_cyclo = False
                    for n in range(1, 50):
                        if f_poly == Poly(cyclotomic_poly(n, gen), gen, domain='QQ'):
                            is_cyclo = True
                            break
                    h1 = is_cyclo
        except Exception:
            h1 = False
            
        # H_2: L/F is a field extension
        try:
            g_poly = Poly(g, domain='QQ')
            h2 = g_poly.degree() > 0 and g_poly.is_irreducible
        except Exception:
            h2 = False
            
        # ¬Q: The conclusion fails because KL is undefined.
        # If the witness provides a 3rd element (a common field), the theorem holds, so neg_Q is False.
        # If it only provides K and L as abstract extensions, KL is undefined, so the conclusion fails.
        if len(witness) >= 3:
            neg_q = False
        else:
            neg_q = True
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: K/F is a finite Galois extension",
    "H_2: L/F is a field extension",
    "¬Q: The composite field KL is undefined (K and L are not in a common field), so the conclusion fails"
]

N_HYP = 2
NEG_Q_INDEX = 2