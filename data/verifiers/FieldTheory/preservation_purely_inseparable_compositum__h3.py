import sympy
from sympy import symbols
from sympy.polys.domains import QQ
import math

# Top-level setup: named object bindings that the witness expression may reference.
# We provide symbols and a helper to easily construct fraction fields over QQ.
x, y, z = symbols('x y z')

def Field(*gens):
    """
    Helper to construct a field from generators over QQ.
    Example: Field(x, y) creates QQ(x, y).
    """
    if not gens:
        return QQ
    return QQ.frac_field(*gens)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness can be either:
      1. A tuple of 4 integers (L, F, E, K) representing degrees of finite fields over GF(p).
      2. A tuple of 4 SymPy domains or sets of generators representing fields.
    """
    try:
        if len(witness) != 4:
            return [False, False, False]
        L, F, E, K = witness
    except Exception:
        return [False, False, False]
        
    # Approach 1: Integer degrees of finite fields over a base field GF(p)
    try:
        if all(isinstance(val, int) for val in [L, F, E, K]):
            h1 = (L > 0)
            h2_a = (L % F == 0) and (L % E == 0) and (L % K == 0)
            h2_b = (E % F == 0) and (K % F == 0)
            h2 = h2_a and h2_b
            
            # The compositum of E and K has degree lcm(E, K)
            EK = (E * K) // math.gcd(E, K)
            
            # In finite fields, all extensions are separable.
            # Thus, EK is purely inseparable over K iff EK == K.
            neg_q = (EK != K)
            
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # Approach 2: SymPy domains or sets of generators
    try:
        def to_domain(obj):
            if hasattr(obj, 'is_Field'):
                return obj
            if hasattr(obj, 'from_sympy'):
                return obj
            if isinstance(obj, (list, tuple, set)):
                gens = list(obj)
                if not gens:
                    return QQ
                return QQ.frac_field(*gens)
            if obj == QQ:
                return QQ
            return QQ.frac_field(obj)
            
        def is_subfield(sub, sup):
            if sub == sup:
                return True
            
            sub_char = getattr(sub, 'char', 0)
            sup_char = getattr(sup, 'char', 0)
            if sub_char != sup_char:
                return False
                
            if sub == QQ:
                return True
                
            if getattr(sub, 'is_FiniteField', False):
                return True
                
            gens = []
            if hasattr(sub, 'gens'):
                gens = sub.gens
            elif hasattr(sub, 'ext'):
                try:
                    gens = [sub.to_sympy(sub.unit)]
                except Exception:
                    try:
                        gens = [sub.to_sympy(sub.gen)]
                    except Exception:
                        return False
            else:
                return False
                
            for g in gens:
                try:
                    if hasattr(sub, 'to_sympy'):
                        expr = sub.to_sympy(g)
                    else:
                        expr = g
                    sup.from_sympy(expr)
                except Exception:
                    return False
            return True

        def is_purely_inseparable(E_dom, K_dom):
            if is_subfield(E_dom, K_dom):
                return True
            
            p = getattr(K_dom, 'char', 0)
            if p == 0:
                # In characteristic 0, purely inseparable implies degree 1 (equal)
                return False
                
            if not hasattr(E_dom, 'gens'):
                return False
                
            for g in E_dom.gens:
                try:
                    if hasattr(E_dom, 'to_sympy'):
                        g_expr = E_dom.to_sympy(g)
                    else:
                        g_expr = g
                except Exception:
                    g_expr = g
                
                is_in = False
                for n in range(1, 6):
                    power = g_expr**(p**n)
                    try:
                        K_dom.from_sympy(power)
                        is_in = True
                        break
                    except Exception:
                        pass
                if not is_in:
                    return False
            return True

        L_dom = to_domain(L)
        F_dom = to_domain(F)
        E_dom = to_domain(E)
        K_dom = to_domain(K)
        
        h1 = getattr(L_dom, 'is_Field', True)
        
        h2_a = (getattr(F_dom, 'is_Field', True) and 
                getattr(E_dom, 'is_Field', True) and 
                getattr(K_dom, 'is_Field', True) and 
                is_subfield(F_dom, L_dom) and 
                is_subfield(E_dom, L_dom) and 
                is_subfield(K_dom, L_dom))
                
        h2_b = is_subfield(F_dom, E_dom) and is_subfield(F_dom, K_dom)
        h2 = h2_a and h2_b
        
        # The conclusion is that EK is purely inseparable over K.
        # This holds iff E is purely inseparable over K.
        neg_q = not is_purely_inseparable(E_dom, K_dom)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: L is a field",
    "H_2: F, E, and K are subfields of L such that F <= E and F <= K",
    "¬Q: EK is not purely inseparable over K"
]

N_HYP = 2
NEG_Q_INDEX = 2