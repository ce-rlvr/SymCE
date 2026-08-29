import math
import re
from sympy import Symbol, eye, zeros
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def get_d(witness):
    """
    Attempt to extract the integer d from a witness representing the ring Z[sqrt(d)].
    Handles integers, SymPy integers, polynomials like x**2 - d, and strings.
    """
    try:
        if isinstance(witness, int):
            return witness
        if hasattr(witness, 'is_Integer') and witness.is_Integer:
            return int(witness)
        
        # Try to treat as a polynomial x**2 - d
        try:
            x = Symbol('x')
            poly = witness.as_poly(x)
            if poly is not None and poly.degree() == 2:
                coeffs = poly.all_coeffs()
                if coeffs[0] == 1 and coeffs[1] == 0:
                    return -int(coeffs[2])
        except Exception:
            pass

        # Try to treat as sqrt(d)
        try:
            val = witness**2
            if hasattr(val, 'is_Integer') and val.is_Integer:
                return int(val)
        except Exception:
            pass

        # Fallback to string parsing
        s = str(witness)
        m = re.search(r'sqrt\((-?\d+)\)', s)
        if m:
            return int(m.group(1))
        m = re.search(r'x(?:\*\*|\^)2\s*\+\s*(\d+)', s)
        if m:
            return -int(m.group(1))
        m = re.search(r'-?\d+', s)
        if m:
            return int(m.group(0))
    except Exception:
        pass
    return None

def conditions(witness) -> list[bool]:
    try:
        d = get_d(witness)
        if d is None or d >= 0:
            # We only handle imaginary quadratic fields for this verifier
            neg_q = False
        else:
            # Compute the class number of the order Z[sqrt(d)]
            # The discriminant of Z[sqrt(d)] is 4d
            D = 4 * d
            h = 0
            b_max = int((-D / 3.0)**0.5)
            for b in range(-b_max, b_max + 1):
                rem = b**2 - D
                if rem % 4 != 0:
                    continue
                ac = rem // 4
                a_max = int(ac**0.5)
                for a in range(1, a_max + 1):
                    if ac % a == 0:
                        c = ac // a
                        if abs(b) <= a and a <= c:
                            # Check primitivity of the quadratic form
                            if math.gcd(math.gcd(a, abs(b)), c) != 1:
                                continue
                            # Count reduced forms
                            if abs(b) == a or a == c:
                                if b >= 0:
                                    h += 1
                            else:
                                h += 1
            # The Picard group is trivial iff the class number is 1
            neg_q = (h > 1)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The Picard group Pic(R) is not the trivial group"
]

N_HYP = 0
NEG_Q_INDEX = 0