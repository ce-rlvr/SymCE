import sympy
import sympy.combinatorics.named_groups

Q = sympy.S.Rationals
Reals = sympy.S.Reals
Complexes = sympy.S.Complexes
Z = sympy.S.Integers
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: D is a divisible abelian group",
    "H_2: f is a group homomorphism from D to R",
    "¬Q: f is not the trivial homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        D, R_codomain, f = witness
    except Exception:
        return [False, False, False]
    
    # H_1: D is a divisible abelian group
    try:
        if D in [sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]:
            h1 = True
        elif hasattr(D, 'is_group') and D.is_group and D.order() == 1:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: f is a group homomorphism from D to R
    try:
        x, y = sympy.symbols('x y')
        
        # Check additive homomorphism: f(x + y) = f(x) + f(y)
        is_hom = (sympy.simplify(f(x + y) - (f(x) + f(y))) == 0)
        
        # Check if f maps D to R_codomain
        def in_codomain(val, codomain):
            val = sympy.sympify(val)
            if codomain == sympy.S.Integers:
                return val.is_integer
            if codomain == sympy.S.Rationals:
                return val.is_rational
            if codomain == sympy.S.Reals:
                return val.is_real
            if codomain == sympy.S.Complexes:
                return val.is_complex
            return True
            
        maps_to_codomain = in_codomain(f(sympy.Integer(1)), R_codomain) and \
                           in_codomain(f(sympy.Rational(1, 2)), R_codomain)
                           
        h2 = bool(is_hom and maps_to_codomain)
    except Exception:
        h2 = False
        
    # ¬Q: f is not the trivial homomorphism
    try:
        x = sympy.symbols('x')
        # For additive groups, the trivial homomorphism maps everything to 0
        is_trivial = (sympy.simplify(f(x)) == 0)
        neg_q = not is_trivial
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]