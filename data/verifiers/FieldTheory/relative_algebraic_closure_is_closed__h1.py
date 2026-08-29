import sympy

class MathField:
    def __init__(self, name, is_alg_closed):
        self.name = name
        self.is_alg_closed = is_alg_closed
        
    def __repr__(self):
        return self.name
        
    def __eq__(self, other):
        if isinstance(other, MathField):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other
        return False
        
    def __hash__(self):
        return hash(self.name)

# Top-level setup: named object bindings for witness expressions
QQ = MathField("QQ", False)
QQ_i = MathField("QQ(i)", False)
QQ_sqrt2 = MathField("QQ(sqrt(2))", False)
QQ_x = MathField("QQ(x)", False)
QQbar = MathField("QQbar", True)
RR = MathField("RR", False)
CC = MathField("CC", True)
Fp = MathField("Fp", False)
Fp_bar = MathField("Fp_bar", True)
Fp_t = MathField("Fp(t)", False)

subfield_relations = {
    ("QQ", "QQ"), ("QQ", "QQ_i"), ("QQ", "QQ_sqrt2"), ("QQ", "QQ_x"), ("QQ", "QQbar"), ("QQ", "RR"), ("QQ", "CC"), ("QQ", "QQ_ext"),
    ("QQ_i", "QQ_i"), ("QQ_i", "QQbar"), ("QQ_i", "CC"),
    ("QQ_sqrt2", "QQ_sqrt2"), ("QQ_sqrt2", "QQbar"), ("QQ_sqrt2", "RR"), ("QQ_sqrt2", "CC"),
    ("QQ_x", "QQ_x"),
    ("QQbar", "QQbar"), ("QQbar", "CC"),
    ("RR", "RR"), ("RR", "CC"),
    ("CC", "CC"),
    ("Fp", "Fp"), ("Fp", "Fp_bar"), ("Fp", "Fp_t"),
    ("Fp_bar", "Fp_bar"),
    ("Fp_t", "Fp_t"),
    ("QQ_ext", "QQ_ext"), ("QQ_ext", "QQbar"), ("QQ_ext", "CC")
}

rel_alg_closures = {
    ("QQ", "QQ"): "QQ",
    ("QQ", "QQ_i"): "QQ_i",
    ("QQ", "QQ_sqrt2"): "QQ_sqrt2",
    ("QQ", "QQ_x"): "QQ",
    ("QQ", "QQbar"): "QQbar",
    ("QQ", "CC"): "QQbar",
    ("QQ", "RR"): "QQbar_R",
    ("QQ", "QQ_ext"): "QQ_ext",
    ("QQ_i", "QQ_i"): "QQ_i",
    ("QQ_i", "QQbar"): "QQbar",
    ("QQ_i", "CC"): "QQbar",
    ("QQ_sqrt2", "QQ_sqrt2"): "QQ_sqrt2",
    ("QQ_sqrt2", "QQbar"): "QQbar",
    ("QQ_sqrt2", "CC"): "QQbar",
    ("QQ_sqrt2", "RR"): "QQbar_R",
    ("QQ_x", "QQ_x"): "QQ_x",
    ("QQbar", "QQbar"): "QQbar",
    ("QQbar", "CC"): "QQbar",
    ("RR", "RR"): "RR",
    ("RR", "CC"): "CC",
    ("CC", "CC"): "CC",
    ("Fp", "Fp"): "Fp",
    ("Fp", "Fp_bar"): "Fp_bar",
    ("Fp", "Fp_t"): "Fp",
    ("Fp_bar", "Fp_bar"): "Fp_bar",
    ("Fp_t", "Fp_t"): "Fp_t",
    ("QQ_ext", "QQ_ext"): "QQ_ext",
    ("QQ_ext", "QQbar"): "QQbar",
    ("QQ_ext", "CC"): "QQbar"
}

def get_field_name(F):
    if isinstance(F, MathField):
        return F.name
    if hasattr(F, 'is_RationalField') and F.is_RationalField:
        return "QQ"
    if hasattr(F, 'is_RealField') and F.is_RealField:
        return "RR"
    if hasattr(F, 'is_ComplexField') and F.is_ComplexField:
        return "CC"
    if hasattr(F, 'is_AlgebraicField'):
        return "QQ_ext"
    if hasattr(F, 'is_Frac') and F.is_Frac:
        return "QQ_x"
    if type(F) is str:
        return F
    return "Unknown"

def is_subfield(K, L):
    if K == L:
        return True
    k_name = get_field_name(K)
    l_name = get_field_name(L)
    if k_name == "QQ_ext" and l_name == "QQ_ext":
        return False
    return (k_name, l_name) in subfield_relations

def is_rel_alg_closure(K, L, E):
    if K == L and L == E:
        return True
    k_name = get_field_name(K)
    l_name = get_field_name(L)
    e_name = get_field_name(E)
    
    if k_name == "QQ_ext" and l_name == "QQ_ext":
        return False
        
    expected_e_name = rel_alg_closures.get((k_name, l_name), None)
    
    if expected_e_name is None:
        return False
        
    if expected_e_name == "QQ_ext":
        return E == L
        
    return e_name == expected_e_name

def is_alg_closed(F):
    if isinstance(F, MathField):
        return F.is_alg_closed
    name = get_field_name(F)
    if name in ["CC", "QQbar", "Fp_bar"]:
        return True
    if name in ["QQ", "RR", "QQ_i", "QQ_sqrt2", "QQ_x", "QQ_ext", "Fp", "Fp_t", "QQbar_R"]:
        return False
    return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        K, L, E = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(is_subfield(K, L))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(is_rel_alg_closure(K, L, E))
    except Exception:
        h2 = False
        
    try:
        q = bool(is_alg_closed(E))
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a subfield of L",
    "H_2: E is the set of all elements in L that are algebraic over K",
    "¬Q: E is not an algebraically closed field"
]

N_HYP = 2
NEG_Q_INDEX = 2