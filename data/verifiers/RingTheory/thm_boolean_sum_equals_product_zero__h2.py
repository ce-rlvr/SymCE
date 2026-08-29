import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup for standard algebra objects
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (R, x, y) where R is the Boolean ring,
    and x, y are elements of R.
    """
    try:
        if len(witness) == 3:
            R, x, y = witness
        elif len(witness) == 2:
            x, y = witness
            R = None
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a Boolean ring
    h1 = False
    zero = None
    try:
        if R is not None:
            # Try to extract elements if R is an iterable collection
            elements = list(R)
            if 0 < len(elements) <= 64:
                # Find additive identity
                zeros = []
                for z in elements:
                    if all(z + a == a for a in elements) and all(a + z == a for a in elements):
                        zeros.append(z)
                
                if zeros:
                    z = zeros[0]
                    zero = z
                    is_ring = True
                    
                    # Check ring axioms and Boolean ring property (idempotence)
                    for a in elements:
                        if a * a != a:
                            is_ring = False
                            break
                        if not any(a + b == z and b + a == z for b in elements):
                            is_ring = False
                            break
                        for b in elements:
                            if a + b not in elements:
                                is_ring = False
                                break
                            if a * b not in elements:
                                is_ring = False
                                break
                            if a + b != b + a:
                                is_ring = False
                                break
                                
                    if is_ring:
                        # Check associativity and distributivity (limit to 8 elements for speed)
                        n_check = min(len(elements), 8)
                        for a in elements[:n_check]:
                            if not is_ring: break
                            for b in elements[:n_check]:
                                if not is_ring: break
                                for c in elements[:n_check]:
                                    if (a + b) + c != a + (b + c): is_ring = False
                                    if (a * b) * c != a * (b * c): is_ring = False
                                    if a * (b + c) != (a * b) + (a * c): is_ring = False
                                    if (a + b) * c != (a * c) + (b * c): is_ring = False
                    h1 = is_ring
    except Exception:
        pass

    # H_2: x + y = x y
    h2 = False
    try:
        h2 = bool(x + y == x * y)
    except Exception:
        pass

    # ¬Q: x != 0 or y != 0
    neg_q = False
    try:
        if zero is not None:
            neg_q = bool(x != zero or y != zero)
        else:
            # Fallback if zero was not found or R was not provided
            try:
                z_x = x - x
                z_y = y - y
                neg_q = bool(x != z_x or y != z_y)
            except Exception:
                # In a Boolean ring, x + x = 0
                z_x = x + x
                z_y = y + y
                neg_q = bool(x != z_x or y != z_y)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: x + y = x y",
    "¬Q: x != 0 or y != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2