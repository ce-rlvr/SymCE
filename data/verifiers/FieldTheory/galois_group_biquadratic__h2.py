import sympy
from sympy import sqrt, minpoly, Poly, Symbol, factor_list, simplify, Rational
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

N_HYP = 5
NEG_Q_INDEX = 5

CONDITION_LABELS = [
    "H_1: F is a field with characteristic not equal to 2",
    "H_2: There is no element x in F such that x^2 = a",
    "H_3: There is no element y in F such that y^2 = b",
    "H_4: There is no element z in F such that z^2 = ab",
    "H_5: K is the splitting field of the polynomial (x^2 - a)(x^2 - b) over F",
    "¬Q: K/F is not Galois with degree 4 and Galois group V4"
]

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
        else:
            a, b = witness
            
        def is_in_QQ(val):
            val_simp = simplify(val)
            if val_simp.is_rational:
                return True
            try:
                Rational(val_simp)
                return True
            except TypeError:
                return False

        def is_square_in_QQ(val):
            s = simplify(sqrt(simplify(val)))
            if s.is_rational:
                return True
            try:
                Rational(s)
                return True
            except TypeError:
                return False

        # H1: F is a field with char != 2. We evaluate over F = QQ.
        h1 = True
        
        # H2, H3, H4: Check that a, b, and ab are not squares in F.
        h2 = not is_square_in_QQ(a)
        h3 = not is_square_in_QQ(b)
        h4 = not is_square_in_QQ(a*b)
        
        # H5: The polynomial (x^2 - a)(x^2 - b) must be over F.
        # This requires its coefficients to be in F (QQ).
        h5 = is_in_QQ(a + b) and is_in_QQ(a * b)
        
        # Conclusion: K/F is Galois with degree 4 and Gal(K/F) == V4.
        # We compute the minimal polynomial of the primitive element r = sqrt(a) + sqrt(b).
        x = Symbol('x')
        r = simplify(sqrt(a) + sqrt(b))
        P = minpoly(r, x)
        
        if P.degree() != 4:
            neg_q = True
        else:
            coeffs = Poly(P, x).all_coeffs()
            if len(coeffs) != 5:
                neg_q = True
            else:
                _, c3, c2, c1, c0 = coeffs
                y = Symbol('y')
                # Resolvent cubic of the quartic P(x)
                resolvent = y**3 - c2*y**2 + (c3*c1 - 4*c0)*y - c3**2*c0 + 4*c2*c0 - c1**2
                factors = factor_list(resolvent)[1]
                
                # The Galois group is V4 iff the resolvent cubic splits completely over QQ
                is_v4 = all(f.degree() == 1 for f, m in factors) and sum(m for f, m in factors) == 3
                neg_q = not is_v4
                
        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(neg_q)]
    except Exception:
        return [False] * 6