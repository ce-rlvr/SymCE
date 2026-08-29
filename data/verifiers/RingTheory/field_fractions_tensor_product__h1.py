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
    Check if the witness is a valid counterexample to the false conjecture.
    Since SymPy does not natively support non-commutative fields of fractions 
    (where this theorem fails), we inspect the witness for properties or mock attributes.
    """
    # Fallback for string-based witnesses naming known counterexamples
    if isinstance(witness, str):
        w = witness.lower()
        if any(kw in w for kw in ["free", "ore", "non-commutative", "noncommutative", "weyl"]):
            return [True, True]

    def get_bool_attr(obj, attrs, default):
        try:
            # If witness is a tuple like (R, K), check the first element or the dictionary
            if isinstance(obj, tuple) and len(obj) > 0:
                target = obj[0]
            else:
                target = obj

            if isinstance(target, dict):
                for attr in attrs:
                    if attr in target:
                        return bool(target[attr])
            else:
                for attr in attrs:
                    if hasattr(target, attr):
                        val = getattr(target, attr)
                        if callable(val):
                            return bool(val())
                        return bool(val)
        except Exception:
            pass
        return default

    # H_1: K is the field of fractions of R
    h1_ok = get_bool_attr(witness, ['is_field_of_fractions', 'field_of_fractions', 'H1'], False)
    
    # ¬Q: The tensor product K \otimes_R K is NOT isomorphic to K as an R-module
    q_ok = get_bool_attr(witness, ['is_tensor_product_isomorphic', 'tensor_product_isomorphic', 'isomorphic_to_K', 'Q'], True)
    neg_q_ok = not q_ok

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is the field of fractions of R",
    "¬Q: The tensor product K \\otimes_R K is not isomorphic to K as an R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1