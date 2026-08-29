import math
import sympy
from sympy.combinatorics.named_groups import CyclicGroup, SymmetricGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z

# Top-level setup
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
V4 = AlternatingGroup(4)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            i = witness.get('I', witness.get('i', witness.get('I_gen')))
            j = witness.get('J', witness.get('j', witness.get('J_gen')))
            p = witness.get('P', witness.get('p', witness.get('P_gen')))
            if i is None or j is None or p is None:
                vals = list(witness.values())
                if len(vals) == 3:
                    i, j, p = vals
                elif len(vals) == 4:
                    _, i, j, p = vals
                else:
                    return [False] * 4
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                i, j, p = witness
            elif len(witness) == 4:
                _, i, j, p = witness
            else:
                return [False] * 4
        else:
            return [False] * 4
            
        def extract_int(val):
            if isinstance(val, int):
                return val
            if hasattr(val, 'is_Integer') and val.is_Integer:
                return int(val)
            if isinstance(val, sympy.Expr):
                coeffs = [arg for arg in val.args if isinstance(arg, sympy.Integer)]
                if coeffs:
                    return int(coeffs[0])
            return int(val)

        i = extract_int(i)
        j = extract_int(j)
        p = extract_int(p)
    except Exception:
        return [False] * 4

    # H1: R is a commutative ring
    # The witness is evaluated in the ring of integers Z, which is a commutative ring.
    h1 = True

    # H2: I and J are comaximal ideals of R
    # In Z, ideals iZ and jZ are comaximal iff gcd(i, j) == 1
    try:
        h2 = (math.gcd(i, j) == 1)
    except Exception:
        h2 = False

    # H3: I \cap J \subseteq P
    # In Z, iZ \cap jZ = lcm(i, j)Z. lcm(i, j)Z \subseteq pZ iff p divides lcm(i, j)
    try:
        if i == 0 and j == 0:
            l = 0
        else:
            l = abs(i * j) // math.gcd(i, j)
            
        if p == 0:
            h3 = (l == 0)
        else:
            h3 = (l % p == 0)
    except Exception:
        h3 = False

    # neg_Q: NOT (Either I \subseteq P or J \subseteq P, but not both)
    # I \subseteq P iff p divides i. J \subseteq P iff p divides j.
    try:
        if p == 0:
            i_sub = (i == 0)
            j_sub = (j == 0)
        else:
            i_sub = (i % p == 0)
            j_sub = (j % p == 0)
            
        q = (i_sub and not j_sub) or (not i_sub and j_sub)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are comaximal ideals of R",
    "H_3: I \\cap J \\subseteq P",
    "¬Q: It is NOT the case that exactly one of I or J is contained in P"
]

N_HYP = 3
NEG_Q_INDEX = 3