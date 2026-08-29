import sympy
from sympy import GF, Matrix, eye, zeros
from sympy.abc import x, y, z
import itertools

# Top-level setup for potential witness elements
Z2 = GF(2)
I2 = eye(2)
O2 = zeros(2, 2)

def eq(a, b):
    if a is b:
        return True
    try:
        if hasattr(a, 'equals'):
            return a.equals(b)
        if hasattr(a, 'shape') and hasattr(b, 'shape'):
            return a == b
        return a == b
    except Exception:
        return False

def is_boolean_ring(R):
    if R is None:
        raise ValueError("Ring is None")
        
    # SymPy domains
    if hasattr(R, 'is_Ring') and R.is_Ring:
        if getattr(R, 'is_Field', False):
            if getattr(R, 'order', None) == 2:
                return True
            return False
        if hasattr(R, 'is_FiniteField') and R.is_FiniteField:
            if getattr(R, 'order', None) == 2:
                return True
            return False
        # Other SymPy rings like ZZ, QQ are not Boolean
        return False

    if hasattr(R, 'order') and getattr(R, 'order', None) == 2 and hasattr(R, 'characteristic') and getattr(R, 'characteristic', None) == 2:
        return True

    elements = None
    add = None
    mul = None

    if hasattr(R, 'elements') and hasattr(R, 'add') and hasattr(R, 'mul'):
        elements = list(R.elements)
        add = R.add
        mul = R.mul
    elif isinstance(R, tuple) and len(R) == 3 and isinstance(R[1], dict) and isinstance(R[2], dict):
        elements = list(R[0])
        add = lambda a, b: R[1].get((a, b))
        mul = lambda a, b: R[2].get((a, b))
    elif isinstance(R, (list, tuple, set)):
        elements = list(R)
        add = lambda a, b: a + b
        mul = lambda a, b: a * b
    else:
        raise ValueError("Unrecognized ring format")

    if not elements:
        return False

    # Find zero
    zero = None
    for e in elements:
        if all(eq(add(e, a), a) and eq(add(a, e), a) for a in elements):
            zero = e
            break
    if zero is None:
        return False

    for a in elements:
        # Boolean property: x^2 = x
        if not eq(mul(a, a), a):
            return False
        
        # Additive inverse
        has_inv = False
        for b in elements:
            if eq(add(a, b), zero) and eq(add(b, a), zero):
                has_inv = True
                break
        if not has_inv:
            return False
        
        for b in elements:
            ab_add = add(a, b)
            ab_mul = mul(a, b)
            
            # Closure
            if not any(eq(ab_add, c) for c in elements): return False
            if not any(eq(ab_mul, c) for c in elements): return False
            
            # Commutativity of addition
            if not eq(ab_add, add(b, a)): return False
            
            for c in elements:
                # Associativity of addition
                if not eq(add(add(a, b), c), add(a, add(b, c))): return False
                # Associativity of multiplication
                if not eq(mul(mul(a, b), c), mul(a, mul(b, c))): return False
                # Distributivity
                if not eq(mul(a, add(b, c)), add(mul(a, b), mul(a, c))): return False
                if not eq(mul(add(a, b), c), add(mul(a, c), mul(b, c))): return False

    return True

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Expected witness format: a tuple (R, S, T) or a dict {'R': R, 'S': S, 'T': T}.
    """
    if isinstance(witness, dict):
        R = witness.get('R')
        S = witness.get('S')
        T = witness.get('T')
    elif isinstance(witness, tuple) and len(witness) == 3:
        R, S, T = witness
    else:
        return [False, False]
        
    try:
        h1 = is_boolean_ring(R) and is_boolean_ring(S)
    except Exception:
        h1 = False
        
    try:
        neg_q = not is_boolean_ring(T)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are Boolean rings",
    "¬Q: T is not a Boolean ring"
]

N_HYP = 1
NEG_Q_INDEX = 1