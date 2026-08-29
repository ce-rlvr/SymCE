import sympy
from sympy import Poly, discriminant, sqrt
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics import PermutationGroup
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

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f, G = witness
                D_wit = None
            elif len(witness) == 3:
                f, D_wit, G = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        if not isinstance(G, PermutationGroup):
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: Let F be a field of characteristic not equal to 2
    # We assume F = QQ, which has characteristic 0 != 2.
    h1 = True

    # H_2: Let f(x) \in F[x] be a separable polynomial of degree n
    try:
        free_syms = f.free_symbols
        if len(free_syms) == 0:
            h2 = False
            n = 0
            D_actual = 0
        elif len(free_syms) > 1:
            h2 = False
            n = 0
            D_actual = 0
        else:
            var = list(free_syms)[0]
            p = Poly(f, var)
            if not all(c.is_rational for c in p.coeffs()):
                h2 = False
                n = p.degree()
                D_actual = discriminant(f, var)
            else:
                n = p.degree()
                D_actual = discriminant(f, var)
                h2 = (D_actual != 0)
    except Exception:
        h2 = False
        n = 0
        D_actual = 0

    # H_3: Let D be the discriminant of f(x)
    try:
        if D_wit is None:
            h3 = True
            D = D_actual
        else:
            h3 = (D_wit == D_actual)
            D = D_wit
    except Exception:
        h3 = False
        D = 0

    # ¬Q: The Galois group Gal(E/F) is a subgroup of the alternating group A_n 
    # if and only if D is the square of an element in F. (Must FAIL)
    try:
        # Check if G <= A_n
        if G.degree > n:
            g_in_an = False
        else:
            g_in_an = all(g.is_even for g in G.generators)
            
        # Check if D is a square in F (QQ)
        d_is_square = bool(sqrt(D).is_rational)
        
        # The conclusion is the equivalence, so its negation is the XOR
        neg_q = (g_in_an != d_is_square)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: f(x) is a separable polynomial of degree n",
    "H_3: D is the discriminant of f(x)",
    "¬Q: The equivalence (Gal(E/F) <= A_n iff D is a square in F) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3