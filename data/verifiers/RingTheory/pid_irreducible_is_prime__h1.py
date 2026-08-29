import sympy
import math

# Top-level setup
class QuadraticInteger:
    """
    Represents an element a + b*sqrt(d) in the ring Z[sqrt(d)].
    (Assuming d is a square-free integer < 0).
    """
    def __init__(self, d, a, b):
        self.d = d
        self.a = a
        self.b = b

    def __repr__(self):
        return f"({self.a} + {self.b}*sqrt({self.d}))"

# Provide a convenient binding for the most common counterexample ring
Z_sqrt_m5 = QuadraticInteger

def parse_sympy_expr(expr):
    if hasattr(expr, 'is_Integer') and expr.is_Integer:
        return -5, int(expr), 0
    try:
        atoms = expr.atoms(sympy.Pow)
        for atom in atoms:
            if atom.exp == sympy.S.Half:
                d_val = atom.base
                if d_val.is_Integer and d_val < 0:
                    d = int(d_val)
                    b = expr.coeff(atom)
                    a = sympy.simplify(expr - b * atom)
                    if a.is_Integer and b.is_Integer:
                        return d, int(a), int(b)
    except Exception:
        pass
    return None

def divides(d, x_a, x_b, y_a, y_b):
    Nx = x_a**2 - d * x_b**2
    if Nx == 0:
        return False
    real_part = y_a * x_a - d * y_b * x_b
    imag_part = y_b * x_a - y_a * x_b
    return real_part % Nx == 0 and imag_part % Nx == 0

def is_irreducible(d, p_a, p_b):
    Np = p_a**2 - d * p_b**2
    if Np <= 1:
        return False
    max_xb = int(math.isqrt(abs(Np // d))) + 1
    max_xa = int(math.isqrt(Np)) + 1
    
    for x_b in range(-max_xb, max_xb + 1):
        for x_a in range(-max_xa, max_xa + 1):
            Nx = x_a**2 - d * x_b**2
            if 1 < Nx < Np:
                if divides(d, x_a, x_b, p_a, p_b):
                    return False
    return True

def is_not_prime(d, p_a, p_b):
    box = 10
    elements = []
    for a in range(-box, box+1):
        for b in range(-box, box+1):
            if a == 0 and b == 0: continue
            elements.append((a, b))
            
    # Sort by norm to find the simplest counterexample quickly
    elements.sort(key=lambda x: x[0]**2 - d * x[1]**2)
            
    for A_a, A_b in elements:
        if divides(d, p_a, p_b, A_a, A_b):
            continue
        for B_a, B_b in elements:
            if divides(d, p_a, p_b, B_a, B_b):
                continue
            prod_a = A_a * B_a + d * A_b * B_b
            prod_b = A_a * B_b + A_b * B_a
            if divides(d, p_a, p_b, prod_a, prod_b):
                return True
    return False

def conditions(witness) -> list[bool]:
    try:
        A_a, A_b, B_a, B_b = None, None, None, None
        parsed = False
        
        if isinstance(witness, tuple):
            if len(witness) == 3:
                d, p_a, p_b = witness
                parsed = True
            elif len(witness) == 7:
                d, p_a, p_b, A_a, A_b, B_a, B_b = witness
                parsed = True
                
        if not parsed and hasattr(witness, 'd') and hasattr(witness, 'a') and hasattr(witness, 'b'):
            d, p_a, p_b = witness.d, witness.a, witness.b
            parsed = True
            
        if not parsed:
            if isinstance(witness, sympy.Expr):
                res = parse_sympy_expr(witness)
                if res is not None:
                    d, p_a, p_b = res
                    parsed = True
            elif isinstance(witness, int):
                d, p_a, p_b = -5, witness, 0
                parsed = True
                
        if not parsed:
            return [False, False]
            
        if d >= 0 or not isinstance(d, int):
            return [False, False]
            
        # H1: p is irreducible
        try:
            h1 = is_irreducible(d, p_a, p_b)
        except Exception:
            h1 = False
        
        # neg_Q: p is not prime
        try:
            if A_a is not None:
                prod_a = A_a * B_a + d * A_b * B_b
                prod_b = A_a * B_b + A_b * B_a
                neg_q = (not divides(d, p_a, p_b, A_a, A_b) and 
                         not divides(d, p_a, p_b, B_a, B_b) and 
                         divides(d, p_a, p_b, prod_a, prod_b))
            else:
                neg_q = is_not_prime(d, p_a, p_b)
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: p is an irreducible element in R",
    "¬Q: p is not a prime element in R"
]
N_HYP = 1
NEG_Q_INDEX = 1