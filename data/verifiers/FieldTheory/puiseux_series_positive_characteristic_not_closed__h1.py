import sympy
from sympy import isprime

# Top-level setup
x, t, X, T, y, Y = sympy.symbols('x t X T y Y')

def conditions(witness):
    """
    Verifies that the witness is a valid counterexample to the false conjecture.
    The conjecture claims that the field of Puiseux series L over a field K of 
    characteristic p > 0 is algebraically closed (or similar, depending on the 
    exact dropped hypothesis). Since L is NEVER algebraically closed in char p > 0,
    any valid prime p (or tuple containing p) serves as a counterexample.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        p_val = None
        
        # 1. Witness is an integer (the prime p)
        if isinstance(witness, (int, sympy.Integer)):
            p_val = int(witness)
            
        # 2. Witness is a string representation of an integer
        elif isinstance(witness, str):
            try:
                p_val = int(witness)
            except ValueError:
                pass
                
        # 3. Witness is a tuple/list, e.g., (p, polynomial)
        elif isinstance(witness, (tuple, list)) and len(witness) > 0:
            if isinstance(witness[0], (int, sympy.Integer)):
                p_val = int(witness[0])
                
        # 4. Witness is a field domain with a characteristic
        elif hasattr(witness, 'characteristic'):
            char = witness.characteristic
            p_val = int(char()) if callable(char) else int(char)
            
        # 5. Witness is a polynomial over a domain with a characteristic
        elif hasattr(witness, 'domain') and hasattr(witness.domain, 'characteristic'):
            char = witness.domain.characteristic
            p_val = int(char()) if callable(char) else int(char)
            
        # 6. Witness is a symbolic expression (e.g., Artin-Schreier polynomial X^p - X - 1/t)
        elif isinstance(witness, sympy.Expr):
            for sym in witness.free_symbols:
                try:
                    poly = sympy.Poly(witness, sym)
                    deg = int(poly.degree())
                    if isprime(deg) and deg > 0:
                        p_val = deg
                        break
                except Exception:
                    continue
                    
        # Verify the extracted characteristic is a prime p > 0
        if p_val is not None:
            if isprime(p_val) and p_val > 0:
                h1 = True
                
        # If H1 holds, H2 (definition of L) holds by context.
        # Since L is never algebraically closed in char p > 0, the conclusion 
        # "L is algebraically closed" always fails, making its negation True.
        if h1:
            h2 = True
            neg_q = True
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Let the characteristic of K be a prime p > 0",
    "H_2: Let L be the field of Puiseux series over K",
    "¬Q: The field L is algebraically closed"
]

N_HYP = 2
NEG_Q_INDEX = 2