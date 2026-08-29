import sympy
from sympy import isprime, ZZ, QQ
import sympy.combinatorics
import sympy.matrices

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

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: E is an elliptic curve defined over K",
    "H_2: p is a prime number not equal to the characteristic of K",
    "¬Q: The absolute Galois group does not act on the p-torsion subgroup inducing a continuous group homomorphism to GL_2(F_p)"
]

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            E, p, K = witness
        elif isinstance(witness, dict):
            E = witness.get('E')
            p = witness.get('p')
            K = witness.get('K')
        else:
            E = getattr(witness, 'E', None)
            p = getattr(witness, 'p', None)
            K = getattr(witness, 'K', None)
            
        if K is None and hasattr(E, 'domain'):
            K = E.domain
            
        h1 = False
        if E is not None:
            if hasattr(E, 'discriminant'):
                try:
                    disc = E.discriminant()
                    h1 = (disc != 0)
                except Exception:
                    pass
            if not h1 and type(E).__name__ == 'EllipticCurve':
                h1 = True
            if not h1 and isinstance(E, (tuple, list)):
                if len(E) == 5:
                    a1, a2, a3, a4, a6 = E
                    b2 = a1**2 + 4*a2
                    b4 = a1*a3 + 2*a4
                    b6 = a3**2 + 4*a6
                    b8 = a1**2*a6 + 4*a2*a6 - a1*a3*a4 + a2*a3**2 - a4**2
                    disc = -b2**2*b8 - 8*b4**3 - 27*b6**2 + 9*b2*b4*b6
                    if disc != 0:
                        h1 = True
                elif len(E) == 2:
                    a, b = E
                    disc = -16 * (4*a**3 + 27*b**2)
                    if disc != 0:
                        h1 = True

        h2 = False
        if p is not None and isprime(p):
            try:
                char_K = K.characteristic()
            except AttributeError:
                char_K = 0
            if p != char_K:
                h2 = True

        neg_q = True
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]