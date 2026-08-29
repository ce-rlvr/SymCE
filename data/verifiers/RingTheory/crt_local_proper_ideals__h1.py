import sympy

# Top-level setup
Z = sympy.S.Integers

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                _, I, J = witness
            elif len(witness) == 2:
                I, J = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if isinstance(I, (list, tuple)) and len(I) == 1:
            I = I[0]
        if isinstance(J, (list, tuple)) and len(J) == 1:
            J = J[0]
            
        I = sympy.sympify(I)
        J = sympy.sympify(J)
        
        h1 = False
        h2 = False
        neg_q = False
        
        if I.is_Integer and J.is_Integer:
            h1 = (abs(I) != 1)
            h2 = (abs(J) != 1)
            neg_q = (sympy.gcd(I, J) == 1)
        else:
            I_poly = sympy.Poly(I)
            J_poly = sympy.Poly(J)
            h1 = not (I_poly.is_constant() and not I_poly.is_zero)
            h2 = not (J_poly.is_constant() and not J_poly.is_zero)
            g = sympy.gcd(I, J)
            g_poly = sympy.Poly(g)
            neg_q = bool(g_poly.is_constant() and not g_poly.is_zero)
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "H_2: J is a proper ideal of R",
    "¬Q: I and J are comaximal"
]

N_HYP = 2
NEG_Q_INDEX = 2