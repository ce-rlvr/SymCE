import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z, u, v, w
import math

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
    "H_1: a and b are elements of R",
    "H_2: d1 is a greatest common divisor of a and b",
    "H_3: d2 is a greatest common divisor of a and b",
    "¬Q: d1 and d2 are not associates (no unit u such that d1 = u d2)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_vars(witness):
    vars_set = set()
    def extract(obj):
        if hasattr(obj, 'free_symbols'):
            vars_set.update(obj.free_symbols)
        elif isinstance(obj, (list, tuple, set)):
            for item in obj:
                extract(item)
    extract(witness)
    return sorted(list(vars_set), key=lambda sym: sym.name)

def conditions(witness):
    try:
        if hasattr(witness, 'a') and hasattr(witness, 'd1') and hasattr(witness, 'elements'):
            a = witness.a
            b = witness.b
            d1 = witness.d1
            d2 = witness.d2
            
            def divides(x_val, y_val):
                return witness.divides(x_val, y_val)
                
            def is_gcd_custom(d, a_val, b_val):
                if not (divides(d, a_val) and divides(d, b_val)): 
                    return False
                for c in witness.elements:
                    if divides(c, a_val) and divides(c, b_val):
                        if not divides(c, d): 
                            return False
                return True
                
            h1 = True
            h2 = is_gcd_custom(d1, a, b)
            h3 = is_gcd_custom(d2, a, b)
            
            neg_q = True
            for u_elem in witness.elements:
                if witness.is_unit(u_elem):
                    if witness.eq(d1, witness.mul(u_elem, d2)):
                        neg_q = False
                        break
            return [h1, h2, h3, neg_q]
            
        if isinstance(witness, tuple):
            if len(witness) == 5:
                I, a, b, d1, d2 = witness
            elif len(witness) == 4:
                a, b, d1, d2 = witness
                I = []
            else:
                return [False] * 4
                
            if all(isinstance(val, (int, sympy.Integer)) for val in [a, b, d1, d2]):
                h1 = True
                def is_gcd_int(d, a_val, b_val):
                    return abs(int(d)) == math.gcd(int(a_val), int(b_val))
                h2 = is_gcd_int(d1, a, b)
                h3 = is_gcd_int(d2, a, b)
                neg_q = abs(int(d1)) != abs(int(d2))
                return [h1, h2, h3, neg_q]
                
            vars_list = get_vars(witness)
            if not vars_list:
                vars_list = [sympy.Symbol('x')]
                
            def divides_ideal(gens, expr):
                if expr == 0: 
                    return True
                if not gens: 
                    return expr == 0
                try:
                    G = sympy.groebner(list(gens) + list(I), *vars_list)
                    return sympy.reduced(expr, G)[1] == 0
                except Exception:
                    return False
                    
            def is_gcd_expr(d, a_val, b_val):
                if not (divides_ideal([d], a_val) and divides_ideal([d], b_val)):
                    return False
                return divides_ideal([a_val, b_val], d)
                
            h1 = True
            h2 = is_gcd_expr(d1, a, b)
            h3 = is_gcd_expr(d2, a, b)
            
            def are_associates(d1_val, d2_val):
                if not I:
                    try:
                        if d1_val == 0 and d2_val == 0: return True
                        if d1_val == 0 or d2_val == 0: return False
                        ratio = sympy.simplify(d1_val / d2_val)
                        return ratio.is_number and ratio != 0
                    except Exception:
                        return False
                try:
                    G = sympy.groebner(I, *vars_list)
                    r1 = sympy.reduced(d1_val, G)[1]
                    r2 = sympy.reduced(d2_val, G)[1]
                    if r1 == 0 and r2 == 0: return True
                    if r1 == 0 or r2 == 0: return False
                    
                    c1 = r1.as_coefficients_dict()
                    c2 = r2.as_coefficients_dict()
                    if set(c1.keys()) != set(c2.keys()): return False
                    ratios = set(c1[k] / c2[k] for k in c1)
                    return len(ratios) == 1
                except Exception:
                    return False
                    
            neg_q = not are_associates(d1, d2)
            return [h1, h2, h3, neg_q]
            
    except Exception:
        pass
        
    return [False, False, False, False]