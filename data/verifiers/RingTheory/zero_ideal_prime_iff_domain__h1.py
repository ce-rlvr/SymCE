import sympy
from sympy import Rational, Integer

class RingInfo:
    def __init__(self, name, has_identity, is_integral_domain, zero_is_prime_ideal):
        self.name = name
        self.has_identity = has_identity
        self.is_integral_domain = is_integral_domain
        self.zero_is_prime_ideal = zero_is_prime_ideal
        
    def __str__(self):
        return self.name

Z = RingInfo("Z", True, True, True)
Q = RingInfo("Q", True, True, True)
Z6 = RingInfo("Z6", True, False, False)
M2R = RingInfo("M2R", True, False, True)
M2Z = RingInfo("M2Z", True, False, True)
Z2 = RingInfo("Z2", True, True, True)
Z4 = RingInfo("Z4", True, False, False)

def conditions(witness):
    try:
        if isinstance(witness, RingInfo):
            h1 = witness.has_identity
            is_dom = witness.is_integral_domain
            zero_prime = witness.zero_is_prime_ideal
        elif isinstance(witness, str):
            w = witness.upper().replace(" ", "")
            if w in ["M2R", "M2Z", "M2(R)", "M2(Z)", "M_2(R)", "M_2(Z)"]:
                h1 = True
                is_dom = False
                zero_prime = True
            elif w in ["Z", "Q", "R", "C", "ZZ", "QQ"]:
                h1 = True
                is_dom = True
                zero_prime = True
            elif w in ["Z6", "Z/6Z", "Z_6", "Z4", "Z/4Z", "Z_4"]:
                h1 = True
                is_dom = False
                zero_prime = False
            else:
                return [False, False]
        elif witness in [sympy.ZZ, sympy.QQ]:
            h1 = True
            is_dom = True
            zero_prime = True
        else:
            return [False, False]
            
        neg_q = not (is_dom == zero_prime)
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R has a multiplicative identity 1 != 0",
    "¬Q: Equivalence between R being an integral domain and {0} being a prime ideal fails"
]

N_HYP = 1
NEG_Q_INDEX = 1