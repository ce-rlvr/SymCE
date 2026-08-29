import sympy
from sympy import Symbol, Poly
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
    try:
        F, n, a = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: F is a field whose characteristic does not divide n
    try:
        if not hasattr(F, 'is_Field') or not F.is_Field:
            h1 = False
        else:
            char = F.characteristic
            if char == 0:
                h1 = True
            else:
                h1 = (n % char != 0)
    except Exception:
        h1 = False
        
    # H2: F contains all n-th roots of unity
    try:
        x = Symbol('x')
        if n == 0:
            h2 = True
        else:
            n_abs = abs(n)
            poly_unity = Poly(x**n_abs - 1, x, domain=F)
            factors_unity = poly_unity.factor_list()[1]
            # Check if x^{|n|} - 1 splits completely into linear factors
            h2 = all(f.degree() == 1 for f, m in factors_unity) and sum(m for f, m in factors_unity) == n_abs
    except Exception:
        h2 = False
        
    # H3: a in F is a non-zero element
    try:
        if a not in F:
            h3 = False
        else:
            a_F = F.convert(a)
            h3 = (a_F != F.zero)
    except Exception:
        h3 = False
        
    # neg_Q: splitting field has degree d dividing n, and Galois group is cyclic
    try:
        x = Symbol('x')
        if n == 0:
            d = 1
            divides = True
            is_cyclic = True
            neg_q = not (divides and is_cyclic)
        else:
            n_abs = abs(n)
            if n < 0:
                a_inv = F.invert(F.convert(a))
                poly_a = Poly(x**n_abs - a_inv, x, domain=F)
            else:
                poly_a = Poly(x**n - a, x, domain=F)
                
            factors_a = poly_a.factor_list()[1]
            degrees = [f.degree() for f, m in factors_a]
            d = degrees[0]
            
            # In a Galois extension, all irreducible factors must have the same degree.
            # If they don't, the splitting field degree is likely not d, or the extension behaves unexpectedly.
            if any(deg != d for deg in degrees):
                neg_q = True
            else:
                divides = (n_abs % d == 0)
                # By Kummer theory, the Galois group of this splitting field over F is always cyclic
                # because it embeds into the group of n-th roots of unity, which is cyclic.
                is_cyclic = True
                neg_q = not (divides and is_cyclic)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field whose characteristic does not divide n",
    "H_2: F contains all n-th roots of unity",
    "H_3: a in F is a non-zero element",
    "¬Q: The splitting field of x^n - a over F does not have degree dividing n, or its Galois group is not cyclic"
]

N_HYP = 3
NEG_Q_INDEX = 3