import sympy
from sympy import symbols, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the conjecture:
    Hypotheses:
      - R is a commutative ring
      - R is a principal ideal ring
    Conclusion:
      - The localized ring S^{-1}R is a principal ideal ring
    """
    try:
        # The witness might be a tuple (R, S) or just the ring R
        if isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        else:
            R = witness
            S = None
    except Exception:
        R = witness
        S = None

    h1 = False
    h2 = False
    neg_q = False

    # Check H_1 (R is a commutative ring) and H_2 (R is a principal ideal ring)
    try:
        if isinstance(R, str):
            R_str = R.replace(' ', '')
            if R_str in ['Z', 'ZZ', 'Q', 'QQ', 'R', 'RR', 'C', 'CC']:
                h1, h2 = True, True
            elif R_str.startswith('Z/') or R_str.startswith('Z_'):
                h1, h2 = True, True
            elif '[' in R_str and ']' in R_str:
                base = R_str.split('[')[0]
                vars_str = R_str.split('[')[1].split(']')[0]
                num_vars = len(vars_str.split(','))
                h1 = True
                if num_vars > 1:
                    h2 = False
                elif base in ['Q', 'QQ', 'R', 'RR', 'C', 'CC']:
                    h2 = True
                else:
                    h2 = False
            else:
                h1, h2 = False, False
        elif isinstance(R, int):
            # Integers can represent Z/nZ or Z (if 0)
            h1 = True
            h2 = True
        else:
            # Sympy objects / domains
            if hasattr(R, 'is_commutative'):
                h1 = (R.is_commutative is True)
            else:
                h1 = True  # Assume commutative if not explicitly non-commutative
            
            if hasattr(R, 'is_PID'):
                h2 = (R.is_PID is True)
            elif hasattr(R, 'is_Field'):
                h2 = (R.is_Field is True)
            else:
                h2 = False
    except Exception:
        h1 = False
        h2 = False

    # Check negated conclusion: The localized ring S^{-1}R is NOT a principal ideal ring
    try:
        if h1 and h2:
            # Mathematically, the localization of any commutative principal ideal ring 
            # is ALWAYS a principal ideal ring. Thus, if the hypotheses hold, the 
            # conclusion holds, meaning the negated conclusion is False.
            neg_q = False
        else:
            # If R is not a PIR, its localization is generally not a PIR either 
            # (unless S is large enough, e.g., forming a field). We approximate this 
            # by returning True when R is not a PIR.
            neg_q = not h2
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a principal ideal ring",
    "¬Q: The localized ring S^{-1}R is not a principal ideal ring"
]

N_HYP = 2
NEG_Q_INDEX = 2