import math
import sympy
from sympy.ntheory import factorint

# Top-level setup
class Z_Ring_Class:
    def __str__(self): return "Z"
    def __repr__(self): return "Z"
    
    def __mul__(self, other):
        if isinstance(other, int) or (hasattr(other, 'is_Integer') and other.is_Integer):
            return abs(int(other))
        if isinstance(other, Z_Ring_Class):
            return self
        return NotImplemented
        
    def __rmul__(self, other):
        return self.__mul__(other)
        
    def __truediv__(self, other):
        if isinstance(other, int) or (hasattr(other, 'is_Integer') and other.is_Integer):
            return [abs(int(other))]
        if isinstance(other, list):
            return other
        return NotImplemented
        
    def __pow__(self, other):
        if isinstance(other, int) and other > 0:
            return [0] * other
        return NotImplemented

Z = Z_Ring_Class()
ZZ = Z

def safe_lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def parse_witness(witness):
    if isinstance(witness, dict):
        if not all(k in witness for k in ("R", "M", "I", "J")):
            raise ValueError("Missing keys in dict witness")
        return witness["R"], witness["M"], witness["I"], witness["J"]
    elif isinstance(witness, (tuple, list)) and len(witness) == 4:
        return witness[0], witness[1], witness[2], witness[3]
    else:
        raise ValueError("Witness must be a 4-tuple (R, M, I, J) or a dict")

def parse_module(M):
    if isinstance(M, Z_Ring_Class) or M == sympy.S.Integers or M == "Z":
        return [0]
    if isinstance(M, int) or (hasattr(M, 'is_Integer') and M.is_Integer):
        return [abs(int(M))]
    if isinstance(M, list):
        return [abs(int(x)) for x in M]
    if isinstance(M, tuple):
        return [abs(int(x)) for x in M]
    raise ValueError("Unsupported module format")

def parse_ideal(I):
    if isinstance(I, int) or (hasattr(I, 'is_Integer') and I.is_Integer):
        return abs(int(I))
    if isinstance(I, tuple) and len(I) == 1:
        return parse_ideal(I[0])
    if isinstance(I, list) and len(I) == 1:
        return parse_ideal(I[0])
    if isinstance(I, Z_Ring_Class) or I == sympy.S.Integers or I == "Z":
        return 1
    raise ValueError("Unsupported ideal format")

def elementary_divisors(inv_factors):
    divs = []
    for d in inv_factors:
        if d == 0:
            divs.append(0)
        elif d == 1 or d == -1:
            continue
        else:
            factors = factorint(abs(d))
            for p, e in factors.items():
                divs.append(p**e)
    return sorted(divs)

def conditions(witness) -> list[bool]:
    try:
        R, M, I, J = parse_witness(witness)
    except Exception:
        return [False, False, False, False]
    
    # H1: R is a commutative ring with identity
    try:
        h1 = bool(isinstance(R, Z_Ring_Class) or R == sympy.S.Integers or R == "Z")
    except Exception:
        h1 = False
        
    # H2: M is an R-module
    try:
        parsed_M = parse_module(M)
        h2 = isinstance(parsed_M, list)
    except Exception:
        h2 = False
        
    # H3: I and J are ideals of R
    try:
        parse_ideal(I)
        parse_ideal(J)
        h3 = True
    except Exception:
        h3 = False
        
    # neg_Q: M/((I \cap J)M) is not isomorphic to M/IM \times M/JM
    try:
        M_parsed = parse_module(M)
        I_parsed = parse_ideal(I)
        J_parsed = parse_ideal(J)
        
        I_cap_J = safe_lcm(I_parsed, J_parsed)
        
        M_cap = [math.gcd(d, I_cap_J) for d in M_parsed]
        M_I = [math.gcd(d, I_parsed) for d in M_parsed]
        M_J = [math.gcd(d, J_parsed) for d in M_parsed]
        
        ed_cap = elementary_divisors(M_cap)
        ed_prod = elementary_divisors(M_I + M_J)
        
        neg_q = bool(ed_cap != ed_prod)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: M is an R-module",
    "H_3: I and J are ideals of R",
    "¬Q: M/((I \\cap J)M) is not isomorphic to M/IM \\times M/JM"
]

N_HYP = 3
NEG_Q_INDEX = 3