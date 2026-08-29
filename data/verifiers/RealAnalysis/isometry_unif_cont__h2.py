import sympy
import sympy.combinatorics.named_groups as named_groups
import sympy.matrices
from sympy import Symbol, S, Interval, limit, oo
from sympy.sets.sets import Set, FiniteSet

# Top-level setup
S3 = named_groups.SymmetricGroup(3)
S4 = named_groups.SymmetricGroup(4)
A4 = named_groups.AlternatingGroup(4)
D4 = named_groups.DihedralGroup(4)
C4 = named_groups.CyclicGroup(4)
V4 = named_groups.AlternatingGroup(4)
Z2 = named_groups.CyclicGroup(2)
Z3 = named_groups.CyclicGroup(3)
Z4 = named_groups.CyclicGroup(4)
Z6 = named_groups.CyclicGroup(6)
trivial = named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: (X, d_X) and (Y, d_Y) are metric spaces",
    "¬Q: f is not uniformly continuous on X"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # Default values
    X = S.Reals
    Y = S.Reals
    f = None
    x = Symbol('x', real=True)
    
    if isinstance(witness, dict):
        f = witness.get('f', None)
        X = witness.get('X', S.Reals)
        Y = witness.get('Y', S.Reals)
        x = witness.get('x', None)
        if x is None and f is not None:
            free = f.free_symbols
            if free:
                x = list(free)[0]
            else:
                x = Symbol('x', real=True)
    else:
        f = witness
        if hasattr(f, 'free_symbols'):
            free = f.free_symbols
            if free:
                x = list(free)[0]
            else:
                x = Symbol('x', real=True)
        else:
            return [False, False]
            
    # H1: X and Y are metric spaces. 
    try:
        h1_ok = isinstance(X, Set) and isinstance(Y, Set)
    except Exception:
        h1_ok = False
        
    # neg_Q: f is NOT uniformly continuous on X
    neg_q_ok = False
    try:
        # Check boundaries for intervals
        if hasattr(X, 'boundary'):
            boundary = X.boundary
            try:
                for pt in boundary:
                    if pt.is_finite:
                        # Check from the right
                        right_int = Interval.Ropen(pt, pt + 1)
                        if X.intersect(right_int).is_empty == False:
                            L_plus = limit(f, x, pt, dir='+')
                            if not isinstance(L_plus, sympy.Limit):
                                if not L_plus.is_finite or L_plus.__class__.__name__ == 'AccumBounds':
                                    neg_q_ok = True
                                    break
                        # Check from the left
                        left_int = Interval.Lopen(pt - 1, pt)
                        if X.intersect(left_int).is_empty == False:
                            L_minus = limit(f, x, pt, dir='-')
                            if not isinstance(L_minus, sympy.Limit):
                                if not L_minus.is_finite or L_minus.__class__.__name__ == 'AccumBounds':
                                    neg_q_ok = True
                                    break
            except TypeError:
                pass
                    
        # Check +oo
        if not neg_q_ok and hasattr(X, 'sup') and X.sup == oo:
            L_f = limit(f, x, oo)
            if not isinstance(L_f, sympy.Limit) and L_f.is_finite and L_f.__class__.__name__ != 'AccumBounds':
                pass # Converges to a finite value, so it doesn't break uniform continuity at +oo
            else:
                n = Symbol('n', real=True, positive=True)
                sequences = [
                    (n, n + 1/n),
                    (sympy.sqrt(n), sympy.sqrt(n + 1)),
                    (n**(S(1)/3), (n + 1)**(S(1)/3)),
                    (sympy.log(n), sympy.log(n + 1))
                ]
                for x_n, y_n in sequences:
                    diff_val = f.subs(x, y_n) - f.subs(x, x_n)
                    L = limit(diff_val, n, oo)
                    if not isinstance(L, sympy.Limit) and L != 0:
                        neg_q_ok = True
                        break
                        
        # Check -oo
        if not neg_q_ok and hasattr(X, 'inf') and X.inf == -oo:
            L_f = limit(f, x, -oo)
            if not isinstance(L_f, sympy.Limit) and L_f.is_finite and L_f.__class__.__name__ != 'AccumBounds':
                pass
            else:
                n = Symbol('n', real=True, positive=True)
                sequences_neg = [
                    (-n, -n - 1/n),
                    (-sympy.sqrt(n), -sympy.sqrt(n + 1)),
                    (-n**(S(1)/3), -(n + 1)**(S(1)/3)),
                    (-sympy.log(n), -sympy.log(n + 1))
                ]
                for x_n, y_n in sequences_neg:
                    diff_val = f.subs(x, y_n) - f.subs(x, x_n)
                    L = limit(diff_val, n, oo)
                    if not isinstance(L, sympy.Limit) and L != 0:
                        neg_q_ok = True
                        break
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]