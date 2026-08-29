import sympy
from sympy import Symbol, limit, oo, im, sqrt, sympify, MatrixBase, Tuple
import math

n = Symbol('n', integer=True, positive=True)
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def evaluate(f, n_sym, i):
    if callable(f):
        try:
            res = f(i)
            return sympify(res)
        except Exception:
            return None
    else:
        try:
            return f.subs(n_sym, i)
        except Exception:
            return None

def has_infinite_range(f, n_sym):
    try:
        vals = set()
        for i in range(1, 201):
            try:
                val = evaluate(f, n_sym, i)
                if val is None:
                    continue
                
                if isinstance(val, (MatrixBase, tuple, list, Tuple)):
                    if isinstance(val, MatrixBase):
                        val_eval = val.evalf()
                        vals.add(tuple(round(float(x), 8) for x in val_eval))
                    else:
                        val_eval = [sympify(v).evalf() for v in val]
                        vals.add(tuple(round(float(x), 8) for x in val_eval))
                else:
                    val_eval = val.evalf()
                    if val_eval.is_number:
                        val_c = complex(val_eval)
                        vals.add((round(val_c.real, 8), round(val_c.imag, 8)))
                    else:
                        vals.add(val_eval)
            except Exception:
                continue
        if len(vals) > 100:
            return True
        return False
    except Exception:
        return False

def is_bounded(f, n_sym):
    if not callable(f):
        try:
            if isinstance(f, (MatrixBase, tuple, list, Tuple)):
                if isinstance(f, MatrixBase):
                    f_mag = f.norm()
                else:
                    f_mag = sqrt(sum(abs(x)**2 for x in f))
            else:
                f_mag = abs(f)
                
            L = limit(f_mag, n_sym, oo)
            if L == oo:
                return False
            if L.is_number and L < oo:
                return True
        except Exception:
            pass

    try:
        vals = []
        for i in [10, 100, 1000, 10000]:
            try:
                val = evaluate(f, n_sym, i)
                if val is None:
                    return False
                    
                if isinstance(val, (MatrixBase, tuple, list, Tuple)):
                    if isinstance(val, MatrixBase):
                        mag = val.norm().evalf()
                    else:
                        mag = sqrt(sum(abs(x)**2 for x in val)).evalf()
                else:
                    mag = abs(val).evalf()
                    
                if not mag.is_number:
                    return False
                vals.append(float(mag))
            except Exception:
                return False
            
        if any(v > 1e6 for v in vals):
            return False
            
        if vals[-1] > vals[-2] > vals[-3]:
            diff1 = vals[-2] - vals[-3]
            diff2 = vals[-1] - vals[-2]
            if diff2 >= diff1 * 0.5:
                return False
                
        return True
    except Exception:
        return False

def has_no_real_accumulation_points(f, n_sym):
    if not callable(f) and isinstance(f, (MatrixBase, tuple, list, Tuple)):
        return True
        
    if not callable(f):
        try:
            im_f = im(f)
            L = limit(im_f, n_sym, oo)
            if L == 0:
                return False
            elif L.is_number and L != 0:
                return True
        except Exception:
            pass
        
        try:
            L = limit(abs(im(f)), n_sym, oo)
            if L == 0:
                return False
            elif L.is_number and L > 0:
                return True
        except Exception:
            pass

    try:
        def get_im_abs(i):
            try:
                val = evaluate(f, n_sym, i)
                if val is None:
                    return 0.0
                if isinstance(val, (MatrixBase, tuple, list, Tuple)):
                    return 1.0 
                return float(abs(im(val)).evalf())
            except Exception:
                return 0.0

        min_100 = min(get_im_abs(i) for i in range(100, 200))
        min_1000 = min(get_im_abs(i) for i in range(1000, 1100))
        
        if min_1000 < 0.05:
            return False
            
        if min_1000 < min_100 * 0.5:
            min_10000 = min(get_im_abs(i) for i in range(10000, 10100))
            if min_10000 < 0.05 or min_10000 < min_1000 * 0.5:
                return False
                
        return True
    except Exception:
        return False

def conditions(witness):
    n_sym = Symbol('n', integer=True, positive=True)
    
    if hasattr(witness, 'formula') and hasattr(witness, 'variables'):
        try:
            f = witness.formula
            var = witness.variables[0]
            f = f.subs(var, n_sym)
        except Exception:
            f = witness
    else:
        f = witness

    if not callable(f) and hasattr(f, 'free_symbols'):
        try:
            free_syms = list(f.free_symbols)
            if len(free_syms) == 1:
                f = f.subs(free_syms[0], n_sym)
        except Exception:
            pass

    H1 = has_infinite_range(f, n_sym)
    H2 = is_bounded(f, n_sym)
    neg_Q = has_no_real_accumulation_points(f, n_sym)
    
    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: The range of the sequence is infinite",
    "H_2: (x_n) is bounded",
    "¬Q: The sequence has no accumulation points in R"
]
N_HYP = 2
NEG_Q_INDEX = 2