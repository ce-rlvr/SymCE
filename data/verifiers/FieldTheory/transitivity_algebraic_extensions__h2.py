import sympy
from sympy import QQ, Symbol, S
from sympy.polys.domains import FractionField, AlgebraicField, RationalField
from sympy.abc import x, y, t

class MathField:
    """
    A simple representation of a field extension over a base field (e.g., Q).
    Used to easily construct witnesses like Q, Q(x), Q(x, sqrt(x)).
    """
    def __init__(self, name, trans_gens, alg_gens):
        self.name = name
        self.trans_gens = frozenset(trans_gens)
        self.alg_gens = frozenset(alg_gens)
        
    def __str__(self):
        return f"{self.name}({', '.join(list(self.trans_gens) + list(self.alg_gens))})"
        
    def is_subfield(self, other):
        if not isinstance(other, MathField): return False
        if self.name != other.name: return False
        return self.trans_gens.issubset(other.trans_gens) and self.alg_gens.issubset(other.alg_gens)
        
    def is_algebraic_over(self, base):
        if not base.is_subfield(self): return False
        return self.trans_gens == base.trans_gens

# Pre-defined fields for easy witness construction
Q = MathField("Q", [], [])
Q_x = MathField("Q", ["x"], [])
Q_y = MathField("Q", ["y"], [])
Q_x_y = MathField("Q", ["x", "y"], [])
Q_sqrt2 = MathField("Q", [], ["sqrt2"])
Q_x_sqrtx = MathField("Q", ["x"], ["sqrtx"])
Q_x_y_sqrtx = MathField("Q", ["x", "y"], ["sqrtx"])

def normalize_field(F):
    try:
        if F == S.Rationals: return QQ
    except Exception:
        pass
    return F

def is_field(F):
    if isinstance(F, MathField): return True
    if isinstance(F, set): return True
    if isinstance(F, str): return True
    try:
        if hasattr(F, 'is_Field') and F.is_Field: return True
    except Exception:
        pass
    try:
        if F == QQ: return True
    except Exception:
        pass
    try:
        if isinstance(F, (FractionField, AlgebraicField, RationalField)): return True
    except Exception:
        pass
    return False

def check_subfield(K, L):
    if isinstance(K, MathField) and isinstance(L, MathField):
        return K.is_subfield(L)
    if isinstance(K, set) and isinstance(L, set):
        return K.issubset(L)
    if isinstance(K, str) and isinstance(L, str):
        K_str = K.replace(" ", "")
        L_str = L.replace(" ", "")
        if K_str == L_str: return True
        if K_str == "Q": return True
        if K_str == "Q(x)" and L_str in ["Q(x)", "Q(x,y)", "Q(x,sqrt(x))", "Q(x)(sqrt(x))", "Q(x,sqrtx)"]: return True
        if K_str == "Q(y)" and L_str in ["Q(x,y)", "Q(y,x)"]: return True
        return False
    try:
        if K == L: return True
        if K == QQ: return True
        if isinstance(K, FractionField) and isinstance(L, FractionField):
            return set(K.symbols).issubset(set(L.symbols))
    except Exception:
        pass
    return False

def check_algebraic(M, L):
    if isinstance(M, MathField) and isinstance(L, MathField):
        return M.is_algebraic_over(L)
    if isinstance(M, set) and isinstance(L, set):
        diff = M.difference(L)
        for g in diff:
            s = str(g)
            if not ('sqrt' in s or 'I' in s or 'cbrt' in s or 'root' in s or s.isdigit()):
                return False
        return True
    if isinstance(M, str) and isinstance(L, str):
        M_str = M.replace(" ", "")
        L_str = L.replace(" ", "")
        if M_str == L_str: return True
        for var in ['x', 'y', 't', 'pi', 'E']:
            if var in M_str and var not in L_str:
                return False
        return True
    try:
        if M == L: return True
        if isinstance(M, FractionField) and isinstance(L, FractionField):
            return set(M.symbols) == set(L.symbols)
        if isinstance(M, AlgebraicField) and L == QQ:
            return True
        if isinstance(M, FractionField) and L == QQ:
            return False
    except Exception:
        pass
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of three fields (K, L, M).
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        K, L, M = witness
    except Exception:
        return [False, False, False]
        
    K = normalize_field(K)
    L = normalize_field(L)
    M = normalize_field(M)
    
    # H_1: K, L, and M are fields such that K \subseteq L \subseteq M
    try:
        h1 = is_field(K) and is_field(L) and is_field(M) and \
             check_subfield(K, L) and check_subfield(L, M)
    except Exception:
        h1 = False
        
    # H_2: The field extension M/L is algebraic
    try:
        h2 = check_algebraic(M, L)
    except Exception:
        h2 = False
        
    # ¬Q: The field extension M/K is NOT algebraic
    try:
        neg_q = not check_algebraic(M, K)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K, L, and M are fields such that K \\subseteq L \\subseteq M",
    "H_2: The field extension M/L is algebraic",
    "¬Q: The field extension M/K is not algebraic"
]

N_HYP = 2
NEG_Q_INDEX = 2