import sympy
from sympy import gcd, ZZ, QQ, RR, CC
from sympy.polys.domains import Domain
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness) -> list[bool]:
    # Parse witness
    R, x = None, None
    try:
        if isinstance(witness, dict):
            R = witness.get('R', witness.get('ring'))
            x = witness.get('x', witness.get('element'))
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, x = witness
        elif hasattr(witness, 'R') and hasattr(witness, 'x'):
            R, x = witness.R, witness.x
        elif hasattr(witness, 'ring') and hasattr(witness, 'element'):
            R, x = witness.ring, witness.element
        else:
            R, x = witness, None
    except Exception:
        pass

    # H1: R is a commutative ring
    h1 = False
    try:
        if isinstance(R, int):
            h1 = True
        elif isinstance(R, Domain):
            h1 = True # Sympy domains are commutative
        elif hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
    except Exception:
        pass

    # H2: R has a multiplicative identity
    h2 = False
    try:
        if isinstance(R, int):
            h2 = True
        elif isinstance(R, Domain):
            h2 = R.has_one
        elif hasattr(R, 'has_one'):
            h2 = bool(R.has_one)
    except Exception:
        pass

    # H3: R is an Artinian ring
    h3 = False
    try:
        if isinstance(R, int):
            h3 = (R != 0) # Z/nZ is finite for n!=0, hence Artinian. Z/0Z is Z, not Artinian.
        elif isinstance(R, Domain):
            if R.is_Field:
                h3 = True
            elif type(R).__name__ == 'QuotientRing':
                h3 = True
            else:
                h3 = False
        elif hasattr(R, 'is_artinian'):
            h3 = bool(R.is_artinian)
    except Exception:
        pass

    # neg_Q: x is neither a unit nor a zero divisor
    neg_q = False
    try:
        if x is not None:
            if isinstance(R, int):
                if R == 1:
                    is_u = True
                    is_zd = False
                elif R == 0:
                    is_u = (x in [1, -1])
                    is_zd = False
                else:
                    x_mod = x % R
                    is_u = (gcd(x_mod, R) == 1)
                    if x_mod == 0:
                        is_zd = False
                    else:
                        is_zd = (gcd(x_mod, R) > 1)
                neg_q = not is_u and not is_zd
            else:
                if hasattr(R, 'zero'):
                    zero = R.zero
                else:
                    zero = 0
                
                if hasattr(R, 'is_unit'):
                    is_u = R.is_unit(x)
                elif hasattr(R, 'is_Field') and R.is_Field:
                    is_u = (x != zero)
                else:
                    is_u = False
                
                if x == zero:
                    is_zd = False
                else:
                    if hasattr(R, 'is_zero_divisor'):
                        is_zd = R.is_zero_divisor(x)
                    elif R == sympy.S.Integers or type(R).__name__ == 'IntegerRing':
                        is_zd = False
                    else:
                        # In an Artinian ring, non-zero non-units are zero divisors
                        is_zd = not is_u
                
                neg_q = not is_u and not is_zd
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R has a multiplicative identity",
    "H_3: R is an Artinian ring",
    "¬Q: x is neither a unit nor a zero divisor"
]

N_HYP = 3
NEG_Q_INDEX = 3