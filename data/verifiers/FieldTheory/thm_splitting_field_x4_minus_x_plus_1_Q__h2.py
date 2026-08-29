import sympy
from sympy import QQ
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f(x) = x^4 - x + 1 in Q polynomials",
    "¬Q: The degree of K over Q is not 24, or the Galois group is not S4"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    f = None
    K = None
    deg = None
    galois_group = None

    # Extract components from the witness
    if isinstance(witness, dict):
        f = witness.get('f', None)
        K = witness.get('K', None)
        deg = witness.get('deg', None)
        galois_group = witness.get('galois_group', None)
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 2:
            f, K = witness
        elif len(witness) >= 1:
            f = witness[0]
    else:
        if hasattr(witness, 'free_symbols') and len(witness.free_symbols) > 0:
            f = witness
        else:
            K = witness

    # H_1: f(x) == x**4 - x + 1
    h1 = False
    try:
        if f is not None:
            if isinstance(f, sympy.Poly):
                var = f.gens[0]
                expected = sympy.Poly(var**4 - var + 1, var)
                h1 = bool(f == expected)
            else:
                f_expr = sympy.sympify(f)
                syms = list(f_expr.free_symbols)
                if len(syms) == 1:
                    var = syms[0]
                    expected = var**4 - var + 1
                    h1 = bool(sympy.simplify(f_expr - expected) == 0)
                elif len(syms) == 0:
                    h1 = False
        else:
            # If f is not provided, we assume the witness is just K and H1 holds vacuously
            h1 = True
    except Exception:
        h1 = False

    # neg_Q: The degree of K over Q is not 24, or the Galois group is not S4
    neg_q = False
    try:
        if deg is None and K is not None:
            if isinstance(K, int):
                deg = K
            elif hasattr(K, 'degree'):
                if callable(K.degree):
                    deg = K.degree()
                else:
                    deg = K.degree
            elif hasattr(K, 'ext'):
                deg = K.degree()
            elif K == sympy.QQ or str(K) == 'QQ':
                deg = 1
            elif isinstance(K, sympy.Expr) or isinstance(K, sympy.Poly):
                K_expr = sympy.sympify(K)
                syms = list(K_expr.free_symbols)
                if len(syms) == 1:
                    deg = sympy.degree(K_expr, syms[0])
            elif isinstance(K, str):
                if K.lower() in ['q', 'qq', 'rationals']:
                    deg = 1

        deg_ok = False
        if deg is not None:
            if int(deg) == 24:
                deg_ok = True

        galois_ok = False
        if galois_group is not None:
            grp_str = str(galois_group).replace(' ', '')
            if grp_str in ['SymmetricGroup(4)', 'S4']:
                galois_ok = True

        if deg is not None and not deg_ok:
            neg_q = True
        if galois_group is not None and not galois_ok:
            neg_q = True

    except Exception:
        pass

    return [h1, neg_q]