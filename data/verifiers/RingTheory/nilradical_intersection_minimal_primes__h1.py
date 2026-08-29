import sympy
from sympy import Matrix, MatrixSymbol, eye, zeros, Symbol
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

Z = sympy.ZZ
Q = sympy.QQ
R = sympy.RR
C = sympy.CC

def conditions(witness):
    try:
        neg_q = False
        
        def is_counterexample(w):
            if isinstance(w, str):
                s = w.lower().replace(" ", "").replace("_", "").replace("(", "").replace(")", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "")
                if "triangular" in s or "weyl" in s or "quaternion" in s or "division" in s or "free" in s:
                    return False
                if any(x in s for x in ["m2", "m3", "m4", "mn", "matrix", "matrices", "gl2", "gl3", "gln", "sl2", "sl3", "sln", "operator", "b(h)", "end", "s3", "s4", "a4", "d4", "q8"]):
                    return True
            
            if isinstance(w, (tuple, list, set)):
                if any(is_counterexample(item) for item in w):
                    return True
                    
            if isinstance(w, dict):
                if any(is_counterexample(item) for item in w.values()):
                    return True
                    
            if hasattr(w, "is_Matrix") and hasattr(w, "shape"):
                if len(w.shape) == 2 and w.shape[0] >= 2 and w.shape[0] == w.shape[1]:
                    return True
                    
            if hasattr(w, "is_abelian") and w.is_abelian is False:
                return True
                
            if hasattr(w, "__class__"):
                cname = w.__class__.__name__.lower()
                if "triangular" in cname or "weyl" in cname or "quaternion" in cname or "division" in cname or "free" in cname:
                    return False
                if "matrix" in cname or "ring" in cname or "algebra" in cname:
                    if hasattr(w, "n") and isinstance(w.n, int) and w.n >= 2:
                        return True
                    if hasattr(w, "size") and isinstance(w.size, int) and w.size >= 2:
                        return True
                    if "matrix" in cname:
                        return True
                        
            return False

        neg_q = is_counterexample(witness)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The nilradical of R is not equal to the intersection of all minimal prime ideals of R"
]

N_HYP = 0
NEG_Q_INDEX = 0