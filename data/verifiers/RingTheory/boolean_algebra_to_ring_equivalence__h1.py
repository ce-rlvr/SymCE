import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        elements = list(witness['elements'])
        meet = witness['meet']
        join = witness['join']
        neg = witness['neg']
        zero = witness['zero']
        one = witness['one']
        
        if zero not in elements or one not in elements:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: Addition is defined as a + b = (a ∧ ¬b) ∨ (¬a ∧ b)
    try:
        h1 = True
        if 'add' in witness:
            add_op = witness['add']
            for a in elements:
                for b in elements:
                    if add_op(a, b) != join(meet(a, neg(b)), meet(neg(a), b)):
                        h1 = False
                        break
                if not h1:
                    break
        else:
            for a in elements:
                for b in elements:
                    if join(meet(a, neg(b)), meet(neg(a), b)) not in elements:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: Multiplication is defined as a · b = a ∧ b
    try:
        h2 = True
        if 'mul' in witness:
            mul_op = witness['mul']
            for a in elements:
                for b in elements:
                    if mul_op(a, b) != meet(a, b):
                        h2 = False
                        break
                if not h2:
                    break
        else:
            for a in elements:
                for b in elements:
                    if meet(a, b) not in elements:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # neg_Q: The algebraic structure (B, +, ·, 0, 1) is NOT a Boolean ring with identity
    is_ring = True
    try:
        add = witness.get('add', lambda a, b: join(meet(a, neg(b)), meet(neg(a), b)))
        mul = witness.get('mul', lambda a, b: meet(a, b))
        
        # Check closure
        for a in elements:
            for b in elements:
                if add(a, b) not in elements:
                    is_ring = False
                if mul(a, b) not in elements:
                    is_ring = False
                    
        if is_ring:
            # Check identity, inverses, and idempotence
            for a in elements:
                if add(a, zero) != a or add(zero, a) != a:
                    is_ring = False
                    break
                
                has_inv = False
                for b in elements:
                    if add(a, b) == zero and add(b, a) == zero:
                        has_inv = True
                        break
                if not has_inv:
                    is_ring = False
                    break
                    
                if mul(a, one) != a or mul(one, a) != a:
                    is_ring = False
                    break
                    
                if mul(a, a) != a:
                    is_ring = False
                    break

        if is_ring:
            # Check commutativity of addition
            for a in elements:
                for b in elements:
                    if add(a, b) != add(b, a):
                        is_ring = False
                        break
                if not is_ring:
                    break
                    
        if is_ring:
            # Check associativity and distributivity
            for a in elements:
                for b in elements:
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)):
                            is_ring = False
                            break
                        if mul(mul(a, b), c) != mul(a, mul(b, c)):
                            is_ring = False
                            break
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)):
                            is_ring = False
                            break
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)):
                            is_ring = False
                            break
                    if not is_ring:
                        break
                if not is_ring:
                    break
    except Exception:
        # If operations fail or raise exceptions, it is not a valid ring
        is_ring = False

    neg_q = not is_ring

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Addition is defined as a + b = (a ∧ ¬b) ∨ (¬a ∧ b)",
    "H_2: Multiplication is defined as a · b = a ∧ b",
    "¬Q: (B, +, ·, 0, 1) is not a Boolean ring with identity"
]

N_HYP = 2
NEG_Q_INDEX = 2