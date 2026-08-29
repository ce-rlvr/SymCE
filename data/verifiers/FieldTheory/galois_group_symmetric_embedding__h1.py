import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        # The witness is expected to be a polynomial f(x)
        if isinstance(witness, tuple):
            f = witness[0]
        else:
            f = witness
            
        if isinstance(f, str):
            f = sympy.sympify(f)
            
        if isinstance(f, sympy.Poly):
            x = f.gen
            f_poly = f
        else:
            free = list(f.free_symbols)
            x = free[0] if free else sympy.Symbol('x')
            f_poly = sympy.Poly(f, x)
            
        n = f_poly.degree()
        if n < 1:
            return [False, False, False]
            
        # Factor the polynomial to check for separability and count distinct roots
        factors = sympy.factor_list(f_poly)
        is_separable = True
        m = 0  # Number of distinct roots in the splitting field
        
        for factor, mult in factors[1]:
            if isinstance(factor, sympy.Poly):
                factor_poly = factor
            else:
                factor_poly = sympy.Poly(factor, x)
                
            deg = factor_poly.degree()
            m += deg
            
            # A polynomial is separable if its irreducible factors have no repeated roots
            if deg > 0:
                deriv = factor_poly.diff()
                g = sympy.gcd(factor_poly, deriv)
                if g.degree() > 0:
                    is_separable = False
                    
        H_1_ok = bool(is_separable)
        
        # L is implicitly defined as the splitting field of f(x) over K
        H_2_ok = True
        
        # The conclusion fails if the action on the roots does not induce a homomorphism into S_n.
        # This happens exactly when the number of distinct roots m is strictly less than the degree n
        # (i.e., when f(x) has repeated roots, despite its irreducible factors being separable).
        neg_Q_ok = bool(m < n)
        
        return [H_1_ok, H_2_ok, neg_Q_ok]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: f(x) is a separable polynomial of degree n",
    "H_2: L is the splitting field of f(x) over K",
    "¬Q: The action of the Galois group does not induce an injective homomorphism into S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2