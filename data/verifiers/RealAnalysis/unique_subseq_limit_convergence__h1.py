import sympy as sp
import math

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Duck-typing for custom witness objects
        if hasattr(witness, 'is_bounded'):
            h1 = witness.is_bounded()
            h2 = False
            for method_name in dir(witness):
                if 'subsequence' in method_name.lower() or 'h2' in method_name.lower():
                    h2 = getattr(witness, method_name)()
                    break
            q = witness.converges_to_L() if hasattr(witness, 'converges_to_L') else True
            return [bool(h1), bool(h2), not bool(q)]
            
        # Tuple unpacking for (sequence_expression_or_function, L) or (expr, n_var, L)
        if isinstance(witness, tuple):
            if len(witness) == 2:
                x_obj, L = witness
            elif len(witness) == 3:
                x_obj, _, L = witness
            else:
                return [False, False, False]
                
            if isinstance(x_obj, sp.Expr):
                syms = list(x_obj.free_symbols)
                if syms:
                    n_sym = syms[0]
                    x_func = sp.lambdify(n_sym, x_obj, 'math')
                else:
                    x_func = lambda n: float(x_obj)
            elif callable(x_obj):
                x_func = x_obj
            else:
                return [False, False, False]
                
            L_val = float(L)
            
            # Generate sequence terms
            terms = []
            for n in range(1, 3001):
                try:
                    val = float(x_func(n))
                    if math.isnan(val):
                        continue
                    terms.append(val)
                except Exception:
                    pass
                    
            if len(terms) < 1000:
                return [False, False, False]
                
            # H1: Check if the sequence is bounded
            max_100 = max(abs(t) for t in terms[:100]) if len(terms) >= 100 else 0
            max_1000 = max(abs(t) for t in terms[:1000]) if len(terms) >= 1000 else 0
            max_3000 = max(abs(t) for t in terms)
            
            h1 = True
            if max_3000 > max_1000 * 1.2 and max_1000 > max_100 * 1.2:
                if max_3000 > 10:
                    h1 = False
            if max_3000 > 1e6:
                h1 = False
                
            # H2: Check if every convergent subsequence converges to L
            last_terms = terms[-1000:]
            limit_points = []
            rounded = [round(val, 2) for val in last_terms]
            unique_rounded = set(rounded)
            
            for t in unique_rounded:
                count = sum(1 for val in last_terms if abs(val - t) < 1e-2)
                if count > 20:
                    limit_points.append(t)
                    
            oscillation = max(last_terms) - min(last_terms)
            
            if not limit_points:
                if oscillation > 0.2:
                    # If bounded and oscillating without dense limit points, it has multiple limit points
                    h2 = False if h1 else True
                else:
                    h2 = True
            else:
                if oscillation > 0.2:
                    if h1:
                        h2 = False
                    else:
                        h2 = all(abs(p - L_val) < 1e-1 for p in limit_points)
                else:
                    h2 = all(abs(p - L_val) < 1e-1 for p in limit_points)
                    
            # Q: Check if the sequence converges to L
            q = all(abs(t - L_val) < 1e-1 for t in last_terms[-100:])
            
            return [bool(h1), bool(h2), not bool(q)]
            
    except Exception:
        pass
        
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: (x_n) is bounded",
    "H_2: Every convergent subsequence of (x_n) converges to the same limit L",
    "¬Q: The sequence (x_n) does not converge to L"
]

N_HYP = 2
NEG_Q_INDEX = 2