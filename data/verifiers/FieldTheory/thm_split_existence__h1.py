import sympy
from sympy import Poly, Matrix, Expr, Symbol, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.ntheory

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = ["H_1: f is a non-constant polynomial over F", "not Q: There does not exist a splitting field for f over F"]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1_ok = False
    neg_q = False
    
    try:
        def is_non_constant_mod(coeffs, n):
            try:
                coeffs_mod = [int(c) % n for c in coeffs]
                while coeffs_mod and coeffs_mod[0] == 0:
                    coeffs_mod.pop(0)
                return len(coeffs_mod) > 1
            except Exception:
                return False

        # Format 1: list of sympy Matrices (coefficients of polynomial, lowest to highest degree)
        if isinstance(witness, list) and len(witness) > 0 and hasattr(witness[0], 'is_Matrix') and witness[0].is_Matrix:
            coeffs = list(witness)
            while coeffs and coeffs[-1].is_zero_matrix:
                coeffs.pop()
            
            if len(coeffs) > 1:
                h1_ok = True
            
            # A matrix ring of size > 1 has zero divisors, so it cannot be embedded in a field.
            if len(coeffs) > 0 and coeffs[0].shape[0] > 1:
                neg_q = True
                
        # Format 2: tuple (domain_info, poly_info) representing a polynomial over a specific ring
        elif isinstance(witness, tuple) and len(witness) == 2:
            domain_info, poly_info = witness
            
            n = None
            if isinstance(domain_info, int):
                n = domain_info
            elif isinstance(domain_info, str):
                digits = ''.join(c for c in domain_info if c.isdigit())
                if digits:
                    n = int(digits)
            elif hasattr(domain_info, 'order'):
                try:
                    n = int(domain_info.order())
                except Exception:
                    pass
            
            if n is not None and n > 1:
                if isinstance(poly_info, list):
                    if is_non_constant_mod(poly_info, n):
                        h1_ok = True
                elif isinstance(poly_info, Expr) or isinstance(poly_info, str):
                    x = Symbol('x')
                    p = Poly(poly_info, x)
                    coeffs = p.all_coeffs()
                    if is_non_constant_mod(coeffs, n):
                        h1_ok = True
                elif hasattr(poly_info, 'is_Poly') and poly_info.is_Poly:
                    coeffs = poly_info.all_coeffs()
                    if is_non_constant_mod(coeffs, n):
                        h1_ok = True
                
                # Z_n can be embedded in a field if and only if n is prime.
                if not sympy.ntheory.isprime(n):
                    neg_q = True

        # Format 3: sympy Poly (assumes domain is an integral domain)
        elif hasattr(witness, 'is_Poly') and witness.is_Poly:
            if witness.degree() > 0:
                h1_ok = True
            neg_q = False
            
        # Format 4: sympy Expr (assumes domain is an integral domain like Z or Q)
        elif isinstance(witness, Expr):
            x = Symbol('x')
            p = Poly(witness, x)
            if p.degree() > 0:
                h1_ok = True
            neg_q = False
            
    except Exception:
        pass

    return [h1_ok, neg_q]