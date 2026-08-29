import sympy
import math

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let R be a commutative ring with 1 != 0. Let n be a positive integer.
    Then I^n is a proper ideal of R."
    
    The dropped hypothesis was "I is a proper ideal of R".
    A valid witness should provide a ring R, an ideal I (via generators), and n,
    such that I is NOT proper (e.g., I = R), making I^n = R not proper.
    
    Expected witness formats:
      - (R, I_gens, n)
      - (I_gens, n)  -- assumes R = ZZ
    where R is ZZ, QQ, an integer m (for Z_m), or a string like 'Z_m'.
    I_gens is a list of integers generating the ideal.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                I_gens, n = witness
                R = ZZ
            elif len(witness) == 3:
                R, I_gens, n = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        if isinstance(I_gens, (int, sympy.Integer)):
            I_gens = [I_gens]
            
        if not isinstance(I_gens, (list, tuple)):
            return [False, False, False, False]
            
    except Exception:
        return [False, False, False, False]

    h1 = False
    h2 = False
    h3 = False
    neg_q = False

    try:
        h3 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        pass

    try:
        is_proper = True
        
        if isinstance(R, (int, sympy.Integer)):
            m = int(R)
            h1 = True
            h2 = (m != 1)
            g = 0
            for x in I_gens:
                g = math.gcd(g, int(x))
            if m > 0:
                is_proper = (math.gcd(g, m) != 1)
            else:
                is_proper = (abs(g) != 1)
                
        elif R in (ZZ, 'Z', 'ZZ'):
            h1 = True
            h2 = True
            g = 0
            for x in I_gens:
                g = math.gcd(g, int(x))
            is_proper = (abs(g) != 1)
            
        elif R in (QQ, 'Q', 'QQ'):
            h1 = True
            h2 = True
            g = 0
            for x in I_gens:
                if x != 0:
                    g = 1
            is_proper = (g == 0)
            
        elif isinstance(R, str) and R.startswith('Z_'):
            m = int(R[2:])
            h1 = True
            h2 = (m != 1)
            g = 0
            for x in I_gens:
                g = math.gcd(g, int(x))
            if m > 0:
                is_proper = (math.gcd(g, m) != 1)
            else:
                is_proper = (abs(g) != 1)
        else:
            # Unrecognized ring format
            pass
            
        neg_q = not is_proper
            
    except Exception:
        pass

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R has an identity element 1 != 0",
    "H_3: n is a positive integer",
    "¬Q: I^n is not a proper ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3