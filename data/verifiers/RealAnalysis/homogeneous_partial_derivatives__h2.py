import sympy
from sympy import symbols, simplify, Derivative
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
x, y, z = symbols('x y z', real=True)
t = symbols('t', positive=True)
k = symbols('k', real=True)

# Standard algebra objects
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
    "H_1: f is differentiable on R^n \\ {0}",
    "¬Q: There exists i such that df/dx_i(tx) != t^{k-1} df/dx_i(x) for some x != 0, t > 0"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            f, k_val = witness
            k_vals_to_test = [k_val]
        else:
            f = witness
            # If k is not provided, the conclusion fails if there is ANY k for which it fails.
            # We test a few arbitrary values to find a counterexample.
            k_vals_to_test = [0, 1, 2, 3, 42]
            
        if not hasattr(f, 'free_symbols'):
            f = sympy.sympify(f)
            
        vars_f = [v for v in f.free_symbols if v not in (t, k)]
        if not vars_f:
            vars_f = [x]
            
        # H_1: f is differentiable
        h1_ok = True
        for v in vars_f:
            df = f.diff(v)
            if df.has(Derivative):
                h1_ok = False
                break
                
    except Exception:
        h1_ok = False

    try:
        neg_q = False
        for k_val in k_vals_to_test:
            fails_for_this_k = False
            for v in vars_f:
                df = f.diff(v)
                subs_dict = {var: t*var for var in vars_f}
                df_tx = df.subs(subs_dict)
                
                diff_expr = simplify(df_tx - (t**(k_val - 1)) * df)
                if diff_expr != 0:
                    if not diff_expr.equals(0):
                        fails_for_this_k = True
                        break
            if fails_for_this_k:
                neg_q = True
                break
                
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]