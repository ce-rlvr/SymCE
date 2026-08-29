import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Returns a list of booleans: [H_1_ok, H_2_ok, H_3_ok, neg_Q_ok]
    """
    # Extract R, I, n from the witness if it's a structured object
    R, I, n = None, None, None
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            n = witness.get('n')
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, I, n = witness
        else:
            R = getattr(witness, 'R', None)
            I = getattr(witness, 'I', None)
            n = getattr(witness, 'n', None)
    except Exception:
        pass

    # H_1: R has an identity element 1 \neq 0
    h1 = False
    try:
        if isinstance(witness, dict) and 'H1' in witness:
            h1 = bool(witness['H1'])
        elif hasattr(witness, 'R_has_identity'):
            h1 = bool(witness.R_has_identity())
        elif hasattr(witness, 'H1'):
            h1 = bool(witness.H1)
        elif R is not None:
            if hasattr(R, 'has_identity'):
                h1 = bool(R.has_identity() if callable(R.has_identity) else R.has_identity)
            elif hasattr(R, 'one') and hasattr(R, 'zero'):
                h1 = bool(R.one != R.zero)
    except Exception:
        h1 = False

    # H_2: I is a proper ideal of R
    h2 = False
    try:
        if isinstance(witness, dict) and 'H2' in witness:
            h2 = bool(witness['H2'])
        elif hasattr(witness, 'I_is_proper_ideal'):
            h2 = bool(witness.I_is_proper_ideal())
        elif hasattr(witness, 'H2'):
            h2 = bool(witness.H2)
        elif I is not None:
            is_ideal = True
            if hasattr(I, 'is_ideal'):
                is_ideal = bool(I.is_ideal(R) if callable(I.is_ideal) else I.is_ideal)
            
            if is_ideal:
                if hasattr(I, 'is_proper'):
                    h2 = bool(I.is_proper() if callable(I.is_proper) else I.is_proper)
                elif hasattr(I, 'is_proper_ideal'):
                    h2 = bool(I.is_proper_ideal(R) if callable(I.is_proper_ideal) else I.is_proper_ideal)
                elif hasattr(R, 'one') and hasattr(I, 'contains'):
                    h2 = not bool(I.contains(R.one))
    except Exception:
        h2 = False

    # H_3: n is a positive integer
    h3 = False
    try:
        if isinstance(witness, dict) and 'H3' in witness:
            h3 = bool(witness['H3'])
        elif hasattr(witness, 'n_is_positive_integer'):
            h3 = bool(witness.n_is_positive_integer())
        elif hasattr(witness, 'H3'):
            h3 = bool(witness.H3)
        elif n is not None:
            if hasattr(n, 'is_integer') and n.is_integer is not None:
                h3 = bool(n.is_integer and n > 0)
            else:
                h3 = bool(int(n) == n and n > 0)
    except Exception:
        h3 = False

    # ¬Q: I^n is not a proper ideal of R
    neg_q = False
    try:
        if isinstance(witness, dict) and 'neg_Q' in witness:
            neg_q = bool(witness['neg_Q'])
        elif isinstance(witness, dict) and 'Q' in witness:
            neg_q = not bool(witness['Q'])
        elif hasattr(witness, 'In_is_proper_ideal'):
            neg_q = not bool(witness.In_is_proper_ideal())
        elif hasattr(witness, 'neg_Q'):
            neg_q = bool(witness.neg_Q)
        elif hasattr(witness, 'Q'):
            neg_q = not bool(witness.Q)
        elif I is not None and n is not None:
            In = I**n
            is_ideal = True
            if hasattr(In, 'is_ideal'):
                is_ideal = bool(In.is_ideal(R) if callable(In.is_ideal) else In.is_ideal)
            
            if not is_ideal:
                neg_q = True
            else:
                if hasattr(In, 'is_proper'):
                    neg_q = not bool(In.is_proper() if callable(In.is_proper) else In.is_proper)
                elif hasattr(In, 'is_proper_ideal'):
                    neg_q = not bool(In.is_proper_ideal(R) if callable(In.is_proper_ideal) else In.is_proper_ideal)
                elif hasattr(R, 'one') and hasattr(In, 'contains'):
                    neg_q = bool(In.contains(R.one))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R has an identity element 1 \\neq 0",
    "H_2: I is a proper ideal of R",
    "H_3: n is a positive integer",
    "¬Q: I^n is not a proper ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3