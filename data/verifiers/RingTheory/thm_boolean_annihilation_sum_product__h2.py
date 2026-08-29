import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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

def extract_ring(witness):
    """
    Extracts the elements, addition, multiplication, and zero element from the witness.
    Supports multiple formats:
    1. Tuple: (n, add_table, mul_table)
    2. Object with attributes/methods: elements, add, mul, zero
    3. Dictionary with keys: 'elements', 'add', 'mul', 'zero'
    4. Iterable of elements (infers + and * operators)
    """
    if isinstance(witness, tuple) and len(witness) == 3 and isinstance(witness[0], int):
        n, add_table, mul_table = witness
        elements = list(range(n))
        def add(x, y): return add_table[x][y]
        def mul(x, y): return mul_table[x][y]
        zero = 0
        return elements, add, mul, zero
    elif hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'zero'):
        elements = witness.elements() if callable(witness.elements) else witness.elements
        zero = witness.zero() if callable(witness.zero) else witness.zero
        return list(elements), witness.add, witness.mul, zero
    elif isinstance(witness, dict) and 'elements' in witness:
        elements = witness['elements']
        add = witness['add']
        mul = witness['mul']
        zero = witness['zero']
        return list(elements), add, mul, zero
    else:
        elements = list(witness)
        def add(x, y): return x + y
        def mul(x, y): return x * y
        zero = None
        for e in elements:
            if all(add(e, x) == x for x in elements):
                zero = e
                break
        return elements, add, mul, zero

def conditions(witness) -> list[bool]:
    try:
        elements, add, mul, zero = extract_ring(witness)
    except Exception:
        return [False, False]
        
    h1_ok = True
    try:
        if zero not in elements:
            h1_ok = False
        else:
            # Check non-associative Boolean ring axioms
            # (Associativity of multiplication is intentionally omitted as it is the dropped hypothesis)
            for x in elements:
                # Boolean condition: x^2 = x
                if mul(x, x) != x:
                    h1_ok = False
                    break
                # Additive identity
                if add(x, zero) != x or add(zero, x) != x:
                    h1_ok = False
                    break
                
                # Additive inverse
                has_inv = False
                for y in elements:
                    if add(x, y) == zero and add(y, x) == zero:
                        has_inv = True
                        break
                if not has_inv:
                    h1_ok = False
                    break
                    
                for y in elements:
                    # Closure
                    if add(x, y) not in elements:
                        h1_ok = False
                        break
                    if mul(x, y) not in elements:
                        h1_ok = False
                        break
                    # Commutativity of addition
                    if add(x, y) != add(y, x):
                        h1_ok = False
                        break
                    
                    for z in elements:
                        # Associativity of addition
                        if add(add(x, y), z) != add(x, add(y, z)):
                            h1_ok = False
                            break
                        # Left distributivity
                        if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)):
                            h1_ok = False
                            break
                        # Right distributivity
                        if mul(add(x, y), z) != add(mul(x, z), mul(y, z)):
                            h1_ok = False
                            break
                    if not h1_ok: break
                if not h1_ok: break
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        for x in elements:
            for y in elements:
                # In a non-associative ring, x * y * (x + y) can be grouped in two ways.
                # If either grouping yields a non-zero result, the identity fails.
                term1 = mul(mul(x, y), add(x, y))
                term2 = mul(x, mul(y, add(x, y)))
                
                if term1 != zero or term2 != zero:
                    neg_q_ok = True
                    break
            if neg_q_ok:
                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: x y (x + y) != 0 for some x, y in R"
]

N_HYP = 1
NEG_Q_INDEX = 1