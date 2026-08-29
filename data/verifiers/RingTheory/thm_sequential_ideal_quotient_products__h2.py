import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros, Rational, Integer
import operator

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

def get_attr(witness, attr):
    if isinstance(witness, dict):
        if attr in witness:
            return witness[attr]
    else:
        if hasattr(witness, attr):
            return getattr(witness, attr)
    
    if attr == 'add':
        return operator.add
    if attr == 'mul':
        return operator.mul
    raise AttributeError(f"Missing attribute {attr}")

def is_in(val, container):
    if callable(container):
        return container(val)
    if isinstance(container, (list, tuple, set)):
        for item in container:
            if item == val: return True
        return False
    else:
        return val in container

def conditions(witness) -> list[bool]:
    try:
        elements = get_attr(witness, 'elements')
        add = get_attr(witness, 'add')
        mul = get_attr(witness, 'mul')
        try:
            zero = get_attr(witness, 'zero')
        except AttributeError:
            zero = None
            for z in elements:
                is_z = True
                for a in elements:
                    if add(a, z) != a or add(z, a) != a:
                        is_z = False
                        break
                if is_z:
                    zero = z
                    break
            if zero is None:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: R is a commutative ring
    h1 = True
    try:
        # Check closure
        for a in elements:
            for b in elements:
                if not is_in(add(a, b), elements):
                    h1 = False
                    break
                if not is_in(mul(a, b), elements):
                    h1 = False
                    break
            if not h1: break

        if h1:
            # Check abelian group under add
            for a in elements:
                if add(a, zero) != a or add(zero, a) != a:
                    h1 = False
                    break
                has_inv = False
                for b in elements:
                    if add(a, b) == zero and add(b, a) == zero:
                        has_inv = True
                        break
                if not has_inv:
                    h1 = False
                    break
                for b in elements:
                    if add(a, b) != add(b, a):
                        h1 = False
                        break
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)):
                            h1 = False
                            break
                if not h1: break
                
        if h1:
            # Check commutative mul and distributivity
            for a in elements:
                for b in elements:
                    if mul(a, b) != mul(b, a):
                        h1 = False
                        break
                    for c in elements:
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)):
                            h1 = False
                            break
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)):
                            h1 = False
                            break
                if not h1: break
    except Exception:
        h1 = False

    # H2: x and y are elements of R
    h2 = False
    try:
        x_val = get_attr(witness, 'x')
        y_val = get_attr(witness, 'y')
        if is_in(x_val, elements) and is_in(y_val, elements):
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: (I : xy) != ((I : x) : y)
    neg_q = False
    try:
        x_val = get_attr(witness, 'x')
        y_val = get_attr(witness, 'y')
        I = get_attr(witness, 'I')
        
        xy = mul(x_val, y_val)
        I_xy = []
        for r in elements:
            if is_in(mul(r, xy), I):
                I_xy.append(r)
                
        I_x = []
        for r in elements:
            if is_in(mul(r, x_val), I):
                I_x.append(r)
                
        I_x_y = []
        for r in elements:
            if is_in(mul(r, y_val), I_x):
                I_x_y.append(r)
                
        def is_subset(lst1, lst2):
            for item1 in lst1:
                if not is_in(item1, lst2): return False
            return True
            
        if not (is_subset(I_xy, I_x_y) and is_subset(I_x_y, I_xy)):
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: x and y are elements of R",
    "¬Q: The ideal quotient (I : xy) is not equal to the iterated ideal quotient ((I : x) : y)"
]

N_HYP = 2
NEG_Q_INDEX = 2