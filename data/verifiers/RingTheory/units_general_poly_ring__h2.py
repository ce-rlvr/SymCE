import sympy as sp
from sympy import eye, zeros
from sympy.abc import x, y, z

# Standard bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def strip_zeros(coeffs):
    res = list(coeffs)
    while len(res) > 1:
        last = res[-1]
        is_zero = False
        if hasattr(last, 'is_Matrix') and last.is_Matrix:
            if sp.simplify(last) == sp.zeros(*last.shape):
                is_zero = True
        else:
            try:
                if sp.simplify(last) == 0:
                    is_zero = True
            except:
                if last == 0:
                    is_zero = True
        if is_zero:
            res.pop()
        else:
            break
    return res

def poly_mul(A, B):
    if not A or not B:
        return []
    n = len(A)
    m = len(B)
    C = [0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            if isinstance(C[i+j], int) and C[i+j] == 0:
                C[i+j] = A[i] * B[j]
            else:
                C[i+j] = C[i+j] + A[i] * B[j]
    return C

def is_unit(a, a_inv=None):
    if a_inv is not None:
        try:
            prod1 = a * a_inv
            prod2 = a_inv * a
            if hasattr(prod1, 'is_Matrix') and prod1.is_Matrix:
                I = sp.eye(prod1.shape[0])
                if sp.simplify(prod1 - I) == sp.zeros(*prod1.shape) and sp.simplify(prod2 - I) == sp.zeros(*prod2.shape):
                    return True
            else:
                try:
                    if sp.simplify(prod1 - 1) == 0 and sp.simplify(prod2 - 1) == 0:
                        return True
                except:
                    if prod1 == 1 and prod2 == 1:
                        return True
        except:
            pass

    if hasattr(a, 'is_Matrix') and a.is_Matrix:
        try:
            d = a.det()
            if d == 1 or d == -1: return True
            a.inv()
            return True
        except:
            return False
    else:
        try:
            if sp.simplify(a - 1) == 0 or sp.simplify(a + 1) == 0: return True
        except:
            if a == 1 or a == -1: return True
        try:
            return sp.simplify(1 / a).is_number
        except:
            return False

def is_nilpotent(a):
    if hasattr(a, 'is_Matrix') and a.is_Matrix:
        n = a.shape[0]
        try:
            return sp.simplify(a**n) == sp.zeros(n, n)
        except:
            return False
    else:
        try:
            if sp.simplify(a) == 0: return True
        except:
            if a == 0: return True
        try:
            curr = a
            for _ in range(10):
                curr = curr * a
                try:
                    if sp.simplify(curr) == 0: return True
                except:
                    if curr == 0: return True
            return False
        except:
            return False

def check_P(f_coeffs, g_coeffs=None):
    if not f_coeffs:
        return False
    
    f_coeffs = strip_zeros(f_coeffs)
    
    if g_coeffs is not None and len(g_coeffs) > 0:
        g_coeffs = strip_zeros(g_coeffs)
        try:
            fg = poly_mul(f_coeffs, g_coeffs)
            gf = poly_mul(g_coeffs, f_coeffs)
            
            def is_identity(prod):
                if not prod: return False
                prod = strip_zeros(prod)
                first = prod[0]
                if hasattr(first, 'is_Matrix') and first.is_Matrix:
                    I = sp.eye(first.shape[0])
                    if sp.simplify(first - I) != sp.zeros(*first.shape): return False
                    if len(prod) > 1: return False
                else:
                    try:
                        if sp.simplify(first - 1) != 0: return False
                    except:
                        if first != 1: return False
                    if len(prod) > 1: return False
                return True
                
            if is_identity(fg) and is_identity(gf):
                return True
        except:
            pass
            
    if hasattr(f_coeffs[0], 'is_Matrix') and f_coeffs[0].is_Matrix:
        try:
            x_sym = sp.Symbol('x')
            n = f_coeffs[0].shape[0]
            f_x = sp.zeros(n, n)
            for i, c in enumerate(f_coeffs):
                f_x += c * (x_sym**i)
            d = f_x.det()
            d = sp.expand(d)
            if x_sym in d.free_symbols:
                return False
            if d == 1 or d == -1:
                return True
            if d != 0:
                f_coeffs[0].inv()
                return True
        except:
            pass
        return False
    else:
        if len(f_coeffs) == 1:
            return is_unit(f_coeffs[0])
        return False

def check_Q(f_coeffs, a0_inv=None):
    if not f_coeffs:
        return False
    f_coeffs = strip_zeros(f_coeffs)
    a_0 = f_coeffs[0]
    if not is_unit(a_0, a0_inv):
        return False
    for a_i in f_coeffs[1:]:
        if not is_nilpotent(a_i):
            return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f_coeffs = witness.get('f', [])
            g_coeffs = witness.get('g', None)
            a0_inv = witness.get('a0_inv', None)
        elif isinstance(witness, tuple) and len(witness) == 2:
            f_coeffs, g_coeffs = witness
            a0_inv = None
        else:
            f_coeffs = witness
            g_coeffs = None
            a0_inv = None
            
        if not isinstance(f_coeffs, list) or not f_coeffs:
            return [False, False]
            
        f_coeffs = strip_zeros(f_coeffs)
        
        # H1: R is a commutative ring with identity
        h1 = True
        for c in f_coeffs:
            if hasattr(c, 'is_Matrix') and c.is_Matrix:
                if c.shape != (1, 1):
                    h1 = False
                    break
            elif hasattr(c, 'is_commutative') and c.is_commutative is False:
                h1 = False
                break
                
        if h1:
            for i in range(len(f_coeffs)):
                for j in range(i, len(f_coeffs)):
                    try:
                        diff = f_coeffs[i] * f_coeffs[j] - f_coeffs[j] * f_coeffs[i]
                        if hasattr(diff, 'is_Matrix') and diff.is_Matrix:
                            if sp.simplify(diff) != sp.zeros(*diff.shape):
                                h1 = False
                                break
                        else:
                            try:
                                if sp.simplify(diff) != 0:
                                    h1 = False
                                    break
                            except:
                                if diff != 0:
                                    h1 = False
                                    break
                    except:
                        pass
                if not h1:
                    break
                    
        # neg_Q: P != Q (The conclusion is an iff statement, so it fails when P != Q)
        P = check_P(f_coeffs, g_coeffs)
        Q = check_Q(f_coeffs, a0_inv)
        neg_q = (P != Q)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: The conclusion fails (f(x) is a unit iff a_0 is a unit and a_1..a_n are nilpotent is FALSE)"
]

N_HYP = 1
NEG_Q_INDEX = 1