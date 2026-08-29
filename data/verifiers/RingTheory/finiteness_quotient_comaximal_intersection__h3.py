import sympy
from sympy import oo, gcd, lcm, degree
from sympy.abc import x

# Top-level setup for potential witness expressions
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    try:
        # Witness can be (R, I, J) or just (I, J) assuming R = 'ZZ'
        if len(witness) == 3:
            R, I, J = witness
        elif len(witness) == 2:
            R = 'ZZ'
            I, J = witness
        else:
            return [False, False, False]
            
        def get_gen(ideal):
            if isinstance(ideal, (list, tuple, set)):
                ideal = list(ideal)
                if len(ideal) == 0:
                    return sympy.Integer(0)
                g = sympy.sympify(ideal[0])
                for elem in ideal[1:]:
                    g = gcd(g, sympy.sympify(elem))
                return g
            return sympy.sympify(ideal)
            
        I = get_gen(I)
        J = get_gen(J)
    except Exception:
        return [False, False, False]
        
    # H1: R is a ring
    try:
        if R in ['ZZ', ZZ, 'QQ[x]']:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: I and J are comaximal ideals of R
    try:
        if R in ['ZZ', ZZ]:
            if not (I.is_integer and J.is_integer):
                h2 = False
            else:
                h2 = (gcd(I, J) in [1, -1])
        elif R == 'QQ[x]':
            if not (I.is_polynomial(x) and J.is_polynomial(x)):
                h2 = False
            else:
                g = gcd(I, J)
                h2 = (g != 0) and (degree(g, x) == 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: R/(I \cap J) is NOT finite, OR its cardinality is NOT |R/I| * |R/J|
    try:
        if R in ['ZZ', ZZ]:
            if not (I.is_integer and J.is_integer):
                return [h1, h2, False]
            card_I = abs(I) if I != 0 else oo
            card_J = abs(J) if J != 0 else oo
            cap = lcm(I, J)
            card_cap = abs(cap) if cap != 0 else oo
        elif R == 'QQ[x]':
            if not (I.is_polynomial(x) and J.is_polynomial(x)):
                return [h1, h2, False]
            def card(poly):
                if poly == 0:
                    return oo
                deg = degree(poly, x)
                if deg == 0:
                    return 1
                else:
                    return oo
            card_I = card(I)
            card_J = card(J)
            cap = lcm(I, J)
            card_cap = card(cap)
        else:
            card_I = card_J = card_cap = None
            
        if card_cap is None:
            neg_q = False
        else:
            is_finite = (card_cap != oo)
            if not is_finite:
                neg_q = True
            else:
                if card_I == oo or card_J == oo:
                    neg_q = True
                else:
                    neg_q = not (card_cap == card_I * card_J)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I and J are comaximal ideals of R",
    "¬Q: R/(I \\cap J) is not finite, or its cardinality is not |R/I| \\times |R/J|"
]

N_HYP = 2
NEG_Q_INDEX = 2