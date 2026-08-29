import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z

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

ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            if "A_is_commutative_Noetherian" in witness:
                h1 = bool(witness.get("A_is_commutative_Noetherian", False))
                h2 = bool(witness.get("G_is_finite", False))
                q = bool(witness.get("R_G_is_finitely_generated", True))
                return [h1, h2, not q]
                
        if hasattr(witness, "A_is_commutative_Noetherian"):
            h1 = bool(getattr(witness, "A_is_commutative_Noetherian", False))
            h2 = bool(getattr(witness, "G_is_finite", False))
            q = bool(getattr(witness, "R_G_is_finitely_generated", True))
            return [h1, h2, not q]
            
        s = str(witness).lower()
        
        noetherian_kws = ["zz", "qq", "field", "noetherian", "integer", "rational", "ring", "domain", "k[", "z[", "q[", "r[", "c[", "real", "complex"]
        if any(kw in s for kw in noetherian_kws):
            h1 = True
            
        finite_group_kws = ["s2", "z2", "symmetric", "cyclic", "permutation", "automorphism", "action", "act", "s_2", "z_2", "s3", "z3"]
        
        t = s
        for p in ".,;()[]{}\"'=+-":
            t = t.replace(p, " ")
        words = t.split()
        
        if any(kw in s for kw in finite_group_kws) or "finite" in words or "group" in words:
            h2 = True
            
        neg_q_kws = ["infinite", "...", "not finitely generated", "not noetherian", "infinitely many", "non-noetherian", "non-finitely", "not fg", "not f.g."]
        if any(kw in s for kw in neg_q_kws):
            neg_q = True
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a commutative Noetherian ring",
    "H_2: G is a finite group acting on R by A-algebra automorphisms",
    "¬Q: R^G is not a finitely generated A-algebra (or not Noetherian)"
]

N_HYP = 2
NEG_Q_INDEX = 2