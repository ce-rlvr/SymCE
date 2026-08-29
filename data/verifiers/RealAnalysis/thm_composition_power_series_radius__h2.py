import sympy
import math

# Top-level setup
n = sympy.Symbol('n', integer=True, nonnegative=True)

def eval_seq(seq, i):
    if callable(seq):
        return seq(i)
    elif hasattr(seq, 'subs'):
        val = seq.subs(n, i)
        if hasattr(val, 'is_Integer') and val.is_Integer:
            return int(val)
        return val
    elif isinstance(seq, (list, tuple)):
        if i < len(seq):
            return seq[i]
        else:
            return 0
    else:
        raise ValueError("Unknown sequence format")

def safe_root(val, i):
    if val == 0:
        return 0.0
    try:
        if hasattr(val, 'is_Integer') and val.is_Integer:
            val = int(val)
            
        if isinstance(val, int):
            return math.exp(math.log(abs(val)) / i)
            
        fval = float(abs(val))
        return fval**(1/i)
    except OverflowError:
        try:
            return float(sympy.Abs(val)**(1/sympy.Integer(i)))
        except Exception:
            return float('inf')
    except Exception:
        return 0.0

def get_limsup_envelope(vals, start=10, end=80, step=5):
    A = []
    for k in range(start, end, step):
        window = []
        for i in range(k, k+step):
            if i < len(vals) and vals[i] != 0:
                window.append(safe_root(vals[i], i))
            else:
                window.append(0.0)
        A.append(max(window))
    return A

def is_R_positive(seq):
    if hasattr(seq, 'free_symbols') and n in seq.free_symbols:
        try:
            L = sympy.limit(sympy.Abs(seq)**(1/n), n, sympy.oo)
            if L == sympy.oo:
                return False
            return True
        except Exception:
            pass
    
    vals = []
    for i in range(80):
        try:
            val = eval_seq(seq, i)
            if hasattr(val, 'is_finite') and not val.is_finite:
                val = 0
            vals.append(val)
        except Exception:
            vals.append(0)
            
    A = get_limsup_envelope(vals, 10, 80, 5)
    if all(a == 0 for a in A):
        return True
        
    mid = len(A) // 2
    if math.isinf(A[-1]) or math.isinf(A[mid]):
        return False
        
    rel_growth = (A[-1] - A[mid]) / (A[-1] + 1e-9)
    
    is_r_zero = (rel_growth > 0.1 and A[-1] > 1.5)
    return not is_r_zero

def get_c_seq(a, b, M):
    a_vals = []
    for i in range(M):
        try:
            val = eval_seq(a, i)
            if hasattr(val, 'is_finite') and not val.is_finite:
                val = 0
            if isinstance(val, float) and val.is_integer():
                val = int(val)
            a_vals.append(val)
        except Exception:
            a_vals.append(0)
            
    b_vals = []
    for i in range(M):
        try:
            val = eval_seq(b, i)
            if hasattr(val, 'is_finite') and not val.is_finite:
                val = 0
            if isinstance(val, float) and val.is_integer():
                val = int(val)
            b_vals.append(val)
        except Exception:
            b_vals.append(0)
    
    c = [0]*M
    g_pow = [[0]*M for _ in range(M)]
    g_pow[0][0] = 1
    for k in range(1, M):
        for i in range(M):
            if g_pow[k-1][i] == 0: continue
            for j in range(M - i):
                try:
                    term = g_pow[k-1][i] * b_vals[j]
                except OverflowError:
                    term = sympy.Float(g_pow[k-1][i]) * sympy.Float(b_vals[j])
                g_pow[k][i+j] += term
                
    for m in range(M):
        for k in range(m + 1):
            try:
                term = a_vals[k] * g_pow[k][m]
            except OverflowError:
                term = sympy.Float(a_vals[k]) * sympy.Float(g_pow[k][m])
            c[m] += term
    return c

def is_R_zero_numeric(vals):
    A = get_limsup_envelope(vals, 10, 80, 5)
    if all(a == 0 for a in A):
        return False
        
    mid = len(A) // 2
    if math.isinf(A[-1]) or math.isinf(A[mid]):
        return True
        
    rel_growth = (A[-1] - A[mid]) / (A[-1] + 1e-9)
    
    return rel_growth > 0.1 and A[-1] > 1.5

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        f_seq, g_seq = witness
        
        try:
            h1 = is_R_positive(f_seq)
        except Exception:
            h1 = False
            
        try:
            b0 = float(eval_seq(g_seq, 0))
            h2 = (b0 == 0.0)
        except Exception:
            h2 = False
            
        try:
            c_vals = get_c_seq(f_seq, g_seq, 80)
            neg_q = is_R_zero_numeric(c_vals)
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: f(x) has radius of convergence R_1 > 0",
    "H_2: The constant term of g(x) is zero (b_0 = 0)",
    "¬Q: The composition f(g(x)) has radius of convergence 0"
]

N_HYP = 2
NEG_Q_INDEX = 2