import math
import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2,2)
O3 = zeros(3,3)
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to define two rings R1, R2 and four ideals I1, J1, I2, J2.
    We represent rings Z/nZ by the integer n (with n=0 for Z), and ideals by their integer generators.
    Expected witness format: dict with keys 'R1', 'R2', 'I1', 'J1', 'I2', 'J2' 
    or a flat tuple (n1, n2, a1, b1, a2, b2).
    """
    try:
        if isinstance(witness, dict):
            w_n1 = witness.get('n1', witness.get('R1'))
            w_n2 = witness.get('n2', witness.get('R2'))
            w_a1 = witness.get('a1', witness.get('I1'))
            w_b1 = witness.get('b1', witness.get('J1'))
            w_a2 = witness.get('a2', witness.get('I2'))
            w_b2 = witness.get('b2', witness.get('J2'))
        else:
            flat = []
            def flatten(w):
                if isinstance(w, (list, tuple)):
                    for x in w:
                        flatten(x)
                else:
                    flat.append(w)
            flatten(witness)
            w_n1, w_n2, w_a1, w_b1, w_a2, w_b2 = flat[:6]

        def parse_ring(r):
            if str(r) == 'ZZ':
                return 0
            return int(r)

        def parse_ideal(i):
            try:
                return int(i)
            except TypeError:
                if hasattr(i, 'gen'):
                    return int(i.gen)
                if hasattr(i, 'args') and len(i.args) == 1:
                    return int(i.args[0])
                raise

        n1 = parse_ring(w_n1)
        n2 = parse_ring(w_n2)
        a1 = parse_ideal(w_a1)
        b1 = parse_ideal(w_b1)
        a2 = parse_ideal(w_a2)
        b2 = parse_ideal(w_b2)

        # H_1: R1 and R2 are rings
        # Any integer >= 0 represents a valid ring Z/nZ
        h1 = n1 >= 0 and n2 >= 0

        def ideal_sum_is_ring(a, b, n):
            # In Z/nZ, the sum of ideals <a> and <b> is <gcd(a, b, n)>
            # It equals the whole ring iff gcd(a, b, n) == 1
            g = math.gcd(a, b)
            if n != 0:
                g = math.gcd(g, n)
            return g == 1

        # H_2: I2 and J2 are ideals of R2 such that I2 + J2 = R2
        h2 = ideal_sum_is_ring(a2, b2, n2)

        # ¬Q: The product ideals I1 x I2 and J1 x J2 are NOT comaximal in R1 x R2
        # They are comaximal iff I1 + J1 = R1 AND I2 + J2 = R2.
        comaximal_1 = ideal_sum_is_ring(a1, b1, n1)
        comaximal_2 = ideal_sum_is_ring(a2, b2, n2)
        
        neg_q = not (comaximal_1 and comaximal_2)

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R1 and R2 are rings",
    "H_2: I2 and J2 are ideals of R2 such that I2 + J2 = R2",
    "¬Q: I1 x I2 and J1 x J2 are not comaximal in R1 x R2"
]

N_HYP = 2
NEG_Q_INDEX = 2