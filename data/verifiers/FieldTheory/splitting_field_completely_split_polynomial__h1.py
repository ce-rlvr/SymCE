import sympy
from sympy import Symbol, Poly

CONDITION_LABELS = [
    "H_1: f is a non-constant polynomial over F",
    "H_2: K is the splitting field of f over F",
    "¬Q: K equals F iff f factors completely into linear polynomials over F is false"
]

N_HYP = 2
NEG_Q_INDEX = 2

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        F, K, f = witness
    except Exception:
        return [False, False, False]
        
    try:
        if not isinstance(f, sympy.Expr):
            f = sympy.sympify(f)
        free_syms = list(f.free_symbols)
        x = free_syms[0] if free_syms else Symbol('x')
        poly_f = Poly(f, x)
        is_non_constant = poly_f.degree() >= 1
        coeffs_in_F = all(c in F for c in poly_f.coeffs())
        h1 = bool(is_non_constant and coeffs_in_F)
    except Exception:
        h1 = False
        
    try:
        if not getattr(K, 'is_Field', False):
            h2 = False
        else:
            frac_F = F.get_field()
            rts = sympy.roots(f, x)
            splits = (sum(rts.values()) == poly_f.degree())
            
            if not splits:
                h2 = False
            else:
                roots_in_frac = all(r in frac_F for r in rts.keys())
                if roots_in_frac:
                    h2 = bool(K == frac_F)
                else:
                    h2 = bool(all(r in K for r in rts.keys()))
    except Exception:
        h2 = False
        
    try:
        k_eq_f = bool(K == F)
        
        const, factors = sympy.factor_list(f, domain=F)
        factors_completely = all(p.as_poly(x).degree() == 1 for p, mult in factors)
        
        conclusion = (k_eq_f == factors_completely)
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]