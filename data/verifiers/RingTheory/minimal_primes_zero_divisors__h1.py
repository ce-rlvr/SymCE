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

from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def _is_ideal(elements, add, mul, zero, I_elements):
    if zero not in I_elements: 
        return False
    for a in I_elements:
        has_inv = False
        for b in I_elements:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: 
            return False
        for b in I_elements:
            if add(a, b) not in I_elements: 
                return False
    for r in elements:
        for x in I_elements:
            if mul(r, x) not in I_elements: 
                return False
            if mul(x, r) not in I_elements: 
                return False
    return True

def _is_prime_ideal(elements, add, mul, zero, I_elements):
    if not _is_ideal(elements, add, mul, zero, I_elements): 
        return False
    if len(I_elements) == len(elements): 
        return False
    for a in elements:
        if a in I_elements: 
            continue
        for b in elements:
            if b in I_elements: 
                continue
            subset = True
            for r in elements:
                if mul(a, mul(r, b)) not in I_elements:
                    subset = False
                    break
            if subset: 
                return False
    return True

def _is_minimal_prime_ideal(elements, add, mul, zero, P_elements):
    if not _is_prime_ideal(elements, add, mul, zero, P_elements): 
        return False
    for i in range(1, len(P_elements)):
        for subset in itertools.combinations(P_elements, i):
            if zero not in subset: 
                continue
            if _is_prime_ideal(elements, add, mul, zero, subset): 
                return False
    return True

def _is_zero_divisor(elements, mul, zero, a):
    for b in elements:
        if b != zero:
            if mul(a, b) == zero or mul(b, a) == zero:
                return True
    return False

def conditions(witness):
    h1 = False
    neg_q = False

    # Handle 5-tuple witness for finite rings: (elements, add, mul, zero, P)
    if isinstance(witness, tuple) and len(witness) == 5:
        elements, add, mul, zero, P = witness
        try:
            h1 = _is_minimal_prime_ideal(elements, add, mul, zero, P)
        except Exception:
            h1 = False
        try:
            neg_q = False
            for a in P:
                if not _is_zero_divisor(elements, mul, zero, a):
                    neg_q = True
                    break
        except Exception:
            neg_q = False
        return [h1, neg_q]

    # Handle 2-tuple witness: (R, P)
    if isinstance(witness, tuple) and len(witness) == 2:
        R, P = witness
        try:
            if hasattr(P, 'is_minimal_prime_ideal'):
                h1 = bool(P.is_minimal_prime_ideal(R))
            elif hasattr(R, 'is_minimal_prime_ideal'):
                h1 = bool(R.is_minimal_prime_ideal(P))
        except Exception:
            pass
            
        try:
            if hasattr(P, 'has_non_zero_divisor'):
                neg_q = bool(P.has_non_zero_divisor(R))
            elif hasattr(R, 'has_non_zero_divisor_in'):
                neg_q = bool(R.has_non_zero_divisor_in(P))
        except Exception:
            pass
            
        return [h1, neg_q]

    # Handle dictionary witness
    if isinstance(witness, dict):
        try:
            if 'is_minimal_prime_ideal' in witness:
                h1 = bool(witness['is_minimal_prime_ideal']())
            elif 'elements' in witness:
                h1 = _is_minimal_prime_ideal(witness['elements'], witness['add'], witness['mul'], witness['zero'], witness['P'])
        except Exception:
            pass
            
        try:
            if 'has_non_zero_divisor_in_P' in witness:
                neg_q = bool(witness['has_non_zero_divisor_in_P']())
            elif 'elements' in witness:
                neg_q = False
                for a in witness['P']:
                    if not _is_zero_divisor(witness['elements'], witness['mul'], witness['zero'], a):
                        neg_q = True
                        break
        except Exception:
            pass
            
        return [h1, neg_q]

    # Handle object witness
    try:
        if hasattr(witness, 'is_minimal_prime_ideal'):
            h1 = bool(witness.is_minimal_prime_ideal())
        elif hasattr(witness, 'P') and hasattr(witness.P, 'is_minimal_prime_ideal'):
            h1 = bool(witness.P.is_minimal_prime_ideal())
        elif hasattr(witness, 'elements'):
            h1 = _is_minimal_prime_ideal(witness.elements, witness.add, witness.mul, witness.zero, witness.P)
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'has_non_zero_divisor_in_P'):
            neg_q = bool(witness.has_non_zero_divisor_in_P())
        elif hasattr(witness, 'P') and hasattr(witness.P, 'has_non_zero_divisor'):
            neg_q = bool(witness.P.has_non_zero_divisor())
        elif hasattr(witness, 'elements'):
            neg_q = False
            for a in witness.P:
                if not _is_zero_divisor(witness.elements, witness.mul, witness.zero, a):
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a minimal prime ideal of R",
    "¬Q: There exists an element in P which is not a zero divisor in R"
]

N_HYP = 1
NEG_Q_INDEX = 1