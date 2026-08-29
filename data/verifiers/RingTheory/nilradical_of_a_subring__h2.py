import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import itertools
import math
import functools

# Top-level setup for potential witness elements
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

def eq(a, b):
    """Safely compare two elements, handling SymPy equality objects."""
    try:
        return bool(a == b)
    except Exception:
        return False

def in_list(item, lst):
    """Safely check if an item is in a list."""
    for x in lst:
        if eq(item, x):
            return True
    return False

def lists_equal_as_sets(l1, l2):
    """Check if two lists contain the same elements."""
    for x in l1:
        if not in_list(x, l2): return False
    for x in l2:
        if not in_list(x, l1): return False
    return True

def is_ring(elements, add, mul, zero):
    """Check if the given operations define a ring on the elements."""
    try:
        if not in_list(zero, elements): return False
        
        # Closure
        for a in elements:
            for b in elements:
                if not in_list(add(a, b), elements): return False
                if not in_list(mul(a, b), elements): return False
                
        # Commutativity of add
        for a in elements:
            for b in elements:
                if not eq(add(a, b), add(b, a)): return False
                
        # Associativity of add
        for a in elements:
            for b in elements:
                for c in elements:
                    if not eq(add(add(a, b), c), add(a, add(b, c))): return False
                    
        # Identity and inverses of add
        for a in elements:
            if not eq(add(a, zero), a): return False
            if not eq(add(zero, a), a): return False
            has_inv = False
            for b in elements:
                if eq(add(a, b), zero) and eq(add(b, a), zero):
                    has_inv = True
                    break
            if not has_inv: return False
            
        # Associativity of mul
        for a in elements:
            for b in elements:
                for c in elements:
                    if not eq(mul(mul(a, b), c), mul(a, mul(b, c))): return False
                    
        # Distributivity
        for a in elements:
            for b in elements:
                for c in elements:
                    if not eq(mul(a, add(b, c)), add(mul(a, b), mul(a, c))): return False
                    if not eq(mul(add(a, b), c), add(mul(a, c), mul(b, c))): return False
                    
        return True
    except Exception:
        return False

def is_commutative_ring(elements, add, mul, zero):
    """Check if the given operations define a commutative ring with identity."""
    if not is_ring(elements, add, mul, zero):
        return False
    try:
        # Commutativity of mul
        for a in elements:
            for b in elements:
                if not eq(mul(a, b), mul(b, a)): return False
                
        # Multiplicative identity
        has_mul_id = False
        for e in elements:
            is_id = True
            for a in elements:
                if not eq(mul(a, e), a):
                    is_id = False
                    break
            if is_id:
                has_mul_id = True
                break
        if not has_mul_id: return False
        
        return True
    except Exception:
        return False

def nilpotent_elements(elements, mul, zero):
    """Return a list of all nilpotent elements in the finite ring."""
    nilpotents = []
    n_max = len(elements)
    for x in elements:
        curr = x
        is_nil = False
        if eq(curr, zero):
            is_nil = True
        else:
            for _ in range(1, n_max + 1):
                curr = mul(curr, x)
                if eq(curr, zero):
                    is_nil = True
                    break
        if is_nil:
            nilpotents.append(x)
    return nilpotents

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to provide the elements and operations for two rings, S and R.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 8:
            S_elements, S_add, S_mul, S_zero, R_elements, R_add, R_mul, R_zero = witness
        else:
            S_elements = witness.S_elements
            S_add = witness.S_add
            S_mul = witness.S_mul
            S_zero = witness.S_zero
            R_elements = witness.R_elements
            R_add = witness.R_add
            R_mul = witness.R_mul
            R_zero = witness.R_zero
            
        S_elements = list(S_elements)
        R_elements = list(R_elements)
    except Exception:
        return [False, False]

    # H1: S is a commutative ring
    try:
        h1 = is_commutative_ring(S_elements, S_add, S_mul, S_zero)
    except Exception:
        h1 = False

    # Ensure R is a valid ring so that "nilradical of R" is well-defined
    try:
        r_is_ring = is_ring(R_elements, R_add, R_mul, R_zero)
        if not r_is_ring:
            return [h1, False]
    except Exception:
        return [h1, False]

    # Conclusion: The nilradical of R is equal to the intersection of R and the nilradical of S
    try:
        nil_S = nilpotent_elements(S_elements, S_mul, S_zero)
        nil_R = nilpotent_elements(R_elements, R_mul, R_zero)
        
        intersection = [x for x in R_elements if in_list(x, nil_S)]
        
        conclusion = lists_equal_as_sets(nil_R, intersection)
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: S is a commutative ring",
    "¬Q: The nilradical of R is NOT equal to the intersection of R and the nilradical of S"
]

N_HYP = 1
NEG_Q_INDEX = 1