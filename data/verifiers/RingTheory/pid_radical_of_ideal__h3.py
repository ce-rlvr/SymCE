import sympy
from sympy import Expr, sqf_part, cancel
from sympy.ntheory import factorint
from sympy.abc import x, y, z

# Top-level setup for potential polynomial witnesses
# x, y, z are available for expressions like x**2

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: a is a non-zero, non-unit element of R",
    "¬Q: The radical of the ideal (a) is not the principal ideal (p_1 p_2 ... p_k)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Parse the witness. It could be:
        # 1. An integer or polynomial `a` (implying p_1...p_k is the full factorization, so prod_p = a)
        # 2. A list/tuple of factors [p_1, ..., p_k], where `a` is their product
        # 3. A tuple (a, [p_1, ..., p_k])
        if isinstance(witness, (int, sympy.Integer)):
            a = witness
            prod_p = witness
        elif isinstance(witness, Expr):
            a = witness
            prod_p = witness
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 2 and isinstance(witness[1], (list, tuple)):
                a = witness[0]
                prod_p = 1
                for p in witness[1]:
                    prod_p *= p
            else:
                a = 1
                for p in witness:
                    a *= p
                prod_p = a
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a principal ideal domain
    # We assume the witness is provided in Z or F[x], which are PIDs.
    h1 = True

    # H_2: a is a non-zero, non-unit element of R
    try:
        if isinstance(a, (int, sympy.Integer)) or (hasattr(a, 'is_number') and a.is_number):
            a_val = int(a)
            h2 = (a_val != 0) and (abs(a_val) != 1)
        else:
            # For polynomials in F[x], non-units have degree > 0 (i.e., have free symbols)
            h2 = (a != 0) and (len(a.free_symbols) > 0)
    except Exception:
        h2 = False

    # neg_Q: The radical of the ideal (a) is not the principal ideal (p_1 p_2 ... p_k)
    try:
        if isinstance(a, (int, sympy.Integer)) or (hasattr(a, 'is_number') and a.is_number):
            a_val = int(a)
            prod_val = int(prod_p)
            if a_val == 0:
                rad_a = 0
            else:
                f = factorint(abs(a_val))
                rad_a = 1
                for p in f:
                    rad_a *= p
            # In Z, ideals are equal iff their generators have the same absolute value
            neg_q = (abs(rad_a) != abs(prod_val))
        else:
            # For polynomials
            rad_a = sqf_part(a)
            # Two polynomials generate the same ideal in F[x] iff they divide each other,
            # which means their ratio is a non-zero constant.
            ratio1 = cancel(rad_a / prod_p)
            ratio2 = cancel(prod_p / rad_a)
            neg_q = not (bool(ratio1.is_constant()) and bool(ratio2.is_constant()))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]