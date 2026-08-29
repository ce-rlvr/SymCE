import sympy
from sympy.ntheory import isprime, factorint

# Top-level setup for Field Theory / Ring Theory
x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Expects witness to be a tuple (p, k, n) or (p, n) where:
      - p is the prime characteristic of F
      - k is the degree of F over GF(p) (default 1)
      - n is the degree of the extension E over F
    Alternatively, a dictionary with keys 'p', 'k', 'n' or 'q', 'n'.
    """
    try:
        if isinstance(witness, dict):
            if 'q' in witness and 'p' not in witness:
                q = int(witness['q'])
                factors = factorint(q)
                if len(factors) == 1:
                    p, k = list(factors.items())[0]
                else:
                    p, k = 0, 0
            else:
                p = int(witness.get('p', 0))
                k = int(witness.get('k', 1))
            n = int(witness.get('n', 0))
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                p, k, n = witness
            elif len(witness) == 2:
                p, n = witness
                k = 1
            else:
                return [False, False, False]
            p = int(p)
            k = int(k)
            n = int(n)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: F is a finite field of characteristic p with q elements
    try:
        h1 = isprime(p) and k >= 1
    except Exception:
        h1 = False

    # H_2: E is a finite extension of F of degree n
    try:
        h2 = n >= 1
    except Exception:
        h2 = False

    # ¬Q: There does NOT exist a self-dual basis of E over F.
    # By a known theorem, a finite extension E/F of finite fields has a self-dual basis
    # if and only if the characteristic p is 2 or the degree n is odd.
    # Therefore, a self-dual basis does NOT exist iff p != 2 and n is even.
    try:
        neg_q = (p != 2) and (n % 2 == 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a finite field of characteristic p with q elements",
    "H_2: E is a finite extension of F of degree n",
    "¬Q: There does not exist a self-dual basis of E over F"
]

N_HYP = 2
NEG_Q_INDEX = 2