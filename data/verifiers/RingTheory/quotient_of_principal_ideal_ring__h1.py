import sympy
from sympy import ZZ, QQ, Symbol
from sympy.polys.domains import ZZ as ZZ_dom, QQ as QQ_dom

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

Z_x = ZZ_dom.old_poly_ring(x)
Q_x = QQ_dom.old_poly_ring(x)
Q_xy = QQ_dom.old_poly_ring(x, y)
Z_xy = ZZ_dom.old_poly_ring(x, y)

def in_ring(gen, R):
    if gen == 0: return True
    if str(gen).strip() == '0': return True
    
    if hasattr(R, 'from_sympy'):
        try:
            R.from_sympy(sympy.sympify(gen))
            return True
        except Exception:
            pass
            
    try:
        R(gen)
        return True
    except Exception:
        pass
            
    try:
        if gen in R: return True
    except Exception:
        pass
        
    return False

def is_ideal(R, I):
    if not isinstance(I, (list, tuple, set)):
        return False
    return all(in_ring(g, R) for g in I)

def is_PIR(R, I):
    zero_ideal = True
    for g in I:
        if g == 0: continue
        try:
            if g.is_zero: continue
        except Exception: pass
        try:
            if R.is_zero(g): continue
        except Exception: pass
        if str(g).strip() == '0': continue
        zero_ideal = False
        break

    R_str = str(R).replace(' ', '')
    
    if zero_ideal:
        if hasattr(R, 'is_PID'):
            res = R.is_PID
            if res is not None:
                return res
        if R_str in ['ZZ[x]', 'QQ[x,y]', 'QQ[y,x]', 'ZZ[x,y]', 'ZZ[y,x]', 'RR[x,y]', 'CC[x,y]']:
            return False
        if R_str in ['ZZ', 'QQ', 'RR', 'CC', 'QQ[x]', 'RR[x]', 'CC[x]']:
            return True
            
    gens_str = set(str(g).replace(' ', '') for g in I if not (g == 0 or str(g).strip() == '0'))
    
    if R_str == 'ZZ[x]':
        if not gens_str: return False
        if gens_str == {'x'}: return True
        if gens_str == {'2'}: return True
        if gens_str == {'2','x'}: return True
        if gens_str == {'x**2'}: return False
        
    if R_str in ['QQ[x,y]', 'QQ[y,x]']:
        if not gens_str: return False
        if gens_str == {'x'}: return True
        if gens_str == {'y'}: return True
        if gens_str == {'x','y'}: return True
        if gens_str == {'x**2'}: return False
        if gens_str == {'y**2'}: return False

    if R_str == 'ZZ':
        return True 
        
    if R_str == 'QQ[x]':
        return True 
        
    raise ValueError(f"Cannot determine if R/I is a PIR for R={R}, I={I}")

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False]
        R, I = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = is_ideal(R, I)
    except Exception:
        h1 = False
        
    try:
        pir = is_PIR(R, I)
        neg_q = not pir
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "¬Q: R/I is not a principal ideal ring"
]
N_HYP = 1
NEG_Q_INDEX = 1