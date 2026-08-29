import sympy
from sympy import sympify, gcd, groebner
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: pi is the canonical projection homomorphism",
    "H_3: f is a polynomial over R",
    "not Q: The content ideal of pi(f) is NOT equal to the projection of c(f)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False, False, False, False]
            
        vars_syms, I_gens, f_coeffs = witness
        
        if not isinstance(vars_syms, (list, tuple)):
            return [False, False, False, False]
        if not isinstance(I_gens, (list, tuple)):
            return [False, False, False, False]
        if not isinstance(f_coeffs, (list, tuple)) or len(f_coeffs) == 0:
            return [False, False, False, False]
            
        vars_syms = [sympify(v) for v in vars_syms]
        I_gens = [sympify(g) for g in I_gens]
        f_coeffs = [sympify(c) for c in f_coeffs]
        
        h1 = all(isinstance(v, sympy.Symbol) for v in vars_syms)
        
        allowed_symbols = set(vars_syms)
        h2 = all(g.free_symbols.issubset(allowed_symbols) for g in I_gens)
        
        h3 = all(c.free_symbols.issubset(allowed_symbols) for c in f_coeffs)
        
        if not (h1 and h2 and h3):
            return [h1, h2, h3, False]
            
        c_f = f_coeffs[0]
        for c in f_coeffs[1:]:
            c_f = gcd(c_f, c)
            
        A_I = list(f_coeffs) + list(I_gens)
        B_I = [c_f] + list(I_gens)
        
        if not vars_syms:
            A_zero = all(g == 0 for g in A_I)
            B_zero = all(g == 0 for g in B_I)
            neg_q = (A_zero != B_zero)
        else:
            gb_A = groebner(A_I, *vars_syms, domain='QQ')
            gb_B = groebner(B_I, *vars_syms, domain='QQ')
            neg_q = (list(gb_A) != list(gb_B))
            
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]