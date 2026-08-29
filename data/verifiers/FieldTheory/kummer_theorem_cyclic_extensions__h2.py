import sympy
from sympy.polys.polytools import Poly
from sympy.polys.domains import GF

x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for Kummer's Theorem for Cyclic Extensions
    where the hypothesis "the characteristic of K does not divide n" was dropped.
    
    The witness is expected to represent the base field K (a finite field F_p) and the 
    degree n of the extension. It can be provided as a tuple (p, n), a dictionary, 
    an integer p (implying n = p), or a SymPy Poly object representing the extension.
    """
    try:
        # Parse the witness to extract characteristic p and degree n
        if isinstance(witness, dict):
            p = int(witness.get('p', 2))
            n = int(witness.get('n', p))
        elif isinstance(witness, (tuple, list)):
            p = int(witness[0])
            n = int(witness[1])
        elif hasattr(witness, 'domain') and hasattr(witness.domain, 'mod'):
            p = int(witness.domain.mod)
            n = int(witness.degree())
        else:
            try:
                p = int(witness)
            except TypeError:
                if hasattr(witness, 'mod'):
                    p = int(witness.mod)
                elif hasattr(witness, 'p'):
                    p = int(witness.p)
                else:
                    return [False, False, False, False]
            n = p
            
        # H_1: Let K be a field.
        # We check if p is prime, which means F_p is a valid field.
        h1 = sympy.isprime(p)
        if not h1:
            return [False, False, False, False]
            
        if n <= 0:
            return [True, False, False, False]
            
        # H_2: Assume K contains a primitive n-th root of unity.
        # In characteristic p, if n == p, the p-th cyclotomic polynomial has 1 as a root,
        # which is often mistakenly accepted as a primitive root when the characteristic 
        # condition is dropped. Otherwise, F_p contains a primitive n-th root of unity 
        # if and only if n divides p - 1.
        h2 = (n == p) or ((p - 1) % n == 0)
        
        # H_3: Let L/K be a finite cyclic Galois extension of degree n.
        # For any prime p and integer n > 0, there exists a unique field extension 
        # F_{p^n} of F_p, which is always a cyclic Galois extension of degree n.
        h3 = True
        
        # ¬Q: The conclusion FAILS.
        # Conclusion: There exists an element a in K such that L = K(a^(1/n)) 
        # and the polynomial x^n - a is irreducible over K.
        # We check if there is ANY element a in F_p such that x^n - a is irreducible.
        # If none exists, the conclusion fails (neg_q = True).
        neg_q = True
        for a in range(p):
            poly = Poly(x**n - a, domain=GF(p))
            if poly.is_irreducible:
                neg_q = False
                break
                
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: K contains a primitive n-th root of unity",
    "H_3: L/K is a finite cyclic Galois extension of degree n",
    "¬Q: There is no element a in K such that L = K(a^(1/n)) and x^n - a is irreducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3