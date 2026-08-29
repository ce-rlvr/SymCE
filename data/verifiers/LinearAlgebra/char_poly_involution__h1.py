import sympy
from sympy import eye, zeros, Dummy, simplify, Poly

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        x = Dummy('x')
        
        # Support both exact matrices and matrices modulo m (provided as a tuple)
        is_mod = False
        if isinstance(witness, tuple) and len(witness) == 2:
            A, m = witness
            try:
                m = int(m)
                is_mod = True
            except Exception:
                pass
                
        if not is_mod:
            A = witness

        # Check basic matrix properties
        if not hasattr(A, 'shape') or len(A.shape) != 2 or A.shape[0] != A.shape[1]:
            return [False, False]
            
        n = A.shape[0]
        I = eye(n)
        
        if is_mod:
            # H1: A^2 = I mod m
            try:
                diff = A**2 - I
                try:
                    h1 = all(int(e) % m == 0 for e in diff)
                except Exception:
                    h1 = False
            except Exception:
                h1 = False
                
            # Q: charpoly is of the form (x-1)^k (x+1)^{n-k} mod m
            try:
                cp = A.charpoly(x).as_expr()
                q_holds = False
                for k in range(n + 1):
                    expected = ((x - 1)**k) * ((x + 1)**(n - k))
                    diff_poly = Poly(cp - expected, x)
                    try:
                        is_zero_mod = all(int(c) % m == 0 for c in diff_poly.coeffs())
                    except Exception:
                        is_zero_mod = False
                    if is_zero_mod:
                        q_holds = True
                        break
                neg_q = not q_holds
            except Exception:
                neg_q = False
                
        else:
            # H1: A^2 = I exactly
            try:
                h1 = bool(A**2 == I)
            except Exception:
                h1 = False
                
            # Q: charpoly is of the form (x-1)^k (x+1)^{n-k} exactly
            try:
                cp = A.charpoly(x).as_expr()
                q_holds = False
                for k in range(n + 1):
                    expected = ((x - 1)**k) * ((x + 1)**(n - k))
                    if simplify(cp - expected) == 0:
                        q_holds = True
                        break
                neg_q = not q_holds
            except Exception:
                neg_q = False
                
        return [h1, neg_q]
        
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: A is an involution (A^2 = I)",
    "¬Q: The characteristic polynomial of A is NOT of the form (x-1)^k (x+1)^{n-k}"
]

N_HYP = 1
NEG_Q_INDEX = 1