import sympy
from sympy import Matrix, eye, zeros, simplify, Poly, Expr, sympify, MatrixBase
from sympy.abc import x

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            lambda_val = witness.get('lambda', witness.get('lambda_val'))
            p = witness.get('p')
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                A, lambda_val, p = witness
            elif len(witness) == 4:
                _, A, lambda_val, p = witness
            else:
                A, lambda_val, p = None, None, None
        else:
            A, lambda_val, p = None, None, None
            
        if A is None or lambda_val is None or p is None:
            return [False, False, False, False]
            
        if isinstance(A, (list, tuple)):
            try:
                A = Matrix(A)
            except Exception:
                pass

        if isinstance(lambda_val, str):
            try:
                lambda_val = sympify(lambda_val)
            except Exception:
                pass

        if isinstance(p, str):
            try:
                p = sympify(p)
            except Exception:
                pass

        # H1: F is a field
        # Implicitly satisfied if A and lambda_val are valid mathematical objects
        h1 = True
        
        # H2: A is an n x n matrix over F
        try:
            h2 = bool(isinstance(A, MatrixBase) and A.is_square)
        except Exception:
            h2 = False
            
        # H3: \lambda \in F
        try:
            h3 = bool(isinstance(lambda_val, (int, float, complex, Expr)))
        except Exception:
            h3 = False
            
        # neg_Q: \lambda is an eigenvalue of A iff p(\lambda) = 0 is FALSE
        try:
            eigenvals = A.eigenvals()
            is_eigenval = False
            for ev in eigenvals:
                if simplify(ev - lambda_val) == 0:
                    is_eigenval = True
                    break
                    
            if isinstance(p, Poly):
                p_val = p.eval(lambda_val)
            elif callable(p):
                p_val = p(lambda_val)
            elif hasattr(p, 'free_symbols'):
                free = p.free_symbols
                if len(free) == 1:
                    p_val = p.subs(list(free)[0], lambda_val)
                else:
                    p_val = p.subs(x, lambda_val)
            else:
                p_val = p
                
            p_zero = bool(simplify(p_val) == 0)
            
            neg_q = bool(is_eigenval != p_zero)
        except Exception:
            neg_q = False
            
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: A is an n \\times n matrix over F",
    "H_3: \\lambda \\in F",
    "¬Q: \\lambda is an eigenvalue of A iff p(\\lambda) = 0 is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3