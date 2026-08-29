import sympy
import math
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_ring(witness):
    """
    Extracts ring elements and operations from the witness.
    Supports a tuple (n, add_table, mul_table) or an object with elements, add, mul, zero.
    """
    if isinstance(witness, tuple) and len(witness) == 3:
        n, add_table, mul_table = witness
        elements = list(range(n))
        zero = 0
        def add(x, y): return add_table[x][y]
        def mul(x, y): return mul_table[x][y]
        return elements, add, mul, zero
    elif hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'zero'):
        elements = list(witness.elements)
        add = witness.add
        mul = witness.mul
        zero = witness.zero
        return elements, add, mul, zero
    else:
        raise ValueError("Unknown ring representation")

def is_commutative(elements, mul):
    for a in elements:
        for b in elements:
            if mul(a, b) != mul(b, a):
                return False
    return True

def get_characteristic(elements, add, zero):
    char = 1
    for x in elements:
        curr = x
        order = 1
        while curr != zero and order <= len(elements):
            curr = add(curr, x)
            order += 1
        if order > len(elements):
            return 0
        char = (char * order) // math.gcd(char, order)
    return char

def conditions(witness) -> list[bool]:
    try:
        elements, add, mul, zero = get_ring(witness)
    except Exception:
        return [False, False, False]
        
    # H_1: R is a commutative ring of prime characteristic p
    try:
        h1 = False
        if is_commutative(elements, mul):
            char = get_characteristic(elements, add, zero)
            if sympy.isprime(char):
                h1 = True
    except Exception:
        h1 = False

    # H_2: R is a reduced ring (no non-zero nilpotent elements)
    try:
        h2 = True
        for x in elements:
            if x == zero:
                continue
            curr = x
            is_nilp = False
            for _ in range(len(elements)):
                curr = mul(curr, x)
                if curr == zero:
                    is_nilp = True
                    break
            if is_nilp:
                h2 = False
                break
    except Exception:
        h2 = False

    # ¬Q: The kernel of the Frobenius endomorphism F(x) = x^p is NOT the trivial ideal {0}
    try:
        neg_q = False
        char = get_characteristic(elements, add, zero)
        if char > 0:
            for x in elements:
                if x == zero:
                    continue
                curr = x
                for _ in range(char - 1):
                    curr = mul(curr, x)
                if curr == zero:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring of prime characteristic p",
    "H_2: R is a reduced ring",
    "¬Q: The kernel of F is not the trivial ideal {0}"
]

N_HYP = 2
NEG_Q_INDEX = 2