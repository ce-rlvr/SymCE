import sympy
from sympy import Poly
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    try:
        if isinstance(witness, Poly):
            f = witness
        else:
            free_symbols = witness.free_symbols
            if len(free_symbols) != 1:
                return [False, False]
            sym = list(free_symbols)[0]
            f = Poly(witness, sym)
    except Exception:
        return [False, False]
    
    try:
        h1 = f.degree() > 0
    except Exception:
        h1 = False

    try:
        f_prime = f.diff()
        g = f.gcd(f_prime)
        
        try:
            F_frac = f.domain.get_field()
            f_field = f.set_domain(F_frac)
            f_prime_field = f_prime.set_domain(F_frac)
            g_field = f_field.gcd(f_prime_field)
            has_multiple_root = (g_field.degree() > 0)
        except Exception:
            has_multiple_root = (f.discriminant() == 0)
            
        if g.degree() == 0:
            if f.domain.is_Field:
                gcd_is_one = True
            else:
                g_expr = g.as_expr()
                gcd_is_one = (g_expr == 1 or g_expr == -1)
        else:
            gcd_is_one = False
            
        gcd_not_one = not gcd_is_one
        
        q = (has_multiple_root == gcd_not_one)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a non-constant polynomial",
    "¬Q: The equivalence between having a multiple root and gcd not equal to 1 fails"
]

N_HYP = 1
NEG_Q_INDEX = 1