import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
import math

# Top-level setup
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to represent ideals in the ring of integers Z.
    Format: (q, p, x) or (R, q, p, x) or a dict with keys 'q', 'p', 'x'.
    q generates the ideal Q, p generates the prime ideal P, and x is the element.
    """
    try:
        if isinstance(witness, dict):
            q = witness.get('Q', witness.get('q'))
            p = witness.get('P', witness.get('p'))
            x = witness.get('x')
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                q, p, x = witness
            elif len(witness) == 4:
                _, q, p, x = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]

        def extract_int(v):
            if hasattr(v, 'gens'):
                gens = v.gens
                if len(gens) == 1:
                    v = gens[0]
                else:
                    raise ValueError
            if isinstance(v, (list, tuple, set)):
                if len(v) == 1:
                    v = list(v)[0]
                else:
                    raise ValueError
            return int(v)

        q = extract_int(q)
        p = extract_int(p)
        x = extract_int(x)
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring with identity
    # We evaluate the witness in the context of R = Z, which is a commutative ring with identity.
    h1 = True

    # H_2: Q is a P-primary ideal of R
    def is_p_primary(ideal_gen, prime_gen):
        ig = abs(ideal_gen)
        pg = abs(prime_gen)
        if ig == 1:
            return False
        if ig == 0:
            return pg == 0
        factors = factorint(ig)
        if len(factors) != 1:
            return False
        prime = list(factors.keys())[0]
        return prime == pg

    try:
        h2 = is_p_primary(q, p)
    except Exception:
        h2 = False

    # neg_Q: The ideal quotient (Q : x) is NOT a P-primary ideal
    try:
        if q == 0 and x == 0:
            q_quot = 1
        elif q == 0:
            q_quot = 0
        else:
            q_quot = q // math.gcd(q, x)
        
        neg_q = not is_p_primary(q_quot, p)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: Q is a P-primary ideal of R",
    "¬Q: The ideal quotient (Q : x) is NOT a P-primary ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2