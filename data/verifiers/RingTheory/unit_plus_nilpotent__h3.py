import sympy as sp
import math

# Top-level setup
x, y, z = sp.symbols('x y z')

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, dict):
            n = witness.get('n', 0)
            u = witness.get('u', 1)
            x_val = witness.get('x', 0)
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                n = 0
                u, x_val = witness
            elif len(witness) == 3:
                n, u, x_val = witness
            else:
                return [False, False, False]
        else:
            n = 0
            u = 1
            x_val = witness

        if isinstance(x_val, sp.MatrixBase) or isinstance(u, sp.MatrixBase):
            return [False, False, False]

        n = int(n)
        if n < 0:
            return [False, False, False]

        # n > 0 case: evaluate in Z/nZ
        if n > 0:
            u = int(u)
            x_val = int(x_val)
            h1 = True
            h2 = (math.gcd(u, n) == 1)
            neg_q = (math.gcd((u + x_val) % n, n) != 1)
            return [h1, h2, neg_q]

        # n == 0 case with sympy expressions: evaluate in Z[x]
        if hasattr(x_val, 'free_symbols') or hasattr(u, 'free_symbols'):
            h1 = True 
            
            u_sym = sp.sympify(u)
            if u_sym.is_constant():
                try:
                    h2 = (abs(int(u_sym)) == 1)
                except Exception:
                    h2 = False
            else:
                h2 = False
                
            ux = sp.sympify(u) + sp.sympify(x_val)
            if ux.is_constant():
                try:
                    neg_q = (abs(int(ux)) != 1)
                except Exception:
                    neg_q = True
            else:
                neg_q = True
                
            return [h1, h2, neg_q]

        # n == 0 pure integer case: evaluate in Z
        u = int(u)
        x_val = int(x_val)
        
        h1 = True
        h2 = (abs(u) == 1)
        neg_q = (abs(u + x_val) != 1)
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: u is a unit in R",
    "¬Q: u + x is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2