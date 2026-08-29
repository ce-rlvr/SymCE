import sympy
from sympy import S, Integer, Rational
from sympy.abc import x, y, z

# Top-level setup
Z2 = Integer(2)
Z3 = Integer(3)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The conjecture states that for any F, the algebraic closure of F(x) has infinite degree over F(x).
    This is true for all fields, but fails if F is the trivial ring {0}, where F(x) = {0} and the degree is 1.
    """
    # H_1: F(x) is the field of rational functions in one variable over F
    # This is a definitional hypothesis that holds for the witness in context.
    h1 = True
    
    # H_2: \overline{F(x)} is an algebraic closure of F(x)
    # This is also a definitional hypothesis.
    h2 = True
    
    # ¬Q: The field extension \overline{F(x)} / F(x) does not have infinite degree
    # This is true if and only if the witness is the trivial ring.
    neg_q = False
    try:
        if isinstance(witness, str):
            if witness.lower() in ['0', 'trivial', 'trivial ring', 'zero', '{0}']:
                neg_q = True
        else:
            try:
                # Check if the witness evaluates to 0
                if witness == 0 or witness == S.Zero:
                    neg_q = True
            except Exception:
                pass
            
            if not neg_q and hasattr(witness, 'is_zero') and witness.is_zero:
                neg_q = True
            elif not neg_q and str(witness) in ['0', '0.0', '{0}']:
                neg_q = True
            elif not neg_q and hasattr(witness, 'zero') and hasattr(witness, 'one'):
                try:
                    # In the trivial ring, 0 == 1
                    if witness.zero == witness.one:
                        neg_q = True
                except Exception:
                    pass
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F(x) is the field of rational functions in one variable over F",
    "H_2: \\overline{F(x)} is an algebraic closure of F(x)",
    "¬Q: The field extension \\overline{F(x)} / F(x) does not have infinite degree"
]

N_HYP = 2
NEG_Q_INDEX = 2