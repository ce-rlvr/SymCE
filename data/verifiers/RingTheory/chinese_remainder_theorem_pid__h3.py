import math
from functools import reduce
from sympy import Expr, Integer, Poly, sympify
from sympy import lcm as sympy_lcm
from sympy.abc import x, y, z, t

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a list of elements [a_1, a_2, ..., a_k] from a PID.
    We support integers (implicitly R=ZZ) and univariate polynomials (implicitly R=F[x]).
    """
    # Allow witness to be of the form ("ZZ", [a_1, ..., a_k]) or just [a_1, ..., a_k]
    if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], str):
        elements = witness[1]
    else:
        elements = witness

    try:
        if not isinstance(elements, (list, tuple)) or len(elements) < 1:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        elements = [sympify(e) for e in elements]
    except Exception:
        pass

    # H_1: R is a principal ideal domain
    h1 = False
    is_int = False
    is_poly = False
    try:
        if all(isinstance(e, int) or isinstance(e, Integer) for e in elements):
            h1 = True
            is_int = True
        elif all(isinstance(e, Expr) for e in elements):
            symbols = set()
            for e in elements:
                symbols.update(e.free_symbols)
            # Univariate polynomials over a field form a PID
            if len(symbols) <= 1:
                h1 = True
                is_poly = True
    except Exception:
        pass

    # H_2: a_1, a_2, \dots, a_k are non-zero elements of R
    h2 = False
    try:
        if is_int:
            h2 = all(int(e) != 0 for e in elements)
        elif is_poly:
            h2 = all(e != 0 for e in elements)
    except Exception:
        pass

    # ¬Q: R/(a_1 a_2 \cdots a_k) is NOT isomorphic to R/(a_1) \times \cdots \times R/(a_k)
    neg_q = False
    try:
        if is_int:
            ints = [abs(int(e)) for e in elements]
            prod = 1
            for val in ints:
                prod *= val
            l = reduce(sympy_lcm, ints)
            # For ZZ, they are isomorphic iff lcm(|a_i|) == |prod(a_i)|
            neg_q = (l != prod)
        elif is_poly:
            prod = elements[0]
            for val in elements[1:]:
                prod = prod * val
            l = reduce(sympy_lcm, elements)
            
            if h2:
                deg_prod = Poly(prod).degree()
                deg_lcm = Poly(l).degree()
                # For F[x], they are isomorphic iff deg(lcm(a_i)) == deg(prod(a_i))
                neg_q = (deg_lcm != deg_prod)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: a_1, a_2, ..., a_k are non-zero elements of R",
    "¬Q: R/(a_1...a_k) is not isomorphic to R/(a_1) x ... x R/(a_k)"
]

N_HYP = 2
NEG_Q_INDEX = 2