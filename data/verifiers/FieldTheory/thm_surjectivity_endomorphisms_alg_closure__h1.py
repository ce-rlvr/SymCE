import sympy
from sympy import S, Symbol, Rational, Integer
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: E is an algebraic closure of F",
    "H_2: \\sigma: E \\to E is a field homomorphism",
    "H_3: \\sigma(a) = a for all a \\in F",
    "¬Q: \\sigma is not a bijective map, and thus not an automorphism of E"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    h1, h2, h3, neg_q = False, False, False, False

    # 1. Dictionary-based mock witness
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('is_algebraic_closure', False) or witness.get('H1', False) or witness.get('h1', False))
            h2 = bool(witness.get('is_field_homomorphism', False) or witness.get('H2', False) or witness.get('h2', False))
            h3 = bool(witness.get('fixes_F', False) or witness.get('H3', False) or witness.get('h3', False))
            neg_q = bool(witness.get('not_bijective', False) or witness.get('neg_Q', False) or witness.get('neg_q', False))
            if any([h1, h2, h3, neg_q]):
                return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # 2. Tuple-based witness (E, F, sigma)
    if isinstance(witness, tuple) and len(witness) == 3:
        E, F, sigma = witness
        
        # Check H1
        try:
            if E == S.Complexes and F == S.Reals:
                h1 = True
            elif hasattr(E, 'is_algebraic_closure'):
                h1 = bool(E.is_algebraic_closure(F))
        except Exception:
            pass

        # Check H2
        try:
            if callable(sigma):
                test_vals = [sympy.Integer(1), sympy.Integer(0), sympy.I, sympy.pi]
                h2 = True
                for a in test_vals:
                    for b in test_vals:
                        if sympy.simplify(sigma(a + b) - (sigma(a) + sigma(b))) != 0:
                            h2 = False
                        if sympy.simplify(sigma(a * b) - (sigma(a) * sigma(b))) != 0:
                            h2 = False
                if sympy.simplify(sigma(sympy.Integer(1)) - sympy.Integer(1)) != 0:
                    h2 = False
            elif hasattr(sigma, 'is_field_homomorphism'):
                h2 = bool(sigma.is_field_homomorphism())
        except Exception:
            pass

        # Check H3
        try:
            if callable(sigma) and F == S.Reals:
                test_f = [sympy.Integer(1), sympy.Integer(0), sympy.pi, sympy.Rational(1, 2)]
                h3 = True
                for a in test_f:
                    if sympy.simplify(sigma(a) - a) != 0:
                        h3 = False
            elif hasattr(sigma, 'fixes'):
                h3 = bool(sigma.fixes(F))
        except Exception:
            pass

        # Check neg_Q
        try:
            if hasattr(sigma, 'is_bijective'):
                neg_q = not bool(sigma.is_bijective())
            else:
                neg_q = False
        except Exception:
            pass

        if any([h1, h2, h3, neg_q]):
            return [h1, h2, h3, neg_q]

    # 3. Object-based mock witness with properties/methods
    try:
        if hasattr(witness, 'H1'): h1 = bool(witness.H1)
        elif hasattr(witness, 'h1'): h1 = bool(witness.h1)
        else:
            h1_val = getattr(witness, 'is_algebraic_closure', None)
            if callable(h1_val): h1 = bool(h1_val())
            elif h1_val is not None: h1 = bool(h1_val)
            elif hasattr(witness, 'E') and hasattr(witness.E, 'is_algebraic_closure'):
                h1 = bool(witness.E.is_algebraic_closure(getattr(witness, 'F', None)))
    except Exception:
        pass

    try:
        if hasattr(witness, 'H2'): h2 = bool(witness.H2)
        elif hasattr(witness, 'h2'): h2 = bool(witness.h2)
        else:
            h2_val = getattr(witness, 'is_field_homomorphism', None)
            if callable(h2_val): h2 = bool(h2_val())
            elif h2_val is not None: h2 = bool(h2_val)
            elif hasattr(witness, 'sigma') and hasattr(witness.sigma, 'is_field_homomorphism'):
                h2 = bool(witness.sigma.is_field_homomorphism())
    except Exception:
        pass

    try:
        if hasattr(witness, 'H3'): h3 = bool(witness.H3)
        elif hasattr(witness, 'h3'): h3 = bool(witness.h3)
        else:
            h3_val = getattr(witness, 'fixes_F', None)
            if callable(h3_val): h3 = bool(h3_val())
            elif h3_val is not None: h3 = bool(h3_val)
            elif hasattr(witness, 'sigma') and hasattr(witness.sigma, 'fixes'):
                h3 = bool(witness.sigma.fixes(getattr(witness, 'F', None)))
    except Exception:
        pass

    try:
        if hasattr(witness, 'neg_Q'): neg_q = bool(witness.neg_Q)
        elif hasattr(witness, 'neg_q'): neg_q = bool(witness.neg_q)
        else:
            is_bij = getattr(witness, 'is_bijective', None)
            if callable(is_bij): neg_q = not bool(is_bij())
            elif is_bij is not None: neg_q = not bool(is_bij)
            elif hasattr(witness, 'sigma') and hasattr(witness.sigma, 'is_bijective'):
                sigma_bij = witness.sigma.is_bijective
                neg_q = not bool(sigma_bij() if callable(sigma_bij) else sigma_bij)
    except Exception:
        pass

    return [h1, h2, h3, neg_q]