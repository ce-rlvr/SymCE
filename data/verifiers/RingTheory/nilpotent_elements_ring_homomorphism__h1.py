import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1, h2, neg_q = False, False, False
    
    # 1. Try object with custom methods
    try:
        if hasattr(witness, 'is_homomorphism') and hasattr(witness, 'x_is_nilpotent') and hasattr(witness, 'fx_is_nilpotent'):
            h1 = bool(witness.is_homomorphism())
            h2 = bool(witness.x_is_nilpotent())
            neg_q = not bool(witness.fx_is_nilpotent())
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Try dictionary format with explicit ring operations
    try:
        if isinstance(witness, dict) and 'R' in witness and 'S' in witness:
            R = witness['R']
            S = witness['S']
            add_R = witness['add_R']
            mul_R = witness['mul_R']
            zero_R = witness['zero_R']
            add_S = witness['add_S']
            mul_S = witness['mul_S']
            zero_S = witness['zero_S']
            f = witness['f']
            x = witness['x']
            
            h1 = True
            for a in R:
                for b in R:
                    if f(add_R(a, b)) != add_S(f(a), f(b)):
                        h1 = False
                    if f(mul_R(a, b)) != mul_S(f(a), f(b)):
                        h1 = False
                        
            h2 = False
            curr = x
            for _ in range(len(R) + 1):
                if curr == zero_R:
                    h2 = True
                    break
                curr = mul_R(curr, x)
                
            fx = f(x)
            is_nil_fx = False
            curr_S = fx
            for _ in range(len(S) + 1):
                if curr_S == zero_S:
                    is_nil_fx = True
                    break
                curr_S = mul_S(curr_S, fx)
            neg_q = not is_nil_fx
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Try (n, m, f, x) format for Z/nZ -> Z/mZ
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            n, m, f, x = witness
            if isinstance(n, int) and isinstance(m, int):
                h1 = True
                for a in range(n):
                    for b in range(n):
                        fa = f(a) if callable(f) else f[a]
                        fb = f(b) if callable(f) else f[b]
                        fab_add = f((a+b)%n) if callable(f) else f[(a+b)%n]
                        fab_mul = f((a*b)%n) if callable(f) else f[(a*b)%n]
                        if fab_add != (fa + fb) % m:
                            h1 = False
                        if fab_mul != (fa * fb) % m:
                            h1 = False
                
                h2 = False
                curr = x % n
                for _ in range(n):
                    if curr == 0:
                        h2 = True
                        break
                    curr = (curr * x) % n
                    
                fx = f(x) if callable(f) else f[x]
                fx = fx % m
                is_nil_fx = False
                curr_fx = fx
                for _ in range(m):
                    if curr_fx == 0:
                        is_nil_fx = True
                        break
                    curr_fx = (curr_fx * fx) % m
                neg_q = not is_nil_fx
                return [h1, h2, neg_q]
    except Exception:
        pass

    # 4. Try (f, x) format for SymPy matrices
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            f, x = witness
            if hasattr(x, 'is_nilpotent'):
                h2 = bool(x.is_nilpotent())
                fx = f(x)
                neg_q = not bool(fx.is_nilpotent())
                
                h1 = True
                n = x.shape[0]
                I = eye(n)
                Z = zeros(n, n)
                tests = [x, x*x, x+x, I, Z]
                for a in tests:
                    for b in tests:
                        if sp.simplify(f(a + b) - (f(a) + f(b))) != zeros(*fx.shape):
                            h1 = False
                        if sp.simplify(f(a * b) - (f(a) * f(b))) != zeros(*fx.shape):
                            h1 = False
                return [h1, h2, neg_q]
    except Exception:
        pass

    # 5. Try (f, x) format for general expressions
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            f, x = witness
            h2 = False
            for k in range(1, 20):
                if x**k == 0:
                    h2 = True
                    break
            fx = f(x)
            is_nil_fx = False
            for k in range(1, 20):
                if fx**k == 0:
                    is_nil_fx = True
                    break
            neg_q = not is_nil_fx
            
            h1 = True
            tests = [x, x*x, x+x, 0, 1]
            for a in tests:
                for b in tests:
                    if f(a + b) != f(a) + f(b):
                        h1 = False
                    if f(a * b) != f(a) * f(b):
                        h1 = False
            return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: f: R -> S is a ring homomorphism",
    "H_2: x is a nilpotent element in R",
    "¬Q: f(x) is not a nilpotent element in S"
]

N_HYP = 2
NEG_Q_INDEX = 2