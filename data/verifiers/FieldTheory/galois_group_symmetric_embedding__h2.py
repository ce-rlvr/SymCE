import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
from sympy.abc import x

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

QQ = sympy.QQ

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f_expr = witness.get('f')
            K = witness.get('K', QQ)
            n = witness.get('n', None)
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                f_expr, n = witness
                K = QQ
            elif len(witness) == 3:
                K, f_expr, n = witness
            elif len(witness) == 4:
                K, L, f_expr, n = witness
            else:
                f_expr = witness[0]
                K = QQ
                n = None
        else:
            f_expr = witness
            K = QQ
            n = None
            
        if K == 'QQ':
            K = QQ
        elif isinstance(K, str) and K.startswith('GF'):
            p = int(K[3:-1])
            K = sympy.GF(p)
            
        if isinstance(f_expr, sympy.Poly):
            poly_f = f_expr
            if n is None:
                n = poly_f.degree()
        else:
            expr = sympy.sympify(f_expr)
            free_syms = expr.free_symbols
            gen = list(free_syms)[0] if len(free_syms) == 1 else x
            poly_f = sympy.Poly(expr, gen, domain=K)
            if n is None:
                n = poly_f.degree()
                
        n = int(n)
    except Exception:
        return [False, False, False]

    # H1: K is a field
    try:
        if K == QQ:
            h1 = True
        elif hasattr(K, 'is_Field') and K.is_Field:
            h1 = True
        elif hasattr(K, 'characteristic') and K.characteristic > 0:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: L is the splitting field of f(x) over K
    try:
        h2 = poly_f.degree() >= 1
    except Exception:
        h2 = False

    # neg_Q: The action does not induce an injective homomorphism into S_n
    try:
        neg_q = False
        if h2:
            f_diff = poly_f.diff()
            gcd_f = poly_f.gcd(f_diff)
            is_separable = gcd_f.degree() == 0
            
            if not is_separable or poly_f.degree() != n:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: L is the splitting field of f(x) over K",
    "¬Q: The action of Gal(L/K) on the roots of f(x) does not induce an injective homomorphism into S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2