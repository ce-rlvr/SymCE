import math
import sympy
from sympy import Rational, Integer, Symbol

# Top-level setup for potential witness expressions
x = Symbol('x')
n = Symbol('n')

def conditions(witness):
    """
    Check if the witness satisfies the hypotheses and falsifies the conclusion.
    Witness should be a tuple (a, b, f) where:
      - a, b are real numbers with a < b
      - f is a callable f(n, x) returning a real number, or a sympy expression in n and x
    """
    h1_ok = False
    h2_ok = False
    neg_q_ok = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            a, b, f_obj = witness
            
            if isinstance(a, (int, float)) and isinstance(b, (int, float)) and a < b:
                if callable(f_obj):
                    f = f_obj
                elif hasattr(f_obj, 'subs'):
                    def f(n_val, x_val):
                        return float(f_obj.subs({'n': n_val, 'x': x_val}))
                else:
                    f = None
                
                if f is not None:
                    # Check H1: f evaluates to real numbers on the interval
                    h1_ok = True
                    for n_val in [1, 2, 5]:
                        for x_val in [a, (a + b) / 2.0, b]:
                            try:
                                val = float(f(n_val, x_val))
                                if math.isnan(val) or math.isinf(val):
                                    h1_ok = False
                                    break
                            except Exception:
                                h1_ok = False
                                break
                        if not h1_ok:
                            break
                    
                    if h1_ok:
                        # Check H2: f_n is monotonically increasing for each n
                        h2_ok = True
                        for n_val in range(1, 21):
                            xs = [a + i * (b - a) / 50.0 for i in range(51)]
                            for i in range(50):
                                try:
                                    v1 = float(f(n_val, xs[i]))
                                    v2 = float(f(n_val, xs[i+1]))
                                    # Allow a tiny floating point tolerance
                                    if v1 > v2 + 1e-7:
                                        h2_ok = False
                                        break
                                except Exception:
                                    h2_ok = False
                                    break
                            if not h2_ok:
                                break
                        
                        # Check ¬Q: The sequence has NO pointwise convergent subsequence.
                        # For a sequence of monotonically increasing functions, this happens
                        # IF AND ONLY IF the sequence is not pointwise bounded, which means
                        # max(|f_n(a)|, |f_n(b)|) -> infinity as n -> infinity.
                        try:
                            def get_M(n_val):
                                try:
                                    v1 = abs(float(f(n_val, a)))
                                    v2 = abs(float(f(n_val, b)))
                                    return max(v1, v2)
                                except OverflowError:
                                    return float('inf')
                                except Exception:
                                    return None

                            M_100_list = [get_M(n_val) for n_val in range(100, 110)]
                            M_1000_list = [get_M(n_val) for n_val in range(1000, 1010)]
                            M_5000_list = [get_M(n_val) for n_val in range(5000, 5010)]
                            
                            if all(m is not None for m in M_100_list + M_1000_list + M_5000_list):
                                M_100 = min(M_100_list)
                                M_1000 = min(M_1000_list)
                                M_5000 = min(M_5000_list)
                                
                                if M_5000 == float('inf') and M_1000 == float('inf'):
                                    neg_q_ok = True
                                elif M_5000 == float('inf') and M_1000 > M_100 + 0.1:
                                    neg_q_ok = True
                                elif M_5000 > M_1000 + 0.1 and M_1000 > M_100 + 0.1:
                                    neg_q_ok = True
                        except Exception:
                            pass
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f_n is a sequence of functions from a closed and bounded interval to R",
    "H_2: f_n is a monotonically increasing function for each n in N",
    "¬Q: The sequence f_n does not have a pointwise convergent subsequence"
]

N_HYP = 2
NEG_Q_INDEX = 2