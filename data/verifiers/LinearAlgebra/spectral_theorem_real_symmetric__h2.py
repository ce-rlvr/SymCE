import sympy as sp
from sympy import Matrix, eye, zeros
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional real inner product space",
    "¬Q: T has an orthonormal basis of eigenvectors but is not a self-adjoint operator"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        T = None
        basis = None
        n = 0
        
        if isinstance(witness, tuple):
            if len(witness) == 3:
                T_exprs, vars_sym, basis = witness
                n = len(basis)
                def T(v):
                    subs = {vars_sym[i]: float(v[i]) for i in range(len(vars_sym))}
                    return [float(expr.subs(subs)) for expr in T_exprs]
            elif len(witness) == 2:
                a, b = witness
                if isinstance(a, list) and len(a) > 0 and hasattr(a[0], 'free_symbols'):
                    T_exprs, vars_sym = a, b
                    n = len(T_exprs)
                    basis = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
                    def T(v):
                        subs = {vars_sym[i]: float(v[i]) for i in range(len(vars_sym))}
                        return [float(expr.subs(subs)) for expr in T_exprs]
                else:
                    T_obj, basis = a, b
                    n = len(basis)
                    if hasattr(T_obj, 'shape') and hasattr(T_obj, 'inv'):
                        def T(v):
                            res = T_obj * sp.Matrix(v)
                            return [float(res[i]) for i in range(len(v))]
                    else:
                        def T(v):
                            return [float(x) for x in T_obj(v)]
        elif isinstance(witness, list) and len(witness) > 0 and hasattr(witness[0], 'free_symbols'):
            T_exprs = witness
            vars_sym = list(set().union(*[expr.free_symbols for expr in T_exprs]))
            vars_sym = sorted(vars_sym, key=lambda s: s.name)
            n = len(T_exprs)
            basis = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
            def T(v):
                subs = {vars_sym[i]: float(v[i]) for i in range(min(len(vars_sym), len(v)))}
                return [float(expr.subs(subs)) for expr in T_exprs]
                
        if T is None or basis is None or n == 0:
            return [False, False]
            
        # H1: V is a finite-dimensional real inner product space
        h1 = True
        for v in basis:
            if len(v) != n:
                h1 = False
                break
        if not h1:
            return [False, False]
            
        # Check if basis is orthonormal
        is_orthonormal = True
        for i in range(n):
            for j in range(n):
                dot = sum(float(basis[i][k]) * float(basis[j][k]) for k in range(n))
                if i == j:
                    if abs(dot - 1) > 1e-5: is_orthonormal = False
                else:
                    if abs(dot) > 1e-5: is_orthonormal = False
                    
        # Check if basis consists of eigenvectors of T
        is_eigenbasis = True
        for v in basis:
            v_float = [float(x) for x in v]
            Tv = T(v_float)
            lam = sum(Tv[k] * v_float[k] for k in range(n))
            for k in range(n):
                if abs(Tv[k] - lam * v_float[k]) > 1e-5:
                    is_eigenbasis = False
                    break
            if not is_eigenbasis:
                break
                
        has_orthonormal_eigenbasis = is_orthonormal and is_eigenbasis
        
        # Check if T is self-adjoint
        # We test this by checking <T(x), y> == <x, T(y)> on a set of test vectors.
        is_self_adjoint = True
        test_vectors = []
        for i in range(n):
            v = [0.0]*n
            v[i] = 1.0
            test_vectors.append(v)
            v2 = [0.0]*n
            v2[i] = 2.0
            test_vectors.append(v2)
            for j in range(i+1, n):
                v3 = [0.0]*n
                v3[i] = 1.0
                v3[j] = 1.0
                test_vectors.append(v3)
                v4 = [0.0]*n
                v4[i] = 1.5
                v4[j] = -0.5
                test_vectors.append(v4)
                
        v5 = [math.sin(i+1) for i in range(n)]
        v6 = [math.cos(i+1) for i in range(n)]
        test_vectors.extend([v5, v6])
                
        for x in test_vectors:
            for y in test_vectors:
                Tx = T(x)
                Ty = T(y)
                dot_Tx_y = sum(Tx[k] * y[k] for k in range(n))
                dot_x_Ty = sum(x[k] * Ty[k] for k in range(n))
                if abs(dot_Tx_y - dot_x_Ty) > 1e-5:
                    is_self_adjoint = False
                    break
            if not is_self_adjoint:
                break
                
        # The conclusion is an equivalence: T has orthonormal eigenbasis <=> T is self-adjoint.
        # Since any self-adjoint operator on a finite-dimensional real inner product space 
        # is linear and has an orthonormal eigenbasis, the only way the equivalence fails 
        # is if T has an orthonormal eigenbasis but is NOT self-adjoint (which implies T is non-linear).
        neg_q = has_orthonormal_eigenbasis and not is_self_adjoint
        
        return [h1, neg_q]
    except Exception:
        return [False, False]