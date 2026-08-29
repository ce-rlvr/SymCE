import math
from sympy import Interval, lambdify, Piecewise, Symbol
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def check_H1(witness):
    """
    Check if U is an open, bounded, and convex subset of R^n.
    We restrict to 1D intervals for simplicity, which are valid subsets of R^1.
    """
    try:
        U = witness.get('U')
        if not hasattr(U, 'is_Interval'):
            return False
        if not U.is_Interval:
            return False
        if not (U.left_open and U.right_open):
            return False
        if not U.is_bounded:
            return False
        return True
    except Exception:
        return False

def check_W1inf(witness):
    """
    Check if f is in W^{1,infty}(U).
    We do this numerically by checking if the almost-everywhere representative
    has a bounded difference quotient.
    """
    try:
        U = witness['U']
        f = witness['f']
        if 'vars' in witness:
            x = witness['vars'][0]
        else:
            free = list(f.free_symbols)
            if not free:
                x = Symbol('x')
            else:
                x = free[0]
        
        a, b = float(U.inf), float(U.sup)
        
        f_lam = lambdify(x, f, modules=['math', 'sympy'])
        
        def get_max_diff(N):
            offset = math.sqrt(2) / 2  # irrational offset to avoid simple rationals
            pts = [a + (i + offset) / N * (b - a) for i in range(N)]
            vals = []
            for p in pts:
                v = float(f_lam(p))
                if math.isnan(v) or math.isinf(v):
                    raise ValueError("nan or inf")
                vals.append(v)
            max_diff = 0
            for i in range(N - 1):
                diff = abs(vals[i+1] - vals[i]) / (pts[i+1] - pts[i])
                if diff > max_diff:
                    max_diff = diff
            return max_diff
            
        md_100 = get_max_diff(100)
        md_1000 = get_max_diff(1000)
        
        # If the max difference scales linearly with N, it's a jump discontinuity
        if md_1000 > 3 * md_100 and md_1000 > 10:
            return False
            
        # If the derivative is unbounded
        if md_1000 > 1e6:
            return False
            
        return True
    except Exception:
        return False

def check_not_Lipschitz(witness):
    """
    Check if f is NOT globally Lipschitz continuous on U.
    """
    try:
        f = witness['f']
        U = witness['U']
        if 'vars' in witness:
            x = witness['vars'][0]
        else:
            free = list(f.free_symbols)
            if not free:
                x = Symbol('x')
            else:
                x = free[0]
        
        # Check explicit points if provided by the witness
        if 'x1' in witness and 'x2' in witness:
            x1 = float(witness['x1'])
            x2 = float(witness['x2'])
            if x1 > U.inf and x1 < U.sup and x2 > U.inf and x2 < U.sup:
                v1 = float(f.subs(x, x1))
                v2 = float(f.subs(x, x2))
                if math.isnan(v1) or math.isnan(v2) or math.isinf(v1) or math.isinf(v2):
                    return True
                if abs(x1 - x2) < 1e-15:
                    if abs(v1 - v2) > 1e-7:
                        return True
                else:
                    if abs(v1 - v2) / abs(x1 - x2) > 1e6:
                        return True
                        
        # Auto-detect discontinuities in Piecewise functions
        points = []
        if f.func.__name__ == 'Piecewise':
            for expr, cond in f.args:
                for atom in cond.atoms():
                    if getattr(atom, 'is_Relational', False):
                        if atom.lhs == x and atom.rhs.is_number:
                            points.append(float(atom.rhs))
                        elif atom.rhs == x and atom.lhs.is_number:
                            points.append(float(atom.lhs))
                            
        for p in points:
            if p > U.inf and p < U.sup:
                v1 = float(f.subs(x, p))
                if math.isnan(v1) or math.isinf(v1):
                    return True
                try:
                    v2 = float(f.subs(x, p + 1e-7))
                    if math.isnan(v2) or math.isinf(v2) or abs(v1 - v2) / 1e-7 > 1e5:
                        return True
                except Exception:
                    pass
                try:
                    v3 = float(f.subs(x, p - 1e-7))
                    if math.isnan(v3) or math.isinf(v3) or abs(v1 - v3) / 1e-7 > 1e5:
                        return True
                except Exception:
                    pass
                    
        return False
    except Exception:
        return False

def conditions(witness):
    H1 = check_H1(witness)
    
    is_W1inf = check_W1inf(witness)
    is_not_lip = check_not_Lipschitz(witness)
    
    # The conclusion is an iff statement. Since globally Lipschitz implies W^{1,infty}
    # is always true, the only way the iff fails is if f is in W^{1,infty} but NOT globally Lipschitz.
    neg_Q = is_W1inf and is_not_lip
    
    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: U is an open, bounded, and convex subset of R^n",
    "¬Q: f is in W^{1,infty}(U) but is not globally Lipschitz continuous on U"
]

N_HYP = 1
NEG_Q_INDEX = 1