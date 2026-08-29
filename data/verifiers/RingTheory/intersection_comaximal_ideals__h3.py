import sympy
import math

# Top-level setup
x, y, z = sympy.symbols('x y z')

def is_int(val):
    if isinstance(val, int):
        return True
    if isinstance(val, sympy.Integer):
        return True
    return False

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                I_obj, J_obj = witness
            elif len(witness) == 3:
                _, I_obj, J_obj = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        def get_gen(obj):
            if is_int(obj):
                return int(obj), 'Z'
            elif isinstance(obj, sympy.Expr):
                return obj, 'Q[x]'
            elif isinstance(obj, (list, tuple, set)):
                obj = list(obj)
                if not obj:
                    return 0, 'Z'
                if all(is_int(v) for v in obj):
                    val = int(obj[0])
                    for g in obj[1:]:
                        val = math.gcd(val, int(g))
                    return val, 'Z'
                elif all(isinstance(v, sympy.Expr) for v in obj):
                    val = obj[0]
                    for g in obj[1:]:
                        val = sympy.gcd(val, g)
                    return val, 'Q[x]'
            return None, None

        I_gen, type_I = get_gen(I_obj)
        J_gen, type_J = get_gen(J_obj)
        
        if type_I is not None and type_J is not None and type_I == type_J:
            if type_I == 'Z':
                h1 = True
                h2 = True
                
                intersect_gen = abs((I_gen * J_gen) // math.gcd(I_gen, J_gen)) if I_gen or J_gen else 0
                prod_gen = abs(I_gen * J_gen)
                
                neg_q = (intersect_gen != prod_gen)
                
            elif type_I == 'Q[x]':
                h1 = True
                h2 = True
                
                intersect_gen = sympy.lcm(I_gen, J_gen)
                prod_gen = sympy.expand(I_gen * J_gen)
                
                if sympy.simplify(prod_gen) == 0:
                    neg_q = (sympy.simplify(intersect_gen) != 0)
                else:
                    ratio = sympy.cancel(intersect_gen / prod_gen)
                    neg_q = not ratio.is_constant()
                    
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I and J are ideals of R",
    "¬Q: I \\cap J is not equal to IJ"
]

N_HYP = 2
NEG_Q_INDEX = 2