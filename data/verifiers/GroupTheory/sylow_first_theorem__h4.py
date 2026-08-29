import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (G, p, n, m), checks the hypotheses and the negated conclusion.
    """
    try:
        G, p, n, m = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The order of G is p^n * m
    try:
        order_G = sympy.sympify(G.order())
        expr = (sympy.sympify(p) ** sympy.sympify(n)) * sympy.sympify(m)
        h2 = bool(order_G == expr)
    except Exception:
        h2 = False

    # H_3: p is a prime number
    try:
        h3 = bool(sympy.isprime(p))
    except Exception:
        h3 = False

    # H_4: p does not divide m
    try:
        # p divides m if m/p is an integer.
        # So p does NOT divide m if m/p is NOT an integer.
        ratio = sympy.sympify(m) / sympy.sympify(p)
        h4 = bool(not ratio.is_integer)
    except Exception:
        h4 = False

    # ¬Q: G does NOT contain a subgroup of order p^n
    try:
        target = sympy.sympify(p) ** sympy.sympify(n)
        if not target.is_integer:
            # If the target order is not an integer, G cannot have a subgroup of that order.
            neg_q = True
        elif target <= 0:
            # Group orders must be positive integers.
            neg_q = True
        else:
            # By Lagrange's Theorem, if target does not divide |G|, no such subgroup exists.
            if G.order() % target != 0:
                neg_q = True
            else:
                # If target divides |G| and p is prime, such a subgroup always exists 
                # by Sylow's First Theorem (and its generalization to all prime powers).
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is p^n * m",
    "H_3: p is a prime number",
    "H_4: p does not divide m",
    "¬Q: G does not contain a subgroup of order p^n"
]

N_HYP = 4
NEG_Q_INDEX = 4