import sympy
from sympy import Symbol, Poly, Rational, roots
from sympy.polys.domains import QQ, GF
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

CONDITION_LABELS = [
    "H_1: a is an element of F",
    "H_2: There does not exist any element c in F such that c^p - c = a",
    "¬Q: The polynomial x^p - x - a is reducible over F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks the witness against the hypotheses and negated conclusion.
    The witness can be provided as:
      - A tuple (p, a) implying F = QQ
      - A tuple (q, p, a) implying F = GF(q)
      - A dictionary or object with attributes 'p', 'a', and optionally 'q'
    """
    try:
        if isinstance(witness, dict):
            p = witness['p']
            a = witness['a']
            q = witness.get('q', 0)
        elif hasattr(witness, 'p') and hasattr(witness, 'a'):
            p = witness.p
            a = witness.a
            q = getattr(witness, 'q', 0)
        elif len(witness) == 2:
            p, a = witness
            q = 0
        elif len(witness) == 3:
            q, p, a = witness
        else:
            return [False, False, False]
            
        p = int(p)
        if p < 2:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: a is an element of F
    try:
        if q == 0:
            a_val = Rational(a)
            h1 = True
        else:
            if not sympy.isprime(q):
                return [False, False, False]
            a_val = int(a) % q
            h1 = True
    except Exception:
        h1 = False

    # H2: There does not exist any element c in F such that c^p - c = a
    try:
        h2 = True
        if q == 0:
            x = Symbol('x')
            poly_c = x**p - x - a_val
            rts = roots(poly_c, x, domain='QQ')
            if len(rts) > 0:
                h2 = False
        else:
            for c in range(q):
                if (pow(c, p, q) - c) % q == a_val:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # neg_Q: The polynomial x^p - x - a is reducible over F
    try:
        x = Symbol('x')
        if q == 0:
            poly_q = Poly(x**p - x - a_val, x, domain='QQ')
        else:
            poly_q = Poly(x**p - x - a_val, x, domain=GF(q))
        
        neg_q = not poly_q.is_irreducible
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]