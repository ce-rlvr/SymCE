import sympy
from sympy.polys.domains import QQ as sympy_QQ, CC as sympy_CC, FractionField, AlgebraicField
from sympy.abc import x

class MathField:
    def __init__(self, name, is_field=True, is_alg_closed=False, char=0, over=None, is_finite_ext=True, is_separable=True):
        self.name = name
        self.is_field = is_field
        self.is_alg_closed = is_alg_closed
        self.char = char
        self.over = over
        self.is_finite_ext = is_finite_ext
        self.is_separable = is_separable

    def contains(self, other):
        if self == other:
            return True
        curr = other
        while curr is not None:
            if self == curr:
                return True
            if self.name == 'CC' and 'QQ' in curr.name:
                return True
            if self.name == 'F2_alg' and 'F2' in curr.name:
                return True
            if hasattr(curr, 'over'):
                curr = curr.over
            else:
                break
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

# Top-level setup: Standard fields and extensions for witnesses
QQ = MathField('QQ', is_alg_closed=False, char=0, over=None)
CC = MathField('CC', is_alg_closed=True, char=0, over=QQ, is_finite_ext=False)
QQ_pi = MathField('QQ(pi)', is_alg_closed=False, char=0, over=QQ, is_finite_ext=False)
QQ_x = MathField('QQ(x)', is_alg_closed=False, char=0, over=QQ, is_finite_ext=False)
QQ_sqrt2 = MathField('QQ(sqrt(2))', is_alg_closed=False, char=0, over=QQ, is_finite_ext=True)

F2 = MathField('F2', is_alg_closed=False, char=2)
F2_t = MathField('F2(t)', is_alg_closed=False, char=2, over=F2, is_finite_ext=False)
F2_t_sqrt_t = MathField('F2(t)(sqrt(t))', is_alg_closed=False, char=2, over=F2_t, is_finite_ext=True, is_separable=False)
F2_alg = MathField('F2_alg', is_alg_closed=True, char=2, over=F2, is_finite_ext=False)

def parse_field(f):
    if isinstance(f, MathField):
        return f
    if isinstance(f, str):
        mapping = {
            'QQ': QQ,
            'CC': CC,
            'QQ(pi)': QQ_pi,
            'QQ(x)': QQ_x,
            'QQ(sqrt(2))': QQ_sqrt2,
            'F2': F2,
            'F2(t)': F2_t,
            'F2(t)(sqrt(t))': F2_t_sqrt_t,
            'F2_alg': F2_alg
        }
        return mapping.get(f, None)
    return None

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False, False, False]
        F_obj, E_obj, L_obj = witness
        
        F = parse_field(F_obj)
        E = parse_field(E_obj)
        L = parse_field(L_obj)
        
        if F and E and L:
            h1 = F.is_field
            h2 = L.is_field and L.is_alg_closed and L.contains(E)
            
            is_finite = True
            is_separable = True
            curr = E
            while curr is not None and curr != F:
                if not curr.is_finite_ext:
                    is_finite = False
                if not curr.is_separable:
                    is_separable = False
                curr = curr.over
            
            if curr != F:
                neg_q = True
            else:
                neg_q = not (is_finite and is_separable)
                
            return [bool(h1), bool(h2), bool(neg_q)]
            
        # Fallback for SymPy domains
        if hasattr(F_obj, 'is_Field') and hasattr(E_obj, 'is_Field') and hasattr(L_obj, 'is_Field'):
            h1 = bool(F_obj.is_Field)
            h2 = bool(L_obj.is_Field) and (L_obj == sympy_CC or getattr(L_obj, 'is_algebraically_closed', False))
            if L_obj == sympy_CC and (E_obj == sympy_QQ or isinstance(E_obj, FractionField) or isinstance(E_obj, AlgebraicField)):
                pass
            else:
                h2 = False
                
            if isinstance(E_obj, FractionField):
                neg_q = True
            elif isinstance(E_obj, AlgebraicField):
                neg_q = False
            elif E_obj == sympy_QQ:
                neg_q = False
            else:
                neg_q = True
                
            return [bool(h1), bool(h2), bool(neg_q)]
            
        # Fallback for strings
        if isinstance(F_obj, str) and isinstance(E_obj, str) and isinstance(L_obj, str):
            h1 = True
            h2 = 'alg' in L_obj.lower() or L_obj == 'CC'
            neg_q = ('pi' in E_obj or 'x' in E_obj or 't' in E_obj)
            return [bool(h1), bool(h2), bool(neg_q)]
            
        return [False, False, False]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: L is an algebraically closed field containing E",
    "¬Q: There does not exist a unique minimal finite Galois extension K of F containing E"
]

N_HYP = 2
NEG_Q_INDEX = 2