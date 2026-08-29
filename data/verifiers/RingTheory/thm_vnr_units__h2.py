import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def get_ring_attrs(witness):
    if isinstance(witness, dict):
        elements = witness.get('elements')
        zero = witness.get('zero')
        add = witness.get('add')
        mul = witness.get('mul')
        a = witness.get('a')
    else:
        elements = getattr(witness, 'elements', None)
        zero = getattr(witness, 'zero', None)
        add = getattr(witness, 'add', None)
        mul = getattr(witness, 'mul', None)
        a = getattr(witness, 'a', None)
    return elements, zero, add, mul, a

def conditions(witness) -> list[bool]:
    try:
        elements, zero, add, mul, a = get_ring_attrs(witness)
        if elements is None or zero is None or mul is None or a is None:
            return [False, False, False]
        elements = list(elements)
    except Exception:
        return [False, False, False]

    # H_1: R is a von Neumann regular ring
    try:
        h1 = True
        for x in elements:
            found = False
            for y in elements:
                if x == mul(x, mul(y, x)):
                    found = True
                    break
            if not found:
                h1 = False
                break
    except Exception:
        h1 = False

    # H_2: a is not a zero-divisor in R
    # Note: Under the standard definition where a zero-divisor must be non-zero,
    # 0 is not a zero-divisor. This is the dropped hypothesis ("a is non-zero").
    try:
        h2 = False
        if a in elements:
            h2 = True
            if a != zero:
                for x in elements:
                    if x != zero:
                        if mul(a, x) == zero or mul(x, a) == zero:
                            h2 = False
                            break
    except Exception:
        h2 = False

    # ¬Q: a is not a unit in R
    try:
        if a not in elements:
            neg_q = True
        else:
            identities = []
            for e in elements:
                is_id = True
                for x in elements:
                    if mul(e, x) != x or mul(x, e) != x:
                        is_id = False
                        break
                if is_id:
                    identities.append(e)
            
            if not identities:
                neg_q = True
            else:
                is_unit = False
                for e in identities:
                    for b in elements:
                        if mul(a, b) == e and mul(b, a) == e:
                            is_unit = True
                            break
                    if is_unit:
                        break
                neg_q = not is_unit
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a von Neumann regular ring",
    "H_2: a is not a zero-divisor in R",
    "¬Q: a is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2