import sympy
from sympy import Symbol, QQ, GF, Rational, sqrt
from sympy.polys.polytools import Poly

# Top-level setup
# QQ and GF are available for the witness to specify the field F.

def conditions(witness):
    try:
        # Witness can be (F, a, b) or just (a, b) with implicit F = QQ
        if len(witness) == 3:
            F, a, b = witness
        elif len(witness) == 2:
            F = QQ
            a, b = witness
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    # H_1: F is a field of characteristic not equal to 2
    try:
        is_field = getattr(F, 'is_Field', False)
        try:
            char = F.characteristic()
        except TypeError:
            char = F.characteristic
        h1 = bool(is_field and char != 2)
    except Exception:
        h1 = False

    # H_2: a and b are elements of F
    try:
        a_F = F(a)
        b_F = F(b)
        h2 = True
    except Exception:
        h2 = False

    # H_3: a is not a square in F
    try:
        if F == QQ:
            a_sym = F.to_sympy(a_F)
            h3 = not sqrt(a_sym).is_rational
        else:
            try:
                char = F.characteristic()
            except TypeError:
                char = F.characteristic
            is_sq = False
            for i in range(char):
                if F(i)**2 == a_F:
                    is_sq = True
                    break
            h3 = not is_sq
    except Exception:
        h3 = False

    # H_4: ab is not a square in F
    try:
        ab_F = a_F * b_F
        if F == QQ:
            ab_sym = F.to_sympy(ab_F)
            h4 = not sqrt(ab_sym).is_rational
        else:
            try:
                char = F.characteristic()
            except TypeError:
                char = F.characteristic
            is_sq = False
            for i in range(char):
                if F(i)**2 == ab_F:
                    is_sq = True
                    break
            h4 = not is_sq
    except Exception:
        h4 = False

    # ¬Q: The minimal polynomial of sqrt(a) + sqrt(b) over F is not x^4 - 2(a+b)x^2 + (a-b)^2
    # The polynomial x^4 - 2(a+b)x^2 + (a-b)^2 has sqrt(a) + sqrt(b) as a root.
    # It is the minimal polynomial if and only if it is irreducible over F.
    # Therefore, the conclusion fails (¬Q is True) if the polynomial is reducible over F.
    try:
        x = Symbol('x')
        c4 = F(1)
        c3 = F(0)
        c2 = F(-2) * (a_F + b_F)
        c1 = F(0)
        c0 = (a_F - b_F)**2
        
        if hasattr(F, 'to_sympy'):
            coeffs = [F.to_sympy(c) for c in [c4, c3, c2, c1, c0]]
        else:
            coeffs = [c4, c3, c2, c1, c0]
            
        P = Poly(coeffs, x, domain=F)
        factors = P.factor_list()
        
        # factor_list returns (constant, [(factor1, multiplicity1), ...])
        # A degree 4 polynomial is irreducible iff it has exactly 1 factor with multiplicity 1
        is_irreducible = (len(factors[1]) == 1 and factors[1][0][1] == 1)
        neg_q = not is_irreducible
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: a and b are elements of F",
    "H_3: a is not a square in F",
    "H_4: ab is not a square in F",
    "¬Q: The minimal polynomial of sqrt(a) + sqrt(b) over F is not x^4 - 2(a+b)x^2 + (a-b)^2"
]

N_HYP = 4
NEG_Q_INDEX = 4