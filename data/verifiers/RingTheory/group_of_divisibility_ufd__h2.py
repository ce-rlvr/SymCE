import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def get_bool_attr(obj, attrs):
    """Helper to safely extract boolean attributes or dictionary keys."""
    if isinstance(obj, dict):
        for attr in attrs:
            if attr in obj:
                return bool(obj[attr])
    else:
        for attr in attrs:
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                return bool(val() if callable(val) else val)
    return None

def conditions(witness) -> list[bool]:
    # H_1: R is an integral domain
    h1 = False
    try:
        val = get_bool_attr(witness, ['is_integral_domain', 'is_domain'])
        if val is not None:
            h1 = val
        elif isinstance(witness, str):
            s = witness.lower()
            if "domain" in s or "ring" in s or "field" in s:
                h1 = True
    except Exception:
        pass

    # ¬Q: The equivalence between R being a UFD and its group of divisibility 
    # being order-isomorphic to a direct sum of copies of Z FAILS.
    # (The true theorem requires the direct sum to have the *product order*. 
    # Without specifying the order, a valuation domain of rank >= 2 is a counterexample 
    # because its group of divisibility is Z^n with lexicographical order).
    neg_q = False
    try:
        is_ufd = get_bool_attr(witness, ['is_UFD', 'is_ufd'])
        is_z_sum = get_bool_attr(witness, ['group_of_divisibility_is_Z_sum', 'group_of_divisibility_is_direct_sum_Z'])
        
        if isinstance(witness, str):
            s = witness.lower()
            if is_ufd is None:
                if "ufd" in s or "unique factorization" in s:
                    is_ufd = True
                elif "valuation" in s:
                    is_ufd = False
            if is_z_sum is None:
                if "valuation" in s and ("rank" in s or "dimension" in s):
                    is_z_sum = True

        # If we cannot determine the properties, assume it behaves like a standard ring
        # where the true theorem holds (so it won't be flagged as a counterexample).
        if is_ufd is None:
            is_ufd = False
        if is_z_sum is None:
            is_z_sum = is_ufd

        # The conclusion fails if the equivalence does not hold
        neg_q = not (is_ufd == is_z_sum)
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: The equivalence between R being a UFD and its group of divisibility being order-isomorphic to a direct sum of copies of Z fails"
]

N_HYP = 1
NEG_Q_INDEX = 1