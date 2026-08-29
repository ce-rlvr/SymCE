import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

def is_finitely_generated(G):
    if hasattr(G, 'is_finitely_generated'):
        val = G.is_finitely_generated() if callable(G.is_finitely_generated) else G.is_finitely_generated
        if isinstance(val, bool): 
            return val
            
    if isinstance(G, str):
        G_lower = G.lower().replace(" ", "").replace("_", "").replace("{", "").replace("}", "").replace("\\", "")
        if any(x in G_lower for x in ["sinfty", "soo", "infinitesymmetric", "sym(infty)", "sym(oo)", "sym(nat)"]):
            return False
        if any(x in G_lower for x in ["ainfty", "aoo", "infinitealternating", "alt(infty)", "alt(oo)", "alt(nat)"]):
            return False
        if G_lower in ["q", "r", "c", "q/z", "r/z"]:
            return False
        if any(x in G_lower for x in ["finfty", "foo", "infinitefree"]):
            return False
        if any(x in G_lower for x in ["gl(infty", "gl(oo"]):
            return False
        if any(x in G_lower for x in ["braidgroup(infty)", "braidgroup(oo)"]):
            return False
        if G_lower in ["z", "z^n", "z*z", "f2", "s3", "s4"]:
            return True
        return False
    
    if hasattr(G, 'generators'):
        try:
            return len(list(G.generators)) < float('inf')
        except Exception:
            pass
            
    return True

def abelianization_is_finitely_generated(G):
    if hasattr(G, 'abelianization_is_finitely_generated'):
        val = G.abelianization_is_finitely_generated() if callable(G.abelianization_is_finitely_generated) else G.abelianization_is_finitely_generated
        if isinstance(val, bool): 
            return val
            
    if hasattr(G, 'abelianization'):
        A = G.abelianization() if callable(G.abelianization) else G.abelianization
        return is_finitely_generated(A)
        
    if isinstance(G, str):
        G_lower = G.lower().replace(" ", "").replace("_", "").replace("{", "").replace("}", "").replace("\\", "")
        if any(x in G_lower for x in ["sinfty", "soo", "infinitesymmetric", "sym(infty)", "sym(oo)", "sym(nat)"]):
            return True 
        if any(x in G_lower for x in ["ainfty", "aoo", "infinitealternating", "alt(infty)", "alt(oo)", "alt(nat)"]):
            return True 
        if G_lower in ["q", "r", "c", "q/z", "r/z"]:
            return False
        if any(x in G_lower for x in ["finfty", "foo", "infinitefree"]):
            return False
        if any(x in G_lower for x in ["gl(infty", "gl(oo"]):
            return True
        if any(x in G_lower for x in ["braidgroup(infty)", "braidgroup(oo)"]):
            return True
        if G_lower in ["z", "z^n", "z*z", "f2", "s3", "s4"]:
            return True
        return False
        
    if hasattr(G, 'derived_subgroup'):
        return True
        
    return True

def conditions(witness):
    try:
        h1 = bool(abelianization_is_finitely_generated(witness))
    except Exception:
        h1 = False

    try:
        q = bool(is_finitely_generated(witness))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The abelianization of G, defined as the quotient group G/G', is a finitely generated group",
    "¬Q: G is not a finitely generated group"
]

N_HYP = 1
NEG_Q_INDEX = 1