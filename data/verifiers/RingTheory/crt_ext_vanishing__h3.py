import math
import sympy
from sympy import S

# Top-level setup
Z = S.Integers
ZZ = S.Integers

def parse_ideal(I):
    """
    Parses an ideal representation into a single integer generator for Z.
    """
    if isinstance(I, (list, tuple, set)):
        if len(I) == 0:
            return 0
        g = 0
        for x in I:
            g = math.gcd(g, parse_ideal(x))
        return g
    if isinstance(I, int):
        return abs(I)
    if hasattr(I, 'is_integer') and I.is_integer:
        return abs(int(I))
    
    s = str(I).replace(' ', '')
    if '/' in s or '.' in s:
        raise ValueError("Fractions not allowed")
        
    if s in ('ZZ', 'Z', 'Integers', 'S.Integers'):
        return 1
    if s == '0':
        return 0
        
    digits = []
    for char in s:
        if char.isdigit():
            digits.append(char)
        elif digits:
            break
    if digits:
        return int("".join(digits))
        
    raise ValueError(f"Cannot parse ideal {I}")

def parse_witness(witness):
    """
    Extracts m, k, n from the witness, assuming R = Z, I = mZ, J = kZ.
    """
    def get_n(val):
        if isinstance(val, int):
            return val
        if hasattr(val, 'is_integer') and val.is_integer:
            return int(val)
        if isinstance(val, float) and val.is_integer():
            return int(val)
        if isinstance(val, str) and val.isdigit():
            return int(val)
        raise ValueError("n must be an integer")

    if isinstance(witness, dict):
        if 'I' in witness and 'J' in witness and 'n' in witness:
            return parse_ideal(witness['I']), parse_ideal(witness['J']), get_n(witness['n'])
        if 'm' in witness and 'k' in witness and 'n' in witness:
            return parse_ideal(witness['m']), parse_ideal(witness['k']), get_n(witness['n'])
    elif isinstance(witness, (list, tuple)):
        if len(witness) == 3:
            return parse_ideal(witness[0]), parse_ideal(witness[1]), get_n(witness[2])
        elif len(witness) == 4:
            return parse_ideal(witness[1]), parse_ideal(witness[2]), get_n(witness[3])
    raise ValueError("Cannot parse witness")

def ext_Z_is_trivial(m, k, n):
    """
    Returns True if Ext^n_Z(Z/mZ, Z/kZ) is the trivial group, False otherwise.
    """
    m = abs(m)
    k = abs(k)
    if n == 0:
        if m == 0:
            return k == 1
        elif k == 0:
            return True
        else:
            return math.gcd(m, k) == 1
    elif n == 1:
        if m == 0:
            return True
        elif k == 0:
            return m == 1
        else:
            return math.gcd(m, k) == 1
    else:
        return True

def conditions(witness):
    try:
        m, k, n = parse_witness(witness)
    except Exception:
        return [False, False, False, False]
    
    # H_1: R is a commutative ring
    # We interpret the witness as ideals in Z, which is a commutative ring.
    h1 = True
    
    # H_2: I and J are ideals of R
    # mZ and kZ are always ideals in Z.
    h2 = True
    
    # H_3: n >= 0 is an integer
    try:
        h3 = isinstance(n, int) and n >= 0
    except Exception:
        h3 = False
        
    # neg_Q: Ext^n_R(R/I, R/J) is not the trivial group
    try:
        neg_q = not ext_Z_is_trivial(m, k, n)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are ideals of R",
    "H_3: n >= 0 is an integer",
    "¬Q: Ext^n_R(R/I, R/J) is not the trivial group"
]

N_HYP = 3
NEG_Q_INDEX = 3