import sympy
from sympy import sympify

# Top-level setup for witness expressions
ZZ = sympy.ZZ
QQ = sympy.QQ
x = sympy.Symbol('x')
y = sympy.Symbol('y')
z = sympy.Symbol('z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, a) where:
      - R is a SymPy domain (e.g., ZZ, QQ.old_poly_ring(x))
      - a is a callable a(k) or a list/tuple representing the sequence (a_k) for k >= 1
    """
    try:
        R, a = witness
    except Exception:
        return [False, False]
        
    # H_1: R is a unique factorization domain
    try:
        h1_ok = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1_ok = False
        
    # neg_Q: The sequence of principal ideals (a_k) does not stabilize.
    # i.e., for all N >= 1, there exists k >= N such that (a_k) != (a_N).
    try:
        def get_a(i):
            if callable(a):
                return a(i)
            else:
                return a[i-1]
                
        def to_R(val):
            try:
                res = R.from_sympy(sympify(val))
                if res in R:
                    return res
            except Exception:
                pass
            try:
                res = R(val)
                if res in R:
                    return res
            except Exception:
                pass
            if val in R:
                return val
            return None

        neg_q_ok = True
        zero = getattr(R, 'zero', 0)
        
        # Test for N from 1 to 20
        for N in range(1, 21):
            found_diff = False
            try:
                val_N = get_a(N)
            except IndexError:
                # If the sequence is finite and exhausted, it stabilizes vacuously.
                neg_q_ok = False
                break
                
            a_N = to_R(val_N)
            if a_N is None:
                neg_q_ok = False
                break
                
            # Look for a k > N where the ideal (a_k) differs from (a_N)
            for k in range(N + 1, N + 21):
                try:
                    val_k = get_a(k)
                except IndexError:
                    continue
                except Exception:
                    continue
                    
                a_k = to_R(val_k)
                if a_k is None:
                    neg_q_ok = False
                    break
                    
                try:
                    if a_N == zero and a_k == zero:
                        same_ideal = True
                    elif a_N == zero or a_k == zero:
                        same_ideal = False
                    else:
                        # In a domain, (x) == (y) iff x divides y and y divides x
                        q1, r1 = R.divide(a_k, a_N)
                        q2, r2 = R.divide(a_N, a_k)
                        same_ideal = (r1 == zero) and (r2 == zero)
                except Exception:
                    same_ideal = False
                    
                if not same_ideal:
                    found_diff = True
                    break
                    
            if not neg_q_ok:
                break
            if not found_diff:
                # No difference found in the window, assume it stabilized
                neg_q_ok = False
                break
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "¬Q: The sequence of principal ideals (a_k) does not stabilize"
]

N_HYP = 1
NEG_Q_INDEX = 1