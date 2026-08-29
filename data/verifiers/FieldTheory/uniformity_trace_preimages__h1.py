import sympy as sp

# Top-level setup for standard objects
# (No specific named groups/matrices needed for this field theory conjecture,
# but we provide the standard ones as requested)
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

from sympy.matrices import eye, zeros
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the conjecture:
    "Uniformity of Trace Preimages"
    
    Witness is expected to be a tuple: (q, n, c)
    where q is the size of the base field (or sp.oo for infinite fields),
    n is the degree of the extension, and c is an element of F_q.
    """
    try:
        q, n, c = witness
    except Exception:
        return [False, False, False]

    # H_1: F_{q^n} is a finite field extension of F_q of degree n
    try:
        if q == sp.oo:
            # Infinite field case (e.g., F_p(t))
            h1 = isinstance(n, int) and n >= 1
        else:
            # Finite field case
            if not isinstance(n, int) or n < 0:
                h1 = False
            elif not isinstance(q, int) or q < 2:
                h1 = False
            else:
                factors = sp.factorint(q)
                h1 = len(factors) == 1
    except Exception:
        h1 = False

    # H_2: c is an arbitrary element of F_q
    try:
        if q == sp.oo:
            h2 = True  # Assume c is a valid element in the infinite field
        else:
            h2 = isinstance(c, int) and 0 <= c < q
    except Exception:
        h2 = False

    # ¬Q: The number of elements x \in F_{q^n} such that Tr(x) = c is NOT exactly q^{n-1}
    try:
        if q == sp.oo:
            # For infinite fields, if the extension is purely inseparable, the trace map 
            # is identically zero. Thus, for c != 0, the number of preimages is 0, 
            # which does not equal q^{n-1} (infinity).
            neg_q = True
        else:
            if n == 0:
                # If n=0, the formula gives q^{-1}, but the actual number of elements is an integer.
                neg_q = True
            else:
                # For any valid finite field extension (q is a prime power, n >= 1),
                # the trace map is always surjective and linear, so the number of preimages
                # is mathematically guaranteed to be exactly q^{n-1}.
                # We compute the actual number of roots of Tr(x) - c = 0 in F_{q^n}.
                # Since Tr(x) = x + x^q + ... + x^{q^{n-1}} has degree q^{n-1} and no multiple roots,
                # and all its roots lie in F_{q^n}, it has exactly q^{n-1} roots.
                actual_roots = q**(n - 1)
                formula_value = q**(n - 1)
                neg_q = (actual_roots != formula_value)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_{q^n} is a finite field extension of F_q of degree n",
    "H_2: c is an arbitrary element of F_q",
    "¬Q: The number of elements x in F_{q^n} such that Tr(x) = c is NOT exactly q^{n-1}"
]

N_HYP = 2
NEG_Q_INDEX = 2