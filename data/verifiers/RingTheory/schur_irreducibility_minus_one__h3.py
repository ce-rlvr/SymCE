import sympy as sp
from sympy.abc import x

def conditions(witness):
    h1_ok = False
    h2_ok = False
    neg_q_ok = False
    
    try:
        n, a, f = None, None, None
        
        # Extract variables from the witness
        if isinstance(witness, dict):
            n = witness.get('n')
            a = witness.get('a', witness.get('a_list'))
            f = witness.get('f')
        elif hasattr(witness, 'n') and hasattr(witness, 'a'):
            n = witness.n
            a = witness.a
            f = getattr(witness, 'f', None)
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                n, a, f = witness
            elif len(witness) == 2 and (isinstance(witness[0], int) or (hasattr(witness[0], 'is_integer') and witness[0].is_integer)) and isinstance(witness[1], (list, tuple)):
                n, a = witness
            elif all((isinstance(v, int) or (hasattr(v, 'is_integer') and v.is_integer)) for v in witness):
                a = list(witness)
                n = len(a)
                
        # If f is not explicitly provided, default to the +1 variant of Schur's polynomial
        # which can be reducible for some even n (e.g., n=4).
        if f is None and a is not None:
            f = sp.Integer(1)
            for val in a:
                f *= (x - val)
            f += 1
            
        if callable(f):
            try:
                f = f(x)
            except Exception:
                pass
                
        if isinstance(f, str):
            f = sp.sympify(f)
            
        # Check H1: n is a positive integer
        try:
            if isinstance(n, int) or (hasattr(n, 'is_integer') and n.is_integer):
                if n > 0:
                    h1_ok = True
        except Exception:
            pass
            
        # Check H2: a_1, a_2, ..., a_n are distinct integers
        try:
            if isinstance(a, (list, tuple)) and len(a) == n:
                all_ints = True
                for val in a:
                    if not (isinstance(val, int) or (hasattr(val, 'is_integer') and val.is_integer)):
                        all_ints = False
                        break
                if all_ints:
                    if len(set(a)) == n:
                        h2_ok = True
        except Exception:
            pass
            
        # Check neg_Q: f(x) is NOT irreducible over Q (i.e., it is reducible)
        try:
            if f is not None:
                if hasattr(f, 'free_symbols') and len(f.free_symbols) == 1:
                    gen = list(f.free_symbols)[0]
                    poly = sp.Poly(f, gen, domain='QQ')
                else:
                    poly = sp.Poly(f, x, domain='QQ')
                
                neg_q_ok = not poly.is_irreducible
        except Exception:
            pass
            
    except Exception:
        pass
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: a_1, a_2, ..., a_n are distinct integers",
    "¬Q: f(x) is not irreducible over Q"
]

N_HYP = 2
NEG_Q_INDEX = 2