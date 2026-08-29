import sympy as sp
import math

n = sp.Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture states that for any metric space X, sequence (x_n) in X, and point x,
    the set {x_n : n in N} U {x} is compact.
    
    A valid witness is a tuple (seq, x_val) where:
      - seq is a sympy expression in terms of n, or a callable function of n.
      - x_val is a real number.
    """
    try:
        seq, x_val = witness
    except Exception:
        return [False, False, False]
        
    # H1: X is a metric space
    # We assume X is the real line with the standard metric, which is always a metric space.
    h1_ok = True
    
    # H2: (x_n) is a sequence in X
    h2_ok = False
    neg_q_ok = False
    
    if callable(seq):
        try:
            vals = []
            for i in range(1, 2001):
                vals.append(float(seq(i)))
            h2_ok = True
        except Exception:
            h2_ok = False
            
        if h2_ok:
            try:
                if max(abs(v) for v in vals) > 1000:
                    # Unbounded, hence not compact
                    neg_q_ok = True
                else:
                    # Empirical check for closedness
                    is_strictly_increasing = all(vals[i] < vals[i+1] for i in range(len(vals)-1))
                    is_strictly_decreasing = all(vals[i] > vals[i+1] for i in range(len(vals)-1))
                    if is_strictly_increasing or is_strictly_decreasing:
                        L_est = vals[-1]
                        if abs(L_est - float(x_val)) > 1e-2:
                            # Limit is not x_val and not in the sequence
                            neg_q_ok = True
            except Exception:
                pass
                
    elif isinstance(seq, sp.Expr):
        try:
            vals = []
            for i in range(1, 11):
                val = seq.subs(n, i).evalf()
                if not val.is_real:
                    break
                vals.append(val)
            else:
                h2_ok = True
        except Exception:
            h2_ok = False
            
        if h2_ok:
            try:
                is_unbounded = False
                for i in [10, 100, 1000, 10000, 100000]:
                    try:
                        val = abs(seq.subs(n, i).evalf())
                        if val > 1000:
                            is_unbounded = True
                            break
                    except Exception:
                        pass
                
                if is_unbounded:
                    neg_q_ok = True
                else:
                    L = sp.limit(seq, n, sp.oo)
                    if L == sp.oo or L == -sp.oo:
                        neg_q_ok = True
                    elif L.is_real:
                        if abs(float(L) - float(x_val)) > 1e-9:
                            has_positive_integer_sol = False
                            try:
                                sol = sp.solve(seq - L, n)
                                for s in sol:
                                    if s.is_real and s > 0 and s.is_integer:
                                        has_positive_integer_sol = True
                                        break
                            except Exception:
                                pass
                            
                            found_in_first_1000 = False
                            for i in range(1, 1001):
                                try:
                                    if abs(float(seq.subs(n, i).evalf()) - float(L)) < 1e-9:
                                        found_in_first_1000 = True
                                        break
                                except Exception:
                                    pass
                                    
                            if not has_positive_integer_sol and not found_in_first_1000:
                                neg_q_ok = True
            except Exception:
                pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: (x_n) is a sequence in X",
    "¬Q: The set {x_n : n in N} U {x} is not a compact subset of X"
]

N_HYP = 2
NEG_Q_INDEX = 2