import sympy
from sympy.ntheory import factorint

# Top-level setup
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z10 = 10
Z12 = 12
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    try:
        # Heuristics to extract integer n for Z/nZ
        if isinstance(witness, str):
            s = witness.replace(" ", "").lower()
            if s.startswith("z/") and s.endswith("z"):
                s = s[2:-1]
            elif s.startswith("z"):
                s = s[1:]
            if s.isdigit():
                witness = int(s)
        elif isinstance(witness, tuple):
            for item in witness:
                if isinstance(item, (int, sympy.Integer)):
                    witness = int(item)
                    break

        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n < 2:
                return [False, False]
            
            # H_1: R is a commutative ring
            # Z/nZ is always a commutative ring for n >= 2.
            h1 = True
            
            # neg_Q: The nilradical of R is not a prime ideal
            # In Z/nZ, the nilradical is prime iff n has exactly one prime factor.
            factors = factorint(n)
            neg_q = len(factors) > 1
            
            return [h1, neg_q]
        
        return [False, False]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The nilradical of R is not a prime ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1