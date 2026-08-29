import sympy
from sympy import symbols, Poly, isprime
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is an irreducible polynomial over F",
    "H_3: The degree of f(x) is n",
    "H_4: K is the splitting field of f(x) over F",
    "¬Q: Gal(K/F) does not act faithfully and transitively on n roots"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        p = witness.get('p')
        n = witness.get('n')
        f = witness.get('f')
        x_var = witness.get('x')
        t_var = witness.get('t')
        
        if p is None or n is None or f is None or x_var is None or t_var is None:
            return [False, False, False, False, False]
            
        # H1: F is a field
        # We use F = F_p(t), which is a field if p is prime.
        h1 = isprime(p) and hasattr(x_var, 'is_Symbol') and x_var.is_Symbol and hasattr(t_var, 'is_Symbol') and t_var.is_Symbol and p > 0
        
        if not h1:
            return [False, False, False, False, False]
            
        # Create polynomial in F_p[x, t]
        f_poly = Poly(f, x_var, t_var, domain='FF(' + str(p) + ')')
        
        # H2: f(x) is an irreducible polynomial over F
        # For F = F_p(t), a polynomial in F_p[x, t] is irreducible in F_p(t)[x] 
        # if it is irreducible in F_p[x, t] and has positive degree in x.
        h2 = bool(f_poly.is_irreducible) and (f_poly.degree(x_var) > 0)
        
        # H3: The degree of f(x) is n
        h3 = (f_poly.degree(x_var) == n)
        
        # H4: K is the splitting field of f(x) over F
        h4 = bool(witness.get('K_is_splitting_field', False))
        
        # ¬Q: Gal(K/F) does not embed as a transitive subgroup of S_n
        # This occurs if and only if f(x) is inseparable over F (gcd(f, f') != 1).
        # In this case, the number of distinct roots is strictly less than n,
        # so the Galois group cannot act faithfully and transitively on n distinct roots.
        f_diff = f_poly.diff(x_var)
        g = f_poly.gcd(f_diff)
        neg_q = (g.degree(x_var) > 0)
        
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False, False, False, False, False]