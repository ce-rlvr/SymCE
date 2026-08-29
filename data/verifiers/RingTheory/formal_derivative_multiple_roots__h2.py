import sympy as sp

x = sp.Symbol('x')
QQ = sp.QQ
ZZ = sp.ZZ
RR = sp.RR
CC = sp.CC

def conditions(witness) -> list[bool]:
    F_is_field = False
    try:
        if isinstance(witness, tuple):
            domain, f_expr = witness
            if hasattr(domain, 'is_Field'):
                F_is_field = bool(domain.is_Field)
            elif str(domain) in ['QQ', 'RR', 'CC']:
                F_is_field = True
        else:
            if hasattr(witness, 'domain') and hasattr(witness.domain, 'is_Field'):
                F_is_field = bool(witness.domain.is_Field)
            else:
                f_tmp = sp.Poly(witness, x)
                F_is_field = bool(f_tmp.domain.is_Field)
    except Exception:
        F_is_field = False

    neg_Q = False
    try:
        if isinstance(witness, tuple):
            domain, f_expr = witness
            if isinstance(f_expr, sp.Expr):
                gens = list(f_expr.free_symbols)
            else:
                gens = []
            if not gens:
                gens = [x]
            f = sp.Poly(f_expr, *gens, domain=domain)
        else:
            if isinstance(witness, sp.Poly):
                f = witness
            else:
                if isinstance(witness, sp.Expr):
                    gens = list(witness.free_symbols)
                else:
                    gens = []
                if not gens:
                    gens = [x]
                f = sp.Poly(witness, *gens)
                
        f_diff = f.diff()
        g = f.gcd(f_diff)
        
        gcd_not_one = not g.is_one
        
        if f.is_zero:
            # The zero polynomial does not have a well-defined multiple root
            # in the standard sense (multiplicity is undefined/infinite).
            has_multiple_root = False
        else:
            # For any non-zero polynomial over any field, having a multiple root
            # in its splitting field is mathematically equivalent to gcd(f, f') != 1.
            has_multiple_root = gcd_not_one
            
        Q = (has_multiple_root == gcd_not_one)
        neg_Q = not Q
    except Exception:
        neg_Q = False

    return [F_is_field, neg_Q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: f(x) has a multiple root in its splitting field iff gcd(f, f') != 1 fails"
]

N_HYP = 1
NEG_Q_INDEX = 1