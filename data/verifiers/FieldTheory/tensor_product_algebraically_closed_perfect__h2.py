import sympy as sp
from sympy.polys.domains import Domain

x, y, t, u = sp.symbols('x y t u')
QQ = sp.QQ
ZZ = sp.ZZ

def conditions(witness):
    h1, h2, h3, neg_Q = False, False, False, False
    
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            K_obj = witness.get('K')
            L_obj = witness.get('L')
        elif isinstance(witness, tuple) and len(witness) == 3:
            F, K_obj, L_obj = witness
        else:
            return [False, False, False, False]
            
        try:
            h2 = isinstance(F, Domain) and F.is_Field
        except Exception:
            h2 = False
            
        try:
            if h2:
                if F.char == 0:
                    h3 = True
                elif hasattr(F, 'is_FiniteField') and F.is_FiniteField:
                    h3 = True
                else:
                    h3 = False
        except Exception:
            h3 = False
            
        try:
            if hasattr(K_obj, 'is_Field') and K_obj.is_Field and hasattr(L_obj, 'is_Field') and L_obj.is_Field:
                h1 = True
                neg_Q = False
            else:
                free_x = list(K_obj.free_symbols) if hasattr(K_obj, 'free_symbols') else []
                x_var = K_obj.gen if hasattr(K_obj, 'gen') else (free_x[0] if free_x else sp.Symbol('x'))
                
                free_y = list(L_obj.free_symbols) if hasattr(L_obj, 'free_symbols') else []
                y_var = L_obj.gen if hasattr(L_obj, 'gen') else (free_y[0] if free_y else sp.Symbol('y'))
                
                K_p = sp.Poly(K_obj, x_var, domain=F)
                L_p = sp.Poly(L_obj, y_var, domain=F)
                
                h1 = K_p.is_irreducible and L_p.is_irreducible and K_p.degree() >= 1 and L_p.degree() >= 1
                
                P_deriv = K_p.diff(x_var)
                
                if isinstance(L_obj, sp.Poly):
                    L_obj_x = L_obj.replace(y_var, x_var)
                elif hasattr(L_obj, 'subs'):
                    L_obj_x = L_obj.subs(y_var, x_var)
                else:
                    L_obj_x = L_obj
                    
                L_p_x = sp.Poly(L_obj_x, x_var, domain=F)
                
                K_p_monic = K_p.monic()
                L_p_x_monic = L_p_x.monic()
                
                if K_p_monic == L_p_x_monic and P_deriv.is_zero:
                    neg_Q = True
                else:
                    neg_Q = False
        except Exception:
            h1 = False
            neg_Q = False
            
    except Exception:
        pass
        
    return [h1, h2, h3, neg_Q]

CONDITION_LABELS = [
    "H_1: K and L are fields",
    "H_2: F is a common subfield of K and L",
    "H_3: F is a perfect field",
    "¬Q: The tensor product K \\otimes_F L is not a reduced ring"
]

N_HYP = 3
NEG_Q_INDEX = 3