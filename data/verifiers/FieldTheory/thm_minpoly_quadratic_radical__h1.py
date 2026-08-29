import sympy
from sympy import Symbol, minpoly, expand, QQ, ZZ, GF
from sympy.matrices import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: The characteristic of F is not equal to 2",
    "H_2: \\alpha \\in K",
    "H_3: \\alpha \\notin F",
    "H_4: \\alpha^2 \\in F",
    "¬Q: The minimal polynomial of \\alpha over F is not x^2 - \\alpha^2"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    # Support dictionary witnesses for maximum flexibility
    if isinstance(witness, dict):
        class Dummy: pass
        w = Dummy()
        w.__dict__.update(witness)
        witness = w

    F = None
    alpha = None
    if isinstance(witness, tuple) and len(witness) == 2:
        F, alpha = witness
    else:
        try:
            F = witness.F
            alpha = witness.alpha
        except AttributeError:
            pass

    # H1: The characteristic of F is not equal to 2
    h1 = False
    try:
        if hasattr(witness, 'h1'):
            h1 = bool(witness.h1)
        elif F is not None:
            if hasattr(F, 'characteristic'):
                char = F.characteristic
                if callable(char): char = char()
                h1 = char != 2
            elif hasattr(F, 'char'):
                char = F.char
                if callable(char): char = char()
                h1 = char != 2
    except Exception:
        h1 = False

    # H2: \alpha \in K
    h2 = False
    try:
        if hasattr(witness, 'h2'):
            h2 = bool(witness.h2)
        else:
            # If alpha is provided, it exists in some extension field K
            h2 = True
    except Exception:
        h2 = False

    # H3: \alpha \notin F
    h3 = False
    try:
        if hasattr(witness, 'h3'):
            h3 = bool(witness.h3)
        elif F is not None and alpha is not None:
            h3 = alpha not in F
    except Exception:
        h3 = False

    # H4: \alpha^2 \in F
    h4 = False
    try:
        if hasattr(witness, 'h4'):
            h4 = bool(witness.h4)
        elif F is not None and alpha is not None:
            h4 = expand(alpha**2) in F
    except Exception:
        h4 = False

    # ¬Q: The minimal polynomial of \alpha over F is not x^2 - \alpha^2
    neg_q = False
    try:
        if hasattr(witness, 'neg_q'):
            neg_q = bool(witness.neg_q)
        elif F is not None and alpha is not None:
            x = Symbol('x')
            mp = minpoly(alpha, x, domain=F)
            expected = x**2 - alpha**2
            neg_q = (mp - expected).simplify() != 0
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]