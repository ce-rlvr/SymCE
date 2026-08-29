import sympy
import math
import itertools
import functools

# Top-level setup for potential witness objects
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def check_eq(a, b):
    """Robust equality check that handles sympy expressions and custom ring elements."""
    try:
        if a == b:
            return True
    except Exception:
        pass
    try:
        diff = a - b
        if hasattr(diff, "simplify"):
            diff = sympy.simplify(diff)
        if hasattr(diff, "is_zero") and diff.is_zero is True:
            return True
        if diff == 0:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness can be a dictionary or an object providing:
      - elements: list of elements in the multiplicative group F_q^\times
      - mul: function(x, y) -> z (the group operation)
      - chi: function(x) -> value (the character)
      - zero: the zero element of the target ring (default 0)
    Alternatively, it can provide 'q' and 'chi' for a Dirichlet character modulo q.
    """
    try:
        # 1. Extract witness components
        if isinstance(witness, dict):
            if 'elements' in witness:
                elements = witness['elements']
                mul = witness['mul']
                chi = witness['chi']
                zero = witness.get('zero', 0)
            elif 'q' in witness:
                q = witness['q']
                chi = witness['chi']
                elements = [x for x in range(1, q) if math.gcd(x, q) == 1]
                mul = lambda x, y: (x * y) % q
                zero = witness.get('zero', 0)
            else:
                return [False, False]
        elif hasattr(witness, "elements") and hasattr(witness, "mul") and hasattr(witness, "chi"):
            elements = witness.elements
            mul = witness.mul
            chi = witness.chi
            zero = getattr(witness, "zero", 0)
        elif hasattr(witness, "modulus") and callable(witness):
            q = witness.modulus
            chi = witness
            elements = [x for x in range(1, q) if math.gcd(x, q) == 1]
            mul = lambda x, y: (x * y) % q
            zero = 0
        else:
            return [False, False]

        if not elements:
            return [False, False]

        # 2. Find the group identity element
        identity = None
        for x in elements:
            is_id = True
            for y in elements:
                if not check_eq(mul(x, y), y) or not check_eq(mul(y, x), y):
                    is_id = False
                    break
            if is_id:
                identity = x
                break
                
        if identity is None:
            return [False, False]
            
        # 3. Check H1: chi is a non-trivial multiplicative character
        is_hom = True
        for x in elements:
            for y in elements:
                if not check_eq(chi(mul(x, y)), chi(x) * chi(y)):
                    is_hom = False
                    break
            if not is_hom:
                break
                
        is_non_trivial = False
        if is_hom:
            id_val = chi(identity)
            for x in elements:
                if not check_eq(chi(x), id_val):
                    is_non_trivial = True
                    break
                    
        h1 = is_hom and is_non_trivial
        
        # 4. Check negated conclusion: The sum is NOT equal to 0
        total = zero
        for x in elements:
            total = total + chi(x)
            
        neg_q = not check_eq(total, zero)
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    r"H_1: \chi is a non-trivial multiplicative character of the multiplicative group F_q^\times",
    r"not Q: The sum \sum_{x \in F_q^\times} \chi(x) is not equal to 0"
]

N_HYP = 1
NEG_Q_INDEX = 1