import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
from sympy.abc import *
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
    Checks if the witness is a valid counterexample to the conjecture:
    Hypotheses:
      H1: R is a ring
      H2: x is an element of J(R)
      H3: y is an element of R
    Conclusion:
      1 - xy is a unit in R
    """
    try:
        # Flexible witness unpacking
        if isinstance(witness, dict):
            R = witness.get('R', [])
            x = witness.get('x', None)
            y = witness.get('y', None)
            add = witness.get('add', lambda a, b: a + b)
            mul = witness.get('mul', lambda a, b: a * b)
            eq = witness.get('eq', lambda a, b: a == b)
        elif isinstance(witness, (list, tuple)) and len(witness) >= 3:
            R = witness[0]
            x = witness[1]
            y = witness[2]
            add = witness[3] if len(witness) > 3 else lambda a, b: a + b
            mul = witness[4] if len(witness) > 4 else lambda a, b: a * b
            eq = witness[5] if len(witness) > 5 else lambda a, b: a == b
        else:
            R = getattr(witness, 'R', [])
            x = getattr(witness, 'x', None)
            y = getattr(witness, 'y', None)
            add = getattr(witness, 'add', lambda a, b: a + b)
            mul = getattr(witness, 'mul', lambda a, b: a * b)
            eq = getattr(witness, 'eq', lambda a, b: a == b)
            
        if not isinstance(R, (list, tuple, set)):
            R = list(R)
            
        if len(R) == 0 or len(R) > 1000:
            return [False, False, False, False]
            
    except Exception:
        return [False, False, False, False]

    def in_R(elem):
        for r in R:
            try:
                if eq(elem, r): return True
            except Exception:
                pass
        return False

    # H1: R is a ring
    h1_ok = False
    zero = None
    try:
        is_ring = True
        # Check closure
        for a in R:
            for b in R:
                if not in_R(add(a, b)): is_ring = False
                if not in_R(mul(a, b)): is_ring = False
        
        if is_ring:
            # Find additive identity (zero)
            for z in R:
                is_z = True
                for a in R:
                    if not (eq(add(z, a), a) and eq(add(a, z), a)):
                        is_z = False
                        break
                if is_z:
                    zero = z
                    break
            if zero is None:
                is_ring = False
        
        if is_ring:
            # Check additive inverses
            for a in R:
                has_inv = False
                for b in R:
                    if eq(add(a, b), zero) and eq(add(b, a), zero):
                        has_inv = True
                        break
                if not has_inv:
                    is_ring = False
                    break
                    
        if is_ring and len(R) <= 30:
            # Check associativity and distributivity (for small rings)
            for a in R:
                for b in R:
                    for c in R:
                        if not eq(add(add(a, b), c), add(a, add(b, c))): is_ring = False
                        if not eq(mul(mul(a, b), c), mul(a, mul(b, c))): is_ring = False
                        if not eq(mul(a, add(b, c)), add(mul(a, b), mul(a, c))): is_ring = False
                        if not eq(mul(add(a, b), c), add(mul(a, c), mul(b, c))): is_ring = False
                        if not eq(add(a, b), add(b, a)): is_ring = False
                        if not is_ring: break
                    if not is_ring: break
                if not is_ring: break
                
        h1_ok = is_ring
    except Exception:
        h1_ok = False

    # H2: x is an element of J(R)
    h2_ok = False
    try:
        if h1_ok and in_R(x):
            is_in_J = True
            # J(R) is the set of elements x such that for all r in R, x*r is right quasi-regular.
            # An element 'a' is right quasi-regular if there exists 'b' such that a + b - ab = 0 => a + b = ab
            for r in R:
                a = mul(x, r)
                has_qr = False
                for b in R:
                    if eq(add(a, b), mul(a, b)):
                        has_qr = True
                        break
                if not has_qr:
                    is_in_J = False
                    break
            h2_ok = is_in_J
    except Exception:
        h2_ok = False

    # H3: y is an element of R
    h3_ok = False
    try:
        if h1_ok:
            h3_ok = in_R(y)
    except Exception:
        h3_ok = False

    # Negated Conclusion: 1 - xy is NOT a unit in R
    neg_q_ok = False
    try:
        if h1_ok:
            id_R = None
            # Find multiplicative identity (1_R)
            for e in R:
                is_id = True
                for a in R:
                    if not (eq(mul(e, a), a) and eq(mul(a, e), a)):
                        is_id = False
                        break
                if is_id:
                    id_R = e
                    break
            
            if id_R is None:
                # If R has no identity, "1 - xy is a unit in R" is false.
                neg_q_ok = True
            else:
                xy = mul(x, y)
                neg_xy = None
                for b in R:
                    if eq(add(xy, b), zero) and eq(add(b, xy), zero):
                        neg_xy = b
                        break
                
                if neg_xy is None:
                    neg_q_ok = True
                else:
                    E = add(id_R, neg_xy) # E = 1 - xy
                    if not in_R(E):
                        neg_q_ok = True
                    else:
                        is_unit = False
                        for b in R:
                            if eq(mul(E, b), id_R) and eq(mul(b, E), id_R):
                                is_unit = True
                                break
                        neg_q_ok = not is_unit
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(h3_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: x is an element of J(R)",
    "H_3: y is an element of R",
    "¬Q: 1 - xy is not a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3