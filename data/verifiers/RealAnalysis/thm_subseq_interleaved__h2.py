import sympy
from sympy import Symbol

# Top-level setup
n = Symbol('n', integer=True, positive=True)

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion for the conjecture.
    
    The witness is expected to be a tuple: (x, y, z, L)
    where x, y, z are lists representing the first N terms of the sequences (1-indexed mathematically),
    or functions/lambdas taking an integer index, or sympy expressions in terms of 'n'.
    """
    try:
        x, y, z, L = witness
    except Exception:
        return [False, False, False, False]

    def get_term(seq, k):
        if isinstance(seq, (list, tuple)):
            return seq[(k - 1) % len(seq)]
        elif callable(seq):
            return seq(k)
        elif isinstance(seq, sympy.Basic):
            return seq.subs(n, k).evalf()
        else:
            raise ValueError("Sequence must be a list, tuple, callable, or sympy expression")

    # H_1: (x_n) is a sequence of real numbers
    try:
        h1_ok = True
        for k in range(1, 101):
            val = get_term(x, k)
            if isinstance(val, sympy.Basic):
                if not val.is_real:
                    h1_ok = False
                    break
            else:
                if isinstance(val, complex) and not isinstance(val, (float, int)):
                    if val.imag != 0:
                        h1_ok = False
                        break
    except Exception:
        h1_ok = False

    # H_2: (z_n) is the sequence defined by z_{2k} = x_k and z_{2k-1} = y_k for all integers k >= 1
    try:
        h2_ok = True
        for k in range(1, 101):
            x_k = get_term(x, k)
            y_k = get_term(y, k)
            z_2k = get_term(z, 2 * k)
            z_2k_minus_1 = get_term(z, 2 * k - 1)
            
            try:
                if abs(float(z_2k) - float(x_k)) > 1e-7:
                    h2_ok = False
                    break
            except Exception:
                if z_2k != x_k:
                    h2_ok = False
                    break
                    
            try:
                if abs(float(z_2k_minus_1) - float(y_k)) > 1e-7:
                    h2_ok = False
                    break
            except Exception:
                if z_2k_minus_1 != y_k:
                    h2_ok = False
                    break
    except Exception:
        h2_ok = False

    def is_subseq_limit(seq, limit_val):
        try:
            is_inf = False
            is_neg_inf = False
            is_numeric = True
            try:
                if limit_val == sympy.oo or limit_val == float('inf'):
                    is_inf = True
                elif limit_val == -sympy.oo or limit_val == float('-inf'):
                    is_neg_inf = True
                else:
                    limit_float = float(limit_val)
            except Exception:
                is_numeric = False

            if isinstance(seq, (list, tuple)):
                for val in seq:
                    if is_numeric:
                        try:
                            if is_inf:
                                if val == sympy.oo or float(val) == float('inf'): return True
                            elif is_neg_inf:
                                if val == -sympy.oo or float(val) == float('-inf'): return True
                            else:
                                if abs(float(val) - limit_float) < 1e-7: return True
                        except Exception:
                            pass
                    else:
                        if val == limit_val: return True
                return False
            
            close_count = 0
            for k in range(1, 501):
                try:
                    val = get_term(seq, k)
                    if is_numeric:
                        if is_inf:
                            if float(val) > 1e4: close_count += 1
                        elif is_neg_inf:
                            if float(val) < -1e4: close_count += 1
                        else:
                            if abs(float(val) - limit_float) < 1e-5: close_count += 1
                    else:
                        if val == limit_val: close_count += 1
                except Exception:
                    pass
                    
            if close_count >= 3:
                return True
                
            large_indices = [10**4, 2*10**4, 3*10**4, 4*10**4, 5*10**4]
            large_close_count = 0
            for idx in large_indices:
                try:
                    val = get_term(seq, idx)
                    if is_numeric:
                        if is_inf:
                            if float(val) > 1e4: large_close_count += 1
                        elif is_neg_inf:
                            if float(val) < -1e4: large_close_count += 1
                        else:
                            if abs(float(val) - limit_float) < 1e-4: large_close_count += 1
                    else:
                        if val == limit_val: large_close_count += 1
                except Exception:
                    pass
                    
            if large_close_count >= 2:
                return True
                
            return False
        except Exception:
            return False

    # H_3: L is a subsequential limit of (z_n)
    try:
        h3_ok = is_subseq_limit(z, L)
    except Exception:
        h3_ok = False

    # neg_Q: L is NOT a subsequential limit of (x_n) AND L is NOT a subsequential limit of (y_n)
    try:
        neg_q = (not is_subseq_limit(x, L)) and (not is_subseq_limit(y, L))
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: (x_n) is a sequence of real numbers",
    "H_2: (z_n) is the sequence defined by z_{2k} = x_k and z_{2k-1} = y_k for all integers k >= 1",
    "H_3: L is a subsequential limit of (z_n)",
    "not Q: L is NOT a subsequential limit of (x_n) AND L is NOT a subsequential limit of (y_n)"
]

N_HYP = 3
NEG_Q_INDEX = 3