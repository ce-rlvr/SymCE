import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to provide the ring elements, operations, zero, 
    the idempotent e, and the element x that fails to commute with e.
    """
    try:
        if isinstance(witness, dict):
            elements = witness['elements']
            add = witness['add']
            mul = witness['mul']
            zero = witness['zero']
            e = witness['e']
            x = witness['x']
        elif isinstance(witness, (tuple, list)):
            elements, add, mul, zero, e, x = witness
        else:
            elements = witness.elements
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            e = witness.e
            x = witness.x
            
        elements = list(elements)
    except Exception:
        return [False, False, False, False]

    # H1: R is a ring (additive abelian group, distributive multiplication)
    # Note: We do NOT check associativity of multiplication, as the dropped hypothesis
    # from the true theorem is associativity. The counterexample must be a non-associative ring.
    h1 = True
    try:
        if zero not in elements:
            h1 = False
        else:
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
                    if add(a, b) not in elements: h1 = False; break
                    if mul(a, b) not in elements: h1 = False; break
                    if add(a, b) != add(b, a): h1 = False; break
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)): h1 = False; break
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): h1 = False; break
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): h1 = False; break
                    if not h1: break
                if not h1: break
    except Exception:
        h1 = False

    # H2: R is a reduced ring (contains no non-zero nilpotent elements)
    # We check if any non-zero element can generate zero through repeated multiplication.
    h2 = True
    try:
        for a in elements:
            if a == zero: 
                continue
            generated = [a]
            has_nilpotent = False
            head = 0
            while head < len(generated):
                curr_x = generated[head]
                for j in range(head + 1):
                    curr_y = generated[j]
                    
                    # Check xy
                    xy = mul(curr_x, curr_y)
                    if xy == zero:
                        has_nilpotent = True
                        break
                    if xy not in generated:
                        if len(generated) < len(elements):
                            generated.append(xy)
                            
                    # Check yx
                    yx = mul(curr_y, curr_x)
                    if yx == zero:
                        has_nilpotent = True
                        break
                    if yx not in generated:
                        if len(generated) < len(elements):
                            generated.append(yx)
                if has_nilpotent:
                    break
                head += 1
            if has_nilpotent:
                h2 = False
                break
    except Exception:
        h2 = False

    # H3: e is an idempotent element of R
    h3 = False
    try:
        if e in elements and mul(e, e) == e:
            h3 = True
    except Exception:
        h3 = False

    # ¬Q: e is not in the center of R (ex != xe)
    neg_q = False
    try:
        if x in elements and mul(e, x) != mul(x, e):
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: R is a reduced ring (contains no non-zero nilpotent elements)",
    "H_3: e is an idempotent element of R",
    "¬Q: e is not in the center of R (ex != xe)"
]

N_HYP = 3
NEG_Q_INDEX = 3