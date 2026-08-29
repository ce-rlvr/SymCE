import sympy as sp
import math

j = sp.Symbol('j')

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is the ring of split-complex numbers over R",
    "¬Q: a+bj is a unit in S iff a^2-b^2 is a unit in R is false"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R_ring, a_expr, b_expr = witness
            elif len(witness) == 2:
                R_ring = 'QQ'
                a_expr, b_expr = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        a = sp.sympify(a_expr, locals={'j': j})
        b = sp.sympify(b_expr, locals={'j': j})
        
        h1 = True
        h2 = True
        
        def get_AB(expr):
            e1 = expr.subs(j, 1)
            em1 = expr.subs(j, -1)
            A = sp.simplify((e1 + em1) / 2)
            B = sp.simplify((e1 - em1) / 2)
            return A, B
            
        def is_unit(val, ring):
            if str(ring) == 'ZZ' or ring == sp.ZZ:
                return sp.simplify(val) in [1, -1]
            elif isinstance(ring, int) and ring > 1:
                try:
                    val_int = int(sp.simplify(val)) % ring
                    return math.gcd(val_int, ring) == 1
                except TypeError:
                    return False
            return sp.simplify(val) != 0
            
        E = sp.simplify(a + b*j)
        A_E, B_E = get_AB(E)
        norm_E = sp.simplify(A_E**2 - B_E**2)
        E_is_unit = is_unit(norm_E, R_ring)
        
        N = sp.simplify(a**2 - b**2)
        A_N, B_N = get_AB(N)
        N_in_R = (sp.simplify(B_N) == 0)
        N_is_unit = N_in_R and is_unit(A_N, R_ring)
        
        neg_q = (E_is_unit != N_is_unit)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]