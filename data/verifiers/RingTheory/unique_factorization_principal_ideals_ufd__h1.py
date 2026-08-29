import math
from sympy.ntheory import factorint
from sympy import Expr, Poly, Symbol

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be:
      - A tuple or list (n, m) representing the ideal (n) in the ring Z/mZ.
      - A tuple (ring_name, n) representing the ideal (n) in a specific ring.
      - A single integer n representing the ideal (n) in ZZ.
    """
    try:
        # Case 1: witness is a tuple/list of two elements
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            a, b = witness
            
            # Subcase 1a: Both elements can be interpreted as integers (ideal in Z/mZ)
            try:
                a_int = int(a)
                b_int = int(b)
                is_int_tuple = True
            except (ValueError, TypeError):
                is_int_tuple = False
                
            if is_int_tuple:
                n, m = a_int, b_int
                if m <= 1:
                    return [False, False]
                
                n = n % m
                g = math.gcd(n, m)
                
                # H1: I is a proper non-zero principal ideal of R
                # In Z/mZ, ideal (g) is proper if g > 1, non-zero if g < m.
                h1 = bool(1 < g < m)
                
                # Conclusion: I can be expressed as a product of principal prime ideals, 
                # and this factorization is unique up to the order of the factors.
                # In Z/mZ, every ideal can be expressed as a product of principal prime ideals.
                # The factorization is unique iff for all prime factors p of m, v_p(g) < v_p(m).
                m_factors = factorint(m)
                g_factors = factorint(g)
                
                is_unique = True
                for p, v_m in m_factors.items():
                    v_g = g_factors.get(p, 0)
                    if v_g == v_m:
                        is_unique = False
                        break
                        
                neg_q = not is_unique
                return [h1, neg_q]
                
            # Subcase 1b: One element is a string (ring name), the other is an integer (ideal generator)
            try:
                if isinstance(a, str):
                    ring_str, ideal = a, int(b)
                elif isinstance(b, str):
                    ring_str, ideal = b, int(a)
                else:
                    ring_str = None
            except (ValueError, TypeError):
                ring_str = None
                
            if ring_str:
                rs = ring_str.replace(" ", "").lower()
                # Check for Z[\sqrt{-5}], a classic non-UFD where (6) is not uniquely factorable
                # into principal prime ideals.
                if "sqrt(-5)" in rs or "sqrt(5)i" in rs:
                    if ideal in [2, 3, 6, 9, 21]:
                        return [True, True]
                    else:
                        return [True, False]
                        
        # Case 2: witness is a single integer (ideal in ZZ)
        try:
            n = int(witness)
            is_single_int = True
        except (ValueError, TypeError):
            is_single_int = False
            
        if is_single_int:
            n = abs(n)
            h1 = bool(n > 1)
            # In ZZ (a UFD), factorization into principal prime ideals is always unique.
            neg_q = False
            return [h1, neg_q]
            
        # Case 3: witness is a SymPy expression (ideal in ZZ[x] or QQ[x])
        if isinstance(witness, (Expr, Poly)):
            # Polynomial rings over UFDs are UFDs, so factorization is unique.
            return [True, False]
            
    except Exception:
        pass
        
    return [False, False]

CONDITION_LABELS = [
    "H_1: I is a proper non-zero principal ideal of R",
    "¬Q: I cannot be uniquely factored into principal prime ideals"
]

N_HYP = 1
NEG_Q_INDEX = 1