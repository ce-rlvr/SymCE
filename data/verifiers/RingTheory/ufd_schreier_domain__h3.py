import sympy
from sympy import divisors

# Top-level setup
ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

def conditions(witness) -> list[bool]:
    try:
        # Parse witness
        if isinstance(witness, tuple):
            if len(witness) == 4:
                R, a, b, c = witness
                R_str = str(R)
                # We restrict verification to the ring of integers for simplicity and robustness
                if not any(valid in R_str for valid in ['ZZ', 'Integer', 'Z']):
                    return [False, False, False]
            elif len(witness) == 3:
                a, b, c = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        c = sympy.sympify(c)
        
        # H_1: R is a unique factorization domain
        # We verify this by checking if the elements belong to ZZ, which is a known UFD.
        try:
            h1 = isinstance(a, (int, sympy.Integer)) and \
                 isinstance(b, (int, sympy.Integer)) and \
                 isinstance(c, (int, sympy.Integer))
        except Exception:
            h1 = False
            
        # H_2: a, b, c are non-zero elements of R
        try:
            h2 = bool(a != 0 and b != 0 and c != 0)
        except Exception:
            h2 = False
            
        # ¬Q: There do NOT exist a_1, a_2 in R such that a = a_1 a_2, a_1 | b, and a_2 | c
        neg_q = True
        if h1 and h2:
            try:
                # Iterate over all possible divisors of a in ZZ
                for a1 in divisors(abs(a)):
                    for sign in (1, -1):
                        a1_signed = a1 * sign
                        if a % a1_signed != 0:
                            continue
                        a2_signed = a // a1_signed
                        
                        # Check if a1 divides b and a2 divides c
                        if b % a1_signed == 0 and c % a2_signed == 0:
                            neg_q = False
                            break
                    if not neg_q:
                        break
            except Exception:
                neg_q = False
        else:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a, b, c are non-zero elements of R",
    "¬Q: There do not exist a_1, a_2 in R such that a = a_1 a_2, a_1 | b, and a_2 | c"
]

N_HYP = 2
NEG_Q_INDEX = 2