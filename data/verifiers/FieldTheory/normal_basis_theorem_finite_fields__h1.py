import sympy
from sympy import Poly, Matrix
from sympy.abc import x
import itertools

CONDITION_LABELS = [
    "H_1: Let F_{q^n} be a finite extension of F_q of degree n",
    "¬Q: No element alpha exists such that its conjugates form a basis"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # Parse the witness which could be a polynomial defining the extension algebra
        if isinstance(witness, Poly):
            poly = witness
            domain = poly.domain
            if not domain.is_FiniteField:
                return [False, False]
            q = domain.order
            n = poly.degree()
        elif isinstance(witness, tuple) and len(witness) == 3:
            q, n, coeffs = witness
            domain = sympy.GF(q)
            poly = Poly(coeffs, x, domain=domain)
        elif isinstance(witness, list):
            q = 2
            n = len(witness) - 1
            domain = sympy.GF(q)
            poly = Poly(witness, x, domain=domain)
        elif isinstance(witness, tuple) and len(witness) == 2:
            # If witness is just (q, n), a normal basis always exists for valid finite fields
            q, n = witness
            return [n >= 1, False]
        else:
            return [False, False]
            
        H1 = (n >= 1)
        
        p = domain.characteristic
        # We iterate over all elements in the algebra F_q[x]/(poly)
        # For simplicity and speed, we check coefficients in the prime subfield
        elements = list(range(p))
            
        basis_exists = False
        for coeffs in itertools.product(elements, repeat=n):
            if all(c == 0 for c in coeffs):
                continue
            
            # Construct element alpha = c_0 + c_1*x + ... + c_{n-1}*x^{n-1}
            alpha = Poly(list(reversed(coeffs)), x, domain=domain)
            
            matrix_rows = []
            for k in range(n):
                # Compute alpha^{q^k} mod poly
                conj = alpha
                for _ in range(k):
                    conj = (conj**q) % poly
                
                # Extract coefficients to form a row vector
                row = [int(conj.nth(j)) for j in range(n)]
                matrix_rows.append(row)
            
            # Check if the n conjugates are linearly independent over F_q
            M = Matrix(matrix_rows)
            if M.det() % p != 0:
                basis_exists = True
                break
                
        neg_Q = not basis_exists
        return [H1, neg_Q]
    except Exception:
        return [False, False]