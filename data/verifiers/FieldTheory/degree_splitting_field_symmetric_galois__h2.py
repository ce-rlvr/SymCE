import sympy
import math
from sympy.combinatorics import SymmetricGroup, CyclicGroup

# Top-level setup for potential witness expressions
S1 = SymmetricGroup(1)
S2 = SymmetricGroup(2)
S3 = SymmetricGroup(3)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)

x, t = sympy.symbols('x t')

def conditions(witness):
    """
    Verifies that the witness is a valid counterexample to the conjecture.
    The conjecture fails because it omits the hypothesis that the polynomial is separable
    (or that the base field is perfect). Over a field of characteristic p > 0, we can have
    an inseparable extension where the degree is strictly greater than the size of the Galois group.
    """
    try:
        # Extract parameters
        p = int(witness.get('char', witness.get('p', 2)))
        n = int(witness.get('n', 2))
        f_sep = witness['f_sep']
        f_insep = witness['f_insep']
        x_sym = witness.get('x', x)
        t_sym = witness.get('t', t)
        
        # H_1: F is a field
        # We use F = GF(p)(t). We verify that p is a valid prime characteristic.
        h1 = sympy.isprime(p)
        
        # H_2: E is the splitting field of f(x) over F
        # We verify that f_sep is a valid polynomial over GF(p) and f_insep is purely inseparable over GF(p)(t).
        poly_sep = sympy.Poly(f_sep, x_sym, domain=sympy.GF(p))
        poly_insep = sympy.Poly(f_insep, x_sym)
        q = poly_insep.degree()
        
        is_power_of_p = False
        if q > 1 and p > 1:
            temp = q
            while temp % p == 0:
                temp //= p
            if temp == 1:
                is_power_of_p = True
                
        # Check if f_insep is exactly of the form x^q - t
        is_insep_form = sympy.simplify(f_insep - (x_sym**q - t_sym)) == 0
        
        h2 = is_power_of_p and is_insep_form and (poly_sep.degree() > 0)
        
        # H_3: The Galois group Gal(E/F) is isomorphic to the symmetric group S_n
        # The Galois group of E/F is determined entirely by the separable part f_sep over GF(p).
        # Since GF(p) is finite, the Galois group is cyclic.
        # A cyclic group can only be isomorphic to S_n if n=1 (trivial) or n=2 (Z_2).
        factors = poly_sep.factor_list()[1]
        degrees = [f[0].degree() for f in factors]
        lcm_deg = 1
        for d in degrees:
            lcm_deg = math.lcm(lcm_deg, d)
            
        if n == 1:
            h3 = (lcm_deg == 1)
        elif n == 2:
            h3 = (lcm_deg == 2)
        else:
            h3 = False
            
        # ¬Q: The degree of the extension is not equal to n!
        # The total degree of the splitting field is the product of the separable and purely inseparable degrees.
        E_degree = lcm_deg * q
        neg_q = (E_degree != math.factorial(n))
        
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is the splitting field of f(x) over F",
    "H_3: The Galois group Gal(E/F) is isomorphic to the symmetric group S_n",
    "¬Q: The degree of the extension is not equal to n!"
]

N_HYP = 3
NEG_Q_INDEX = 3