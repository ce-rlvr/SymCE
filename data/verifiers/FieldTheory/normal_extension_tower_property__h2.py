import sympy
from sympy import Dummy, minpoly, QQ, sympify
from sympy.polys.polytools import factor_list
from sympy.polys.numberfields import primitive_element
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def extract_gen(obj):
    if obj == QQ:
        return sympy.S.One
    if hasattr(obj, 'ext'):
        return obj.ext
    return sympify(obj)

def get_field(gen):
    gen = sympify(gen)
    if gen.is_Rational:
        return QQ
    return QQ.algebraic_field(gen)

def is_subfield(sub_obj, super_obj):
    sub_gen = extract_gen(sub_obj)
    super_gen = extract_gen(super_obj)
    
    if sub_gen.is_Rational:
        return True
    if super_gen.is_Rational:
        return sub_gen.is_Rational
        
    x = Dummy('x')
    try:
        deg_super = minpoly(super_gen, x).degree()
        poly_both, _ = primitive_element([sub_gen, super_gen], x)
        deg_both = poly_both.degree()
        return deg_both == deg_super
    except Exception:
        return False

def is_normal_extension(L_obj, K_obj):
    L_gen = extract_gen(L_obj)
    K_gen = extract_gen(K_obj)
    
    if not is_subfield(K_gen, L_gen):
        return False
        
    if L_gen.is_Rational:
        return True
        
    x = Dummy('x')
    try:
        minpoly_L = minpoly(L_gen, x)
        K_field = get_field(K_gen)
        
        _, factors_K = factor_list(minpoly_L, domain=K_field)
        
        minpoly_L_K = None
        for fac, _ in factors_K:
            val = fac.subs(x, L_gen)
            if val == 0 or val.simplify() == 0:
                minpoly_L_K = fac
                break
            try:
                if abs(complex(val.evalf())) < 1e-9:
                    minpoly_L_K = fac
                    break
            except Exception:
                pass
                
        if minpoly_L_K is None:
            return False
            
        L_field = get_field(L_gen)
        _, factors_L = factor_list(minpoly_L_K, domain=L_field)
        
        for fac, _ in factors_L:
            if fac.as_poly(x).degree() > 1:
                return False
                
        return True
    except Exception:
        return False

def conditions(witness):
    """
    witness: A dictionary {'E': ..., 'K': ..., 'L': ...} or a tuple (E, K, L)
    representing the primitive elements of the fields over Q, or their Galois groups.
    """
    if isinstance(witness, dict):
        E = witness.get('E')
        K = witness.get('K')
        L = witness.get('L')
    else:
        try:
            E, K, L = witness
        except Exception:
            return [False, False]
            
    # H_1: L/K is a normal field extension
    try:
        if isinstance(L, PermutationGroup) and isinstance(K, PermutationGroup):
            # By Galois correspondence, L/K is normal iff H_L is a normal subgroup of H_K
            h1 = L.is_subgroup(K) and K.is_normal(L)
        else:
            h1 = is_normal_extension(L, K)
    except Exception:
        h1 = False
        
    # ¬Q: The extension L/E is NOT a normal extension
    try:
        if isinstance(L, PermutationGroup) and isinstance(E, PermutationGroup):
            is_ext = L.is_subgroup(E)
            is_norm = E.is_normal(L)
            neg_q = not (is_ext and is_norm)
        else:
            is_ext = is_subfield(E, L)
            if not is_ext:
                # If E is not a subfield of L, L/E is not an extension, so it cannot be a normal extension
                neg_q = True
            else:
                neg_q = not is_normal_extension(L, E)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: L/K is a normal field extension",
    "¬Q: The extension L/E is not a normal extension"
]

N_HYP = 1
NEG_Q_INDEX = 1