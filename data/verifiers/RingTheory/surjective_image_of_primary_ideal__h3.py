import sympy
from sympy import abc
from sympy.ntheory import factorint
import math

# Top-level setup
x = abc.x
y = abc.y
z = abc.z
QQ = sympy.S.Rationals
ZZ = sympy.S.Integers

CONDITION_LABELS = [
    "H_1: f is a surjective homomorphism of commutative rings",
    "H_2: Q is an ideal of R",
    "¬Q: The equivalence of Q being primary and f(Q) being primary fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Evaluates the witness for the conjecture.
    The witness is expected to be a tuple (n, q) representing:
      - R = Z (or QQ[x])
      - S = Z/nZ (or QQ[x]/<n>)
      - f: R -> S is the natural projection
      - Q = <q> is an ideal of R
    """
    try:
        if isinstance(witness, dict):
            if 'n' in witness and 'q' in witness:
                witness = (witness['n'], witness['q'])
            else:
                return [False, False, False]
                
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
            
        n, q = witness
        
        def is_int_like(val):
            if isinstance(val, int): return True
            if hasattr(val, 'is_integer') and val.is_integer: return True
            return False

        # Case 1: Witness over the integers Z
        if is_int_like(n) and is_int_like(q):
            n = abs(int(n))
            q = abs(int(q))
            
            h1 = True  # Natural projection is always a surjective homomorphism
            h2 = True  # qZ is always an ideal of Z
            
            def is_primary_Z(m):
                if m == 1: return False
                if m == 0: return True
                return len(factorint(m)) == 1
                
            q_prim = is_primary_Z(q)
            d = math.gcd(q, n) if n != 0 else q
            fq_prim = is_primary_Z(d)
            
            neg_q = (q_prim != fq_prim)
            return [h1, h2, neg_q]
            
        # Case 2: Witness over the polynomial ring QQ[x]
        elif hasattr(n, 'free_symbols') and hasattr(q, 'free_symbols'):
            syms = n.free_symbols | q.free_symbols
            if len(syms) > 1:
                return [False, False, False]
                
            h1 = True
            h2 = True
            
            def is_primary_poly(poly):
                poly = sympy.sympify(poly)
                if poly.is_zero: return True
                if not poly.free_symbols: return False
                factors = sympy.factor_list(poly, domain='QQ')[1]
                return len(factors) == 1
                
            q_prim = is_primary_poly(q)
            d = sympy.gcd(q, n)
            fq_prim = is_primary_poly(d)
            
            neg_q = (q_prim != fq_prim)
            return [h1, h2, neg_q]
            
        else:
            return [False, False, False]
            
    except Exception:
        return [False, False, False]