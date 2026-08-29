import sympy
from sympy import ZZ, QQ, RR, CC, eye, zeros
from sympy.polys.domains import Domain

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 1",
    "H_2: GL_n(F) is the general linear group of degree n over F",
    "¬Q: The center Z(GL_n(F)) is not the set of all matrices cI for non-zero c in F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        n, F = witness
    except Exception:
        return [False, False, False]
        
    # H_1: n is an integer such that n >= 1
    try:
        h1 = isinstance(n, int) and n >= 1
    except Exception:
        h1 = False
        
    # H_2: GL_n(F) is the general linear group of degree n over F
    # We verify that F is a valid algebraic domain over which GL_n can be defined.
    try:
        h2 = isinstance(F, Domain) or hasattr(F, 'is_Field')
    except Exception:
        h2 = False
        
    # ¬Q: The conclusion states that Z(GL_n(F)) = {cI | c in F, c != 0}.
    # For a commutative ring F, the center of GL_n(F) consists of scalar matrices cI 
    # where c is a unit in F. The set of all non-zero elements is equal to the set 
    # of units if and only if F is a field.
    # Therefore, the conclusion fails (¬Q is True) if and only if F is NOT a field.
    try:
        if hasattr(F, 'is_Field'):
            neg_q = not F.is_Field
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]