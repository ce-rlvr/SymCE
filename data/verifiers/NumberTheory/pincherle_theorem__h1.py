import sympy
import math

# Top-level setup
n = sympy.Symbol('n', integer=True)

def conditions(witness) -> list[bool]:
    """
    witness is a tuple (a, b) where a and b are callables, lists/tuples, or sympy expressions in terms of n.
    a(n) and b(n) return the n-th term of the sequences for n >= 1.
    """
    N = 400
    try:
        a_seq = []
        b_seq = []
        for i in range(1, N + 1):
            # Extract a_n
            if callable(witness[0]):
                a_val = witness[0](i)
            elif isinstance(witness[0], (list, tuple)):
                a_val = witness[0][i-1]
            else:
                a_val = witness[0]
                
            # Extract b_n
            if callable(witness[1]):
                b_val = witness[1](i)
            elif isinstance(witness[1], (list, tuple)):
                b_val = witness[1][i-1]
            else:
                b_val = witness[1]
                
            # Evaluate in case it's a sympy expression with 'n'
            if isinstance(a_val, sympy.Expr):
                a_val = a_val.subs(n, i)
            if isinstance(b_val, sympy.Expr):
                b_val = b_val.subs(n, i)
                
            a_seq.append(sympy.sympify(a_val))
            b_seq.append(sympy.sympify(b_val))
    except Exception:
        return [False, False]
        
    # Check H1: a_n != 0 for all n >= 1
    try:
        h1 = all(a != 0 for a in a_seq)
    except Exception:
        h1 = False
        
    # Check Conclusion
    try:
        A = [sympy.Integer(0)] * (N + 2)
        B = [sympy.Integer(0)] * (N + 2)
        
        A[0] = sympy.Integer(1) # A_{-1}
        A[1] = sympy.Integer(0) # A_0
        B[0] = sympy.Integer(0) # B_{-1}
        B[1] = sympy.Integer(1) # B_0
        
        for i in range(1, N + 1):
            a_n = a_seq[i-1]
            b_n = b_seq[i-1]
            A[i+1] = b_n * A[i] + a_n * A[i-1]
            B[i+1] = b_n * B[i] + a_n * B[i-1]
            
        convergents = []
        for i in range(1, N + 1):
            if B[i+1] == 0:
                convergents.append(float('inf'))
            else:
                try:
                    val_expr = sympy.N(A[i+1] / B[i+1])
                    val = float(val_expr)
                    convergents.append(val)
                except TypeError:
                    convergents.append(float('nan'))
                except OverflowError:
                    try:
                        if (A[i+1] > 0) == (B[i+1] > 0):
                            convergents.append(float('inf'))
                        else:
                            convergents.append(-float('inf'))
                    except Exception:
                        convergents.append(float('inf'))
                except Exception:
                    convergents.append(float('nan'))
                    
        def goes_to_infinity(seq):
            if len(seq) < 50: return False
            tail = seq[-50:]
            if any(math.isnan(x) for x in tail): return False
            
            try:
                if max(tail) - min(tail) < 1e-2 and max([abs(x) for x in tail]) < 1e6:
                    return False
            except Exception:
                pass
                
            inv_tail = [1.0/x if x != 0 and not math.isinf(x) else 0.0 if math.isinf(x) else float('inf') for x in tail]
            if any(math.isinf(x) for x in inv_tail): return False
            
            if max(inv_tail) - min(inv_tail) > 1e-2:
                return False
                
            if max([abs(x) for x in inv_tail]) > 1e-2:
                return False
                
            return True
            
        neg_q = goes_to_infinity(convergents)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a_n != 0 for all n >= 1",
    "¬Q: The equivalence between convergence of the continued fraction and existence of a minimal solution fails"
]

N_HYP = 1
NEG_Q_INDEX = 1