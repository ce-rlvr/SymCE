import sympy
from sympy import sqrt, Rational, Poly, I, QQ
from sympy.abc import x

# Top-level setup: named object bindings that the witness expression may reference.
F_field = QQ.algebraic_field(sqrt(-3))
f_poly = Poly(x**3 - 7, x, domain=F_field)

def conditions(witness) -> list[bool]:
    # H_1: Let F = Q(sqrt(-3))
    # This is a contextual definition, so it holds for any witness.
    h1 = True
    
    # H_2: Let f(x) = x^3 - 7 in F[x]
    # This is also a contextual definition.
    h2 = True
    
    # neg_Q: The degree of the extension is not 3, or E != F(cbrt(7))
    # The witness is a counterexample field E (or a representation of it).
    # If the witness IS F(cbrt(7)), then the conclusion holds, so neg_Q is False.
    # Otherwise, the conclusion fails, so neg_Q is True.
    neg_q = True
    try:
        is_F_cbrt = False
        
        # Check if witness is a SymPy AlgebraicField
        if hasattr(witness, 'degree') and callable(witness.degree):
            try:
                deg = witness.degree()
                # F(cbrt(7)) has degree 6 over Q
                if deg == 6:
                    exts = str(witness.exts).replace(' ', '').lower()
                    if ('7**(1/3)' in exts or 'cbrt(7)' in exts) and ('sqrt(-3)' in exts or 'i*sqrt(3)' in exts or 'sqrt(3)*i' in exts):
                        is_F_cbrt = True
            except Exception:
                pass
        
        # Check if witness is a string representation
        if not is_F_cbrt and isinstance(witness, str):
            s = witness.replace(' ', '').lower()
            if ('cbrt(7)' in s or '7**(1/3)' in s or '7**rational(1,3)' in s):
                is_F_cbrt = True
                
        # Check if witness is a tuple, e.g., (degree, field) or (F, f, E)
        if not is_F_cbrt and isinstance(witness, tuple):
            if len(witness) >= 2 and witness[0] == 3:
                s = str(witness[1]).replace(' ', '').lower()
                if ('cbrt(7)' in s or '7**(1/3)' in s or '7**rational(1,3)' in s):
                    is_F_cbrt = True
            elif len(witness) == 3:
                E = witness[2]
                if hasattr(E, 'degree') and callable(E.degree):
                    try:
                        if E.degree() == 6:
                            exts = str(E.exts).replace(' ', '').lower()
                            if ('7**(1/3)' in exts or 'cbrt(7)' in exts) and ('sqrt(-3)' in exts or 'i*sqrt(3)' in exts or 'sqrt(3)*i' in exts):
                                is_F_cbrt = True
                    except Exception:
                        pass
                if not is_F_cbrt and isinstance(E, str):
                    s = E.replace(' ', '').lower()
                    if ('cbrt(7)' in s or '7**(1/3)' in s or '7**rational(1,3)' in s):
                        is_F_cbrt = True
                        
        if is_F_cbrt:
            neg_q = False
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: F is Q(sqrt(-3))", "H_2: f(x) is x^3 - 7 over F", "¬Q: degree of E over F is not 3 or E is not F(cbrt(7))"]

N_HYP = 2
NEG_Q_INDEX = 2