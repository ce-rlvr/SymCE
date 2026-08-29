import sympy
import math
import itertools
import functools

from sympy.abc import n, k, x, y

CONDITION_LABELS = [
    "H_1: a_n and b_n are sequences of positive integers",
    "¬Q: The continued fraction does NOT converge to an irrational number strictly between 0 and 1"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        
        a_raw, b_raw = witness
        
        def make_func(seq):
            if callable(seq):
                return lambda idx: sympy.sympify(seq(idx))
            elif isinstance(seq, (list, tuple)):
                return lambda idx: sympy.sympify(seq[(idx - 1) % len(seq)])
            
            try:
                seq_expr = sympy.sympify(seq)
            except Exception:
                seq_expr = seq
                
            if hasattr(seq_expr, 'free_symbols') and len(seq_expr.free_symbols) == 1:
                sym = list(seq_expr.free_symbols)[0]
                return lambda idx: sympy.sympify(seq_expr.subs(sym, idx))
            else:
                return lambda idx: sympy.sympify(seq_expr)
                
        a_func = make_func(a_raw)
        b_func = make_func(b_raw)
        
        # Check hypothesis
        h1_ok = True
        for i in range(1, 201):
            try:
                a = a_func(i)
                b = b_func(i)
                if not a.is_integer or a <= 0:
                    h1_ok = False
                    break
                if not b.is_integer or b <= 0:
                    h1_ok = False
                    break
            except Exception:
                h1_ok = False
                break
                
    except Exception:
        h1_ok = False

    # Check negated conclusion
    neg_q_ok = False
    try:
        # 1. Try to detect periodicity
        seq_a = [int(a_func(i)) for i in range(1, 201)]
        seq_b = [int(b_func(i)) for i in range(1, 201)]
        
        def get_period(seq, max_period=100):
            for p in range(1, max_period + 1):
                is_periodic = True
                for i in range(max_period):
                    if seq[i] != seq[i + p]:
                        is_periodic = False
                        break
                if is_periodic:
                    return p
            return None
            
        p_a = get_period(seq_a)
        p_b = get_period(seq_b)
        
        periodic_success = False
        if p_a is not None and p_b is not None:
            p = math.lcm(p_a, p_b)
            
            M = sympy.Matrix([[1, 0], [0, 1]])
            for a, b in zip(seq_a[:p], seq_b[:p]):
                M = M * sympy.Matrix([[0, a], [1, b]])
            
            c2 = M[1,0]
            c1 = M[1,1] - M[0,0]
            c0 = -M[0,1]
            
            limit_val = None
            if c2 == 0:
                if c1 != 0:
                    r = -c0 / c1
                    if r > 0: limit_val = r
            else:
                delta = c1**2 - 4 * c2 * c0
                if delta >= 0:
                    r1 = (-c1 + sympy.sqrt(delta)) / (2 * c2)
                    r2 = (-c1 - sympy.sqrt(delta)) / (2 * c2)
                    pos_roots = [r for r in (r1, r2) if r > 0]
                    if pos_roots:
                        limit_val = pos_roots[0]
                        
            if limit_val is not None:
                periodic_success = True
                if limit_val <= 0 or limit_val >= 1:
                    neg_q_ok = True
                elif limit_val.is_rational:
                    neg_q_ok = True
                else:
                    neg_q_ok = False
                    
        if not periodic_success:
            # 2. Compute convergents
            N_conv = 500
            A_prev, A_curr = 1, 0
            B_prev, B_curr = 0, 1
            for i in range(1, N_conv + 1):
                a = int(a_func(i))
                b = int(b_func(i))
                A_next = b * A_curr + a * A_prev
                B_next = b * B_curr + a * B_prev
                A_prev, A_curr = A_curr, A_next
                B_prev, B_curr = B_curr, B_next
                
            if B_curr == 0 or B_prev == 0:
                neg_q_ok = True
            else:
                val1 = sympy.Rational(A_curr, B_curr)
                val2 = sympy.Rational(A_prev, B_prev)
                
                min_val = min(val1, val2)
                max_val = max(val1, val2)
                
                if max_val <= 0 or min_val >= 1:
                    neg_q_ok = True
                else:
                    diff = max_val - min_val
                    if diff < sympy.Rational(1, 10**20):
                        mid = (min_val + max_val) / 2
                        if mid <= 0 or mid >= 1:
                            neg_q_ok = True
                        elif abs(mid - 0) < sympy.Rational(1, 10**15) or abs(mid - 1) < sympy.Rational(1, 10**15):
                            neg_q_ok = True
                        else:
                            mid_float = mid.evalf(50)
                            simp = sympy.nsimplify(mid_float, tolerance=1e-15)
                            if isinstance(simp, sympy.Rational) and simp.q < 10000:
                                neg_q_ok = True
                            else:
                                neg_q_ok = False
                    else:
                        # Diverges or converges too slowly
                        neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]