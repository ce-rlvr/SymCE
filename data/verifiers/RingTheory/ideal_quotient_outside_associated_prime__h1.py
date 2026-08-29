import sympy
from sympy import Matrix, Integer, eye, zeros
from math import gcd
from sympy.ntheory import factorint

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: Q is a P-primary ideal of R",
    "H_2: x is an element of R such that x ∉ P",
    "¬Q: The ideal quotient (Q : x) is not equal to Q"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Evaluates the conditions for the counterexample.
    The theorem holds for commutative rings, so a valid counterexample 
    must be in a non-commutative ring (e.g., a matrix ring).
    
    Expected witness format:
    A tuple (Q, P, x) or (R, Q, P, x) or a dict with keys 'Q', 'P', 'x'.
    For the matrix ring M_n(F), the zero ideal is {0}-primary.
    """
    try:
        # Extract Q, P, x from the witness
        if isinstance(witness, dict):
            Q = witness.get('Q')
            P = witness.get('P')
            x = witness.get('x')
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                Q, P, x = witness
            elif len(witness) == 4:
                _, Q, P, x = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]

        # Convert list of lists to SymPy Matrix if applicable
        if isinstance(x, list) and len(x) > 0 and isinstance(x[0], list):
            try:
                x = Matrix(x)
            except Exception:
                pass

        def is_zero_ideal(ideal):
            if ideal in (0, [0], "0", "[0]"): 
                return True
            if ideal is None:
                return False
            if isinstance(ideal, list):
                if len(ideal) == 0: return True
                for b in ideal:
                    if hasattr(b, '__iter__'):
                        if not all(val == 0 for val in b): return False
                    elif b != 0:
                        return False
                return True
            if hasattr(ideal, '__iter__'):
                return all(val == 0 for val in ideal)
            return False

        # Case 1: Non-commutative Matrix Ring (Valid counterexamples exist here)
        if hasattr(x, 'shape') and len(x.shape) == 2 and x.shape[0] == x.shape[1]:
            # In M_n(F), the zero ideal is {0}-primary.
            h1 = is_zero_ideal(Q) and is_zero_ideal(P)
            
            # x must be an element of R not in P (which is {0})
            h2 = not is_zero_ideal(x)
            
            # Conclusion: (Q : x) == Q
            # Since Q = {0}, the left ideal quotient (Q : x) = {y | yx = 0}.
            # (Q : x) == {0} iff x is not a right zero divisor.
            # For square matrices, this is true iff det(x) != 0.
            # We want the conclusion to FAIL, so neg_q is True when det(x) == 0.
            neg_q = (x.det() == 0)
            
            return [bool(h1), bool(h2), bool(neg_q)]
            
        # Case 2: Commutative Integer Ring (Included for completeness; will not yield a counterexample)
        elif isinstance(x, (int, Integer)):
            try:
                q = abs(int(Q))
            except (ValueError, TypeError):
                q = 0
            try:
                p = abs(int(P))
            except (ValueError, TypeError):
                p = 0
            x_val = int(x)
            
            if q == 0:
                h1 = (p == 0)
            else:
                factors = factorint(q)
                if len(factors) == 1:
                    prime = list(factors.keys())[0]
                    h1 = (p == prime)
                else:
                    h1 = False
                    
            h2 = (x_val % p != 0) if p != 0 else (x_val != 0)
            
            if q == 0:
                ideal_quotient = 0
            else:
                ideal_quotient = q // gcd(q, x_val)
                
            neg_q = (ideal_quotient != q)
            
            return [bool(h1), bool(h2), bool(neg_q)]
            
        else:
            return [False, False, False]
            
    except Exception:
        return [False, False, False]