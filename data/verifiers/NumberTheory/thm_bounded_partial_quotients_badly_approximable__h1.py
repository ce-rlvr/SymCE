import sympy

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: alpha is a real number",
    "¬Q: The equivalence between bounded partial quotients and the Diophantine approximation condition fails"
]

def conditions(witness):
    try:
        witness = sympy.sympify(witness)
    except Exception:
        return [False, False]
        
    try:
        h1 = witness.is_real
    except Exception:
        h1 = False
        
    try:
        if h1:
            # For rational numbers, the sequence of partial quotients is finite (hence bounded),
            # but the Diophantine condition fails because we can choose p/q = alpha, giving 0 > c/q^2.
            # Thus, the "if and only if" equivalence fails for rational numbers.
            # For irrational numbers, the equivalence holds (this is the true Bounded Partial Quotients Theorem).
            if witness.is_rational:
                neg_q = True
            elif witness.is_irrational:
                neg_q = False
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]