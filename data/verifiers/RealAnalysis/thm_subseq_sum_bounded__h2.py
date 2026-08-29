import math
import sympy as sp
from sympy.abc import n
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

CONDITION_LABELS = [
    "H_1: (x_n) is a bounded sequence of real numbers",
    "H_2: z is a subsequential limit of the sequence (x_n + y_n)",
    "¬Q: There do not exist subsequential limits x of (x_n) and y of (y_n) such that z = x + y"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            x = witness.get('x')
            y = witness.get('y')
            z = witness.get('z')
        else:
            x, y, z = witness
            
        # Convert sympy expressions to callable functions
        if isinstance(x, sp.Expr):
            x_expr = x
            x = lambda i: float(x_expr.subs(n, i))
        if isinstance(y, sp.Expr):
            y_expr = y
            y = lambda i: float(y_expr.subs(n, i))
            
        if isinstance(z, sp.Expr):
            z = float(z)
        elif isinstance(z, str):
            z = float(z)
            
        # Case 1: Sequences are provided as periodic lists/tuples
        if isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)):
            x = list(x)
            y = list(y)
            if not x or not y:
                return [False, False, False]
            
            h1 = True  # A periodic sequence is always bounded
            
            lcm = (len(x) * len(y)) // math.gcd(len(x), len(y))
            xy = [x[i % len(x)] + y[i % len(y)] for i in range(lcm)]
            
            h2 = any(math.isclose(z, val, abs_tol=1e-5) for val in xy)
            
            q = False
            for a in set(x):
                for b in set(y):
                    if math.isclose(z, a + b, abs_tol=1e-5):
                        q = True
                        break
                if q:
                    break
            return [h1, h2, not q]
            
        # Case 2: Sequences are provided as callable functions
        elif callable(x) and callable(y):
            x_vals = []
            y_vals = []
            for i in range(1, 1001):
                try:
                    vx = float(x(i))
                    vy = float(y(i))
                    if not math.isnan(vx) and not math.isnan(vy):
                        x_vals.append(vx)
                        y_vals.append(vy)
                except Exception:
                    pass
            
            if not x_vals or not y_vals:
                return [False, False, False]
                
            h1 = max(x_vals) - min(x_vals) < 1e6
            
            xy_vals = [x_vals[i] + y_vals[i] for i in range(len(x_vals))]
            
            def is_close(a, b, tol=1e-3):
                if a == float('inf') and b == float('inf'): return True
                if a == float('-inf') and b == float('-inf'): return True
                if math.isinf(a) or math.isinf(b): return False
                return abs(a - b) < tol

            if z == float('inf'):
                h2 = max(xy_vals) > 1e5
            elif z == float('-inf'):
                h2 = min(xy_vals) < -1e5
            else:
                h2 = any(abs(z - v) < 1e-3 for v in xy_vals)
                
            x_vals_ext = x_vals.copy()
            y_vals_ext = y_vals.copy()
            if max(x_vals) > 1e5: x_vals_ext.append(float('inf'))
            if min(x_vals) < -1e5: x_vals_ext.append(float('-inf'))
            if max(y_vals) > 1e5: y_vals_ext.append(float('inf'))
            if min(y_vals) < -1e5: y_vals_ext.append(float('-inf'))
            
            q = False
            for a in x_vals_ext:
                for b in y_vals_ext:
                    if a == float('inf') and b == float('-inf'): continue
                    if a == float('-inf') and b == float('inf'): continue
                    if is_close(z, a + b, 1e-3):
                        q = True
                        break
                if q:
                    break
                    
            return [h1, h2, not q]
            
    except Exception:
        pass
        
    return [False, False, False]