import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

class InnerProductSpaceOperator:
    """
    Represents a linear operator on an inner product space with a countable basis e_0, e_1, ...
    dim: integer or sympy.oo
    ip: function(n, m) returning <e_n, e_m>
    action: function(n) returning a dict {k: coeff} representing T(e_n) = sum coeff * e_k
    """
    def __init__(self, dim, ip_func, action_func):
        self.dim = dim
        self.ip = ip_func
        self.action = action_func

def _poly_ip(n, m):
    return sympy.Rational(1, n + m + 1)

def _poly_deriv_action(n):
    if n == 0:
        return {}
    return {n - 1: n}

PolynomialDerivative = InnerProductSpaceOperator(sympy.oo, _poly_ip, _poly_deriv_action)

def _shift_ip(n, m):
    return 1 if n == m else 0

def _shift_action(n):
    return {n + 1: 1}

RightShift = InnerProductSpaceOperator(sympy.oo, _shift_ip, _shift_action)

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "¬Q: T does not have a unique adjoint"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    if isinstance(witness, sympy.Matrix):
        # Finite dimensional matrices always have a unique adjoint
        return [True, False]
        
    if isinstance(witness, InnerProductSpaceOperator):
        dim = witness.dim
        ip = witness.ip
        T_action = witness.action
    elif isinstance(witness, tuple) and len(witness) == 3:
        dim, ip, T_action = witness
    else:
        return [False, False]
        
    try:
        test_dim = min(3, dim if isinstance(dim, int) else 3)
        h1 = True
        
        # Check if T_action returns a valid dictionary for basis elements
        for n in range(test_dim):
            res = T_action(n)
            if not isinstance(res, dict):
                h1 = False
                break
                
        # Check if ip is a valid inner product (symmetric and positive definite)
        is_inner_product = True
        for n in range(test_dim):
            for m in range(test_dim):
                diff = sympy.simplify(ip(n, m) - ip(m, n))
                if diff != 0:
                    try:
                        if abs(float(diff)) > 1e-9:
                            is_inner_product = False
                    except Exception:
                        is_inner_product = False
        
        if is_inner_product:
            M_test = sympy.Matrix([[ip(n, k) for k in range(test_dim)] for n in range(test_dim)])
            for i in range(1, test_dim + 1):
                det_val = M_test[:i, :i].det()
                try:
                    if float(det_val) <= 0:
                        is_inner_product = False
                        break
                except Exception:
                    pass
                    
        if not is_inner_product:
            h1 = False
            
        if not h1:
            return [False, False]
            
        # Check if the adjoint exists
        if isinstance(dim, int):
            neg_q = False
        else:
            adjoint_exists_for_all = True
            # We check if T*(e_m) exists for the first few basis vectors
            for m in range(3):
                def L(n, m_val=m):
                    t_n = T_action(n)
                    return sum(coeff * ip(k, m_val) for k, coeff in t_n.items())
                
                adjoint_exists_for_m = False
                # Try to find a finite linear combination for T*(e_m)
                for D in range(1, 15):
                    M = sympy.Matrix([[ip(n, k) for k in range(D+1)] for n in range(D+1)])
                    b = sympy.Matrix([L(n, m) for n in range(D+1)])
                    try:
                        c = M.LUsolve(b)
                        holds = True
                        # Verify the solution holds for subsequent basis vectors
                        for n in range(D+1, D+4):
                            expected = L(n, m)
                            actual = sum(c[k] * ip(n, k) for k in range(D+1))
                            diff = sympy.simplify(expected - actual)
                            if diff != 0:
                                try:
                                    if abs(float(diff)) > 1e-9:
                                        holds = False
                                        break
                                except Exception:
                                    holds = False
                                    break
                        if holds:
                            adjoint_exists_for_m = True
                            break
                    except Exception:
                        pass
                
                if not adjoint_exists_for_m:
                    adjoint_exists_for_all = False
                    break
            
            neg_q = not adjoint_exists_for_all
            
        return [h1, neg_q]
    except Exception:
        return [False, False]