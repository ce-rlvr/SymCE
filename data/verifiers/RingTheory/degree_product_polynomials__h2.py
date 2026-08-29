import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

# Standard algebra objects
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

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: The degree of the product f(x)g(x) is not equal to the sum of the degrees of f(x) and g(x)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f, g = witness
            elif len(witness) == 3:
                _, f, g = witness
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: R is an integral domain
    try:
        h1_ok = True
        
        if getattr(f, 'is_Matrix', False) or getattr(g, 'is_Matrix', False):
            h1_ok = False
            
        for expr in (f, g):
            if hasattr(expr, 'domain') and hasattr(expr.domain, 'is_IntegralDomain'):
                if not expr.domain.is_IntegralDomain:
                    h1_ok = False
                    
            if hasattr(expr, 'is_commutative') and expr.is_commutative is False:
                h1_ok = False
                
            if hasattr(expr, 'free_symbols'):
                for sym in expr.free_symbols:
                    if hasattr(sym, 'is_commutative') and sym.is_commutative is False:
                        h1_ok = False
                        
            if hasattr(expr, 'atoms'):
                for atom in expr.atoms(sp.Mod):
                    if len(atom.args) == 2:
                        modulus = atom.args[1]
                        if modulus.is_Integer and not sp.isprime(modulus):
                            h1_ok = False
    except Exception:
        h1_ok = False

    # ¬Q: deg(f*g) != deg(f) + deg(g)
    try:
        syms = set()
        for expr in (f, g):
            if hasattr(expr, 'free_symbols'):
                syms.update(expr.free_symbols)
        
        syms = list(syms)
        if syms:
            syms.sort(key=lambda s: s.name)
            var = syms[0]
        else:
            var = sp.Symbol('x')
            
        def get_deg(expr, v):
            if hasattr(expr, 'is_zero') and expr.is_zero:
                raise ValueError("Undefined degree")
            if expr == 0:
                raise ValueError("Undefined degree")
            
            expr_expanded = sp.expand(expr)
            if expr_expanded == 0:
                raise ValueError("Undefined degree")
                
            return sp.degree(expr_expanded, v)
            
        deg_f = get_deg(f, var)
        deg_g = get_deg(g, var)
        deg_fg = get_deg(f * g, var)
        
        q_ok = (deg_fg == deg_f + deg_g)
    except Exception:
        # If degree is undefined (e.g., zero polynomial), the equation fails
        q_ok = False

    neg_q = not q_ok

    return [h1_ok, neg_q]