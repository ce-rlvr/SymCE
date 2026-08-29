import math
import sympy
import sympy.combinatorics.named_groups as named_groups
import sympy.matrices

# Top-level setup
S3 = named_groups.SymmetricGroup(3)
S4 = named_groups.SymmetricGroup(4)
A4 = named_groups.AlternatingGroup(4)
D4 = named_groups.DihedralGroup(4)
C4 = named_groups.CyclicGroup(4)
V4 = named_groups.AlternatingGroup(4)
Z2 = named_groups.CyclicGroup(2)
Z3 = named_groups.CyclicGroup(3)
Z4 = named_groups.CyclicGroup(4)
Z6 = named_groups.CyclicGroup(6)
trivial = named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide the base p and the first coefficient a_0.
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            if 'a0' in witness:
                a0 = witness['a0']
            elif 'a' in witness:
                a0 = witness['a'][0]
            elif 'x' in witness:
                a0 = witness['x']
            else:
                return [False, False, False]
        elif isinstance(witness, tuple) and len(witness) == 2:
            p, a = witness
            if isinstance(a, (list, tuple)):
                a0 = a[0]
            else:
                a0 = a
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        p_val = int(p)
        h1 = (p_val >= 2)
    except Exception:
        h1 = False

    try:
        a0_val = int(a0)
        p_val = int(p)
        h2 = (0 <= a0_val < p_val)
    except Exception:
        h2 = False

    try:
        a0_val = int(a0)
        p_val = int(p)
        # In the ring of p-adic integers (or g-adic integers if p is not prime),
        # an element is a unit if and only if its lowest order term is coprime to p.
        is_unit = (math.gcd(a0_val, p_val) == 1)
        a0_not_zero = (a0_val != 0)
        
        # The conclusion states: x is a unit iff a_0 != 0.
        # We want the negation of this conclusion.
        neg_q = (is_unit != a0_not_zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an integer >= 2 (Z_p is a ring)",
    "H_2: a_0 is an integer with 0 <= a_0 < p",
    "¬Q: x being a unit is NOT equivalent to a_0 != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2