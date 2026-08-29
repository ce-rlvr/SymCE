import sympy
from sympy import Symbol, Poly, Dummy, RootOf, factor_list
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard groups and matrices
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

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple of polynomials (f_E, f_K) representing the 
    minimal polynomials of the primitive elements of E and K over F.
    If a single polynomial is provided, it is assumed to be f_K, and E is assumed to be F.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f_E, f_K = witness
            elif len(witness) == 3:
                _, f_E, f_K = witness
            else:
                f_E = witness[0]
                f_K = witness[-1]
        else:
            f_E = Symbol('x')  # E = F
            f_K = witness
            
        if not hasattr(f_E, 'free_symbols') or not hasattr(f_K, 'free_symbols'):
            return [False, False, False]
            
        free_E = f_E.free_symbols
        x_E = list(free_E)[0] if free_E else Symbol('x')
        f_E_poly = Poly(f_E, x_E)
        
        free_K = f_K.free_symbols
        x_K = list(free_K)[0] if free_K else Symbol('x')
        f_K_poly = Poly(f_K, x_K)
        
        # Work over the fraction field of the domain (e.g., ZZ -> QQ)
        f_E_field = f_E_poly.set_domain(f_E_poly.domain.get_field())
        f_K_field = f_K_poly.set_domain(f_K_poly.domain.get_field())
        
        # H_1: F is a field
        # The fraction field of any valid polynomial domain is a field.
        h1 = True
        
        # H_2: E is a finite separable extension of F
        # This means f_E is irreducible and separable over F
        h2 = f_E_field.is_irreducible and f_E_field.degree() > 0 and f_E_field.gcd(f_E_field.diff()).degree() == 0
        
        # neg_Q: K is NOT a separable extension of F, OR K is NOT a Galois extension of F
        # First check if K is a separable extension
        k_separable = f_K_field.is_irreducible and f_K_field.degree() > 0 and f_K_field.gcd(f_K_field.diff()).degree() == 0
        
        if not k_separable:
            neg_q = True
        else:
            # If separable, check if it is Galois (splits completely in its own extension)
            y_sym = Dummy('y')
            try:
                if f_K_field.domain.is_FiniteField:
                    # Any finite separable extension of a finite field is Galois
                    k_galois = True
                else:
                    # Check if f_K splits into linear factors over F[x]/(f_K)
                    r = RootOf(f_K_field.as_expr(), 0)
                    factors = factor_list(f_K_field.as_expr().subs(x_K, y_sym), extension=r)[1]
                    k_galois = all(Poly(fac, y_sym).degree() == 1 for fac, mult in factors)
            except Exception:
                # If we cannot compute the Galois property, assume it is Galois to avoid false positives
                k_galois = True
                
            neg_q = not k_galois
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is a finite separable extension of F",
    "¬Q: K is not a separable extension of F, or K is not a Galois extension of F"
]

N_HYP = 2
NEG_Q_INDEX = 2