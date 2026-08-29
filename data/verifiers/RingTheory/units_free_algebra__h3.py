import sympy
import sympy.combinatorics
import sympy.matrices

# Top-level setup
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

def is_in_kX(expr, X_set):
    if hasattr(expr, 'free_symbols'):
        if not expr.free_symbols.issubset(X_set):
            return False
        n, d = sympy.fraction(expr)
        if len(d.free_symbols) > 0:
            return False
        return True
    elif isinstance(expr, (int, float, sympy.Integer, sympy.Float, sympy.Rational)):
        return True
    return False

def conditions(witness):
    # H_1: k is a field
    try:
        k = witness.get('k')
        H1 = bool(k.is_Field)
    except Exception:
        H1 = False

    # H_2: X is a set of variables
    try:
        X = witness.get('X')
        H2 = isinstance(X, (list, set, tuple)) and all(isinstance(x, sympy.Symbol) for x in X)
    except Exception:
        H2 = False

    # H_3: u \in k<X>
    try:
        u = witness.get('u')
        X_set = set(witness.get('X', []))
        H3 = is_in_kX(u, X_set)
    except Exception:
        H3 = False

    # ¬Q: u is a unit in k<X> iff u is a non-zero scalar in k FAILS
    try:
        u = witness.get('u')
        X_set = set(witness.get('X', []))
        
        is_nonzero_scalar = False
        if hasattr(u, 'free_symbols'):
            if len(u.free_symbols) == 0 and sympy.simplify(u) != 0:
                is_nonzero_scalar = True
        else:
            if u != 0 and isinstance(u, (int, float, sympy.Integer, sympy.Float, sympy.Rational)):
                is_nonzero_scalar = True

        is_unit = False
        if is_nonzero_scalar:
            is_unit = True
        elif 'v' in witness:
            v = witness['v']
            if is_in_kX(v, X_set):
                if sympy.expand(u * v) == 1 and sympy.expand(v * u) == 1:
                    is_unit = True
        
        Q = (is_unit == is_nonzero_scalar)
        neg_Q = not Q
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: k is a field",
    "H_2: X is a set of variables",
    "H_3: u \\in k\\langle X \\rangle",
    "¬Q: u is a unit in k\\langle X \\rangle iff u is a non-zero scalar in k FAILS"
]

N_HYP = 3
NEG_Q_INDEX = 3