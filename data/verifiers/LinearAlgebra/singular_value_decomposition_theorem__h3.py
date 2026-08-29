import sympy as sp
import math
from sympy.abc import x, y, z, t
from sympy import Matrix, eye, zeros, Rational, Integer

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            vars_list, T_expr = witness
            if isinstance(vars_list, (list, tuple)) and all(isinstance(v, sp.Symbol) for v in vars_list):
                if isinstance(T_expr, sp.Matrix):
                    h1 = len(vars_list) > 0
                    h2 = T_expr.rows > 0
                    
                    J = T_expr.jacobian(vars_list)
                    is_linear = True
                    for element in J:
                        if len(element.free_symbols) > 0:
                            is_linear = False
                            break
                    if is_linear:
                        T0 = T_expr.subs({v: 0 for v in vars_list})
                        if not all(e == 0 for e in T0):
                            is_linear = False
                            
                    if not is_linear:
                        neg_q = True
                    else:
                        witness = J
                        
        elif isinstance(witness, tuple) and len(witness) == 3:
            n, m, T_func = witness
            if isinstance(n, int) and isinstance(m, int) and callable(T_func):
                h1 = n > 0
                h2 = m > 0
                
                is_linear = True
                for i in range(5):
                    vx = [math.sin(i * n + j) for j in range(n)]
                    vy = [math.cos(i * n + j) for j in range(n)]
                    c = math.sin(i)
                    
                    try:
                        Tx = T_func(vx)
                        Ty = T_func(vy)
                        Txy = T_func([a + b for a, b in zip(vx, vy)])
                        Tcx = T_func([c * a for a in vx])
                        
                        for a, b, ab in zip(Tx, Ty, Txy):
                            if abs(a + b - ab) > 1e-6:
                                is_linear = False
                                break
                        for a, ca in zip(Tx, Tcx):
                            if abs(c * a - ca) > 1e-6:
                                is_linear = False
                                break
                    except Exception:
                        is_linear = False
                        break
                        
                if not is_linear:
                    neg_q = True
                else:
                    neg_q = False
                    
        if isinstance(witness, sp.Matrix):
            free_syms = list(witness.free_symbols)
            if len(free_syms) > 0:
                h1 = len(free_syms) > 0
                h2 = witness.rows > 0
                
                J = witness.jacobian(free_syms)
                is_linear = True
                for element in J:
                    if len(element.free_symbols) > 0:
                        is_linear = False
                        break
                if is_linear:
                    T0 = witness.subs({v: 0 for v in free_syms})
                    if not all(e == 0 for e in T0):
                        is_linear = False
                        
                if not is_linear:
                    neg_q = True
                else:
                    witness = J
                    free_syms = []
            
            if len(free_syms) == 0:
                M = witness
                if not h1: h1 = M.cols > 0
                if not h2: h2 = M.rows > 0
                
                is_Q = all(e.is_rational == True for e in M)
                has_svd = True
                if is_Q:
                    try:
                        svs = M.singular_values()
                        for sv in svs:
                            if sv.is_rational != True:
                                has_svd = False
                                break
                        
                        if has_svd:
                            MTM = M.T * M
                            eigenvects = MTM.eigenvects()
                            for val, mult, basis in eigenvects:
                                ortho_basis = sp.GramSchmidt(basis)
                                for v in ortho_basis:
                                    norm_sq = sum(x**2 for x in v)
                                    if sp.sqrt(norm_sq).is_rational != True:
                                        has_svd = False
                                        break
                                if not has_svd:
                                    break
                    except Exception:
                        has_svd = False
                neg_q = not has_svd

    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space",
    "H_2: W is a finite-dimensional inner product space over the same field as V",
    "¬Q: There do not exist orthonormal bases of V and W such that the matrix representation of T is diagonal with non-negative real entries"
]

N_HYP = 2
NEG_Q_INDEX = 2