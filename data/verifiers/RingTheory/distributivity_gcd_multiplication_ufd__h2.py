import sympy
from sympy import Rational, Integer, Symbol
from sympy.abc import x, y, z

# Define common rings that might be referenced in the witness
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should provide the ring R and elements a, b, c, d.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R', ZZ)
            a = witness['a']
            b = witness['b']
            c = witness['c']
            d = witness['d']
        elif len(witness) == 5:
            R, a, b, c, d = witness
        elif len(witness) == 4:
            R = ZZ
            a, b, c, d = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a unique factorization domain
    try:
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False

    def is_zero(val):
        if val == 0:
            return True
        if hasattr(R, 'zero') and val == R.zero:
            return True
        return False

    def divides(div, val):
        if is_zero(div):
            return is_zero(val)
        if hasattr(R, 'exquo'):
            try:
                R.exquo(val, div)
                return True
            except Exception:
                return False
        else:
            try:
                return (val % div) == 0
            except Exception:
                return False

    def is_gcd(g, val1, val2):
        # In many abstract algebra contexts, gcd(0,0) is undefined.
        # If the conjecture is false because c=0 leads to ca=0 and cb=0,
        # then cd is not a gcd because gcd(0,0) doesn't exist.
        if is_zero(val1) and is_zero(val2):
            return False
            
        if not (divides(g, val1) and divides(g, val2)):
            return False
            
        try:
            # R.gcd gives a valid greatest common divisor in a UFD
            true_g = R.gcd(val1, val2)
            # g is a greatest common divisor iff it is an associate of true_g
            return divides(true_g, g)
        except Exception:
            return False

    # H_2: d is a greatest common divisor of a and b
    try:
        h2 = is_gcd(d, a, b)
    except Exception:
        h2 = False

    # ¬Q: The product cd is NOT a greatest common divisor of ca and cb
    try:
        # Attempt to multiply within the domain R
        if hasattr(R, 'mul'):
            try:
                ca = R.mul(c, a)
                cb = R.mul(c, b)
                cd = R.mul(c, d)
            except Exception:
                # Fallback if c is outside the domain (e.g., a fraction or symbol)
                ca = c * a
                cb = c * b
                cd = c * d
        else:
            ca = c * a
            cb = c * b
            cd = c * d
            
        # If ca, cb, cd are outside R, is_gcd will correctly return False
        neg_q = not is_gcd(cd, ca, cb)
    except Exception:
        # If multiplication or gcd check fails entirely, cd is not a valid gcd
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: d is a greatest common divisor of a and b",
    "¬Q: The product cd is not a greatest common divisor of ca and cb"
]

N_HYP = 2
NEG_Q_INDEX = 2