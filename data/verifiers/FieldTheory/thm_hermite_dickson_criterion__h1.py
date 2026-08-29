import sympy
from sympy import symbols, Poly
from sympy.ntheory import factorint

# Top-level setup
x = symbols('x')

CONDITION_LABELS = [
    "H_1: f is a polynomial over F_q",
    "¬Q: The equivalence between f being a PP and the Hermite-Dickson conditions fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def is_prime_power(n):
    try:
        n = int(n)
    except Exception:
        return False
    if n < 2:
        return False
    factors = factorint(n)
    return len(factors) == 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            p = witness.get('p')
            f = witness.get('f')
        else:
            q, p, f = witness
    except Exception:
        return [False, False]
        
    try:
        if not is_prime_power(q):
            return [False, False]
            
        try:
            p = int(p)
        except Exception:
            return [False, False]
            
        if p < 2:
            return [False, False]
            
        factors = factorint(q)
        char = list(factors.keys())[0]
        
        # For simplicity, we only support prime fields in this verifier.
        # A valid counterexample exists for prime fields (e.g., q=5, p=2, f=x**2).
        if q != char:
            return [False, False]
            
        # Check H1: f is a polynomial
        try:
            f_poly = Poly(f, x, domain=f'GF({q})')
            h1 = True
        except Exception:
            h1 = False
            
        if not h1:
            return [False, False]
            
        # Evaluate LHS: f is a permutation polynomial over F_q
        values = set()
        roots = 0
        for i in range(q):
            val = f.subs(x, i)
            try:
                val = int(val)
            except TypeError:
                val = int(sympy.simplify(val))
            val = val % q
            values.add(val)
            if val == 0:
                roots += 1
                
        is_pp = (len(values) == q)
        exactly_one_root = (roots == 1)
        
        # Evaluate RHS: exactly one root AND degree conditions
        degree_condition = True
        mod_expr = x**q - x
        for t in range(1, q - 1):
            if t % p == 0:
                continue
                
            # Compute f(x)^t mod (x^q - x) over GF(q)
            base = f
            res = 1
            exp = t
            while exp > 0:
                if exp % 2 == 1:
                    res = sympy.rem(res * base, mod_expr, x, domain=f'GF({q})')
                base = sympy.rem(base * base, mod_expr, x, domain=f'GF({q})')
                exp //= 2
                
            res_poly = Poly(res, x, domain=f'GF({q})')
            deg = res_poly.degree()
            if deg == sympy.oo or deg == -sympy.oo:
                deg = -1
                
            if deg >= q - 1:
                degree_condition = False
                break
                
        rhs = exactly_one_root and degree_condition
        
        # The conjecture claims LHS <==> RHS
        conclusion = (is_pp == rhs)
        
        # We want the conclusion to FAIL
        neg_q = not conclusion
        
        return [h1, neg_q]
        
    except Exception:
        return [False, False]