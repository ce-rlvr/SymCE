import sympy
import sympy.combinatorics
import sympy.matrices
from sympy import Symbol, Poly, fraction, diff, factor_list, degree
from sympy.ntheory import isprime

# Top-level setup for standard algebra objects
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    Expects witness to be a tuple: (p, t, X, P1, P2)
    where:
      - p is a prime integer (characteristic of the base field K)
      - t is a SymPy Symbol (transcendental element, K = GF(p)(t))
      - X is a SymPy Symbol (the variable for the polynomials)
      - P1 is an irreducible polynomial in X over K defining L_1
      - P2 is an irreducible polynomial in X over K defining L_2
    """
    try:
        p, t, X, P1, P2 = witness
    except Exception:
        return [False, False, False, False]

    # H_1: E is a field extension of K
    # We verify that K = GF(p)(t) is a valid field setup.
    # (The existence of a common extension E for any two valid extensions L1, L2 is mathematically guaranteed).
    try:
        h1 = isprime(p) and isinstance(t, sympy.Symbol) and isinstance(X, sympy.Symbol)
    except Exception:
        h1 = False

    def is_irred(P):
        try:
            num, den = fraction(P.cancel())
            if degree(den, X) > 0:
                return False
            poly_num = Poly(num, X, t, domain=f'GF({p})')
            expr_num = poly_num.as_expr()
            if degree(expr_num, X) < 1:
                return False
            facs = factor_list(expr_num, modulus=p)
            x_factors = [f for f, exp in facs[1] if degree(f, X) > 0]
            if len(x_factors) == 1:
                for f, exp in facs[1]:
                    if f == x_factors[0] and exp == 1:
                        return True
            return False
        except Exception:
            return False

    # H_2: L_1 and L_2 are subfields of E containing K
    # We verify that P1 and P2 define valid field extensions of K.
    try:
        h2 = is_irred(P1) and is_irred(P2)
    except Exception:
        h2 = False

    # H_3: L_1/K is a separable extension
    try:
        dP1 = diff(P1, X)
        num1, _ = fraction(dP1.cancel())
        poly_num1 = Poly(num1, X, t, domain=f'GF({p})')
        l1_insep = poly_num1.is_zero
        h3 = not l1_insep
    except Exception:
        h3 = False
        l1_insep = False

    # ¬Q: The compositum L_1 L_2 is not a separable extension of K
    # The compositum of L_1 and L_2 is inseparable over K if and only if 
    # L_1/K is inseparable OR L_2/K is inseparable.
    try:
        dP2 = diff(P2, X)
        num2, _ = fraction(dP2.cancel())
        poly_num2 = Poly(num2, X, t, domain=f'GF({p})')
        l2_insep = poly_num2.is_zero
        
        neg_q = l1_insep or l2_insep
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: E is a field extension of K",
    "H_2: L_1 and L_2 are subfields of E containing K",
    "H_3: L_1/K is a separable extension",
    "¬Q: The compositum L_1 L_2 is not a separable extension of K"
]

N_HYP = 3
NEG_Q_INDEX = 3