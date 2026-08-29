import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools

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
    try:
        h1 = bool(witness.is_abelian)
    except Exception:
        h1 = False

    try:
        order = witness.order()
        h2 = bool(isinstance(order, (int, sympy.Integer)) and order % 2 == 1)
    except Exception:
        h2 = False

    try:
        elements_iter = iter(witness.elements)
        elements = list(itertools.islice(elements_iter, 2001))
        
        if len(elements) > 2000:
            is_homo = bool(witness.is_abelian)
            order = witness.order()
            if not isinstance(order, (int, sympy.Integer)):
                raise ValueError("Cannot determine bijection for infinite group")
            is_bij = bool(order % 2 == 1)
            is_auto = is_homo and is_bij
        else:
            try:
                # Try multiplicative notation (standard for sympy groups)
                is_homo = True
                for x in elements:
                    for y in elements:
                        if (x * y)**2 != (x**2) * (y**2):
                            is_homo = False
                            break
                    if not is_homo:
                        break
                
                is_bij = True
                if is_homo:
                    seen = set()
                    for x in elements:
                        seen.add(x**2)
                    if len(seen) != len(elements):
                        is_bij = False
                is_auto = is_homo and is_bij
            except Exception:
                # Try additive notation (for custom additive groups)
                is_homo = True
                for x in elements:
                    for y in elements:
                        if (x + y) + (x + y) != (x + x) + (y + y):
                            is_homo = False
                            break
                    if not is_homo:
                        break
                
                is_bij = True
                if is_homo:
                    seen = set()
                    for x in elements:
                        seen.add(x + x)
                    if len(seen) != len(elements):
                        is_bij = False
                is_auto = is_homo and is_bij
                
        neg_q = not is_auto
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: The order of G is an odd integer",
    "¬Q: The map f(x) = 2x is not a group automorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2