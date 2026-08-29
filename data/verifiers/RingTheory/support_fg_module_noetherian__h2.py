import sympy

class CommutativeRing:
    def __init__(self, name, is_comm, is_noeth):
        self.name = name
        self.is_commutative = is_comm
        self.is_noetherian = is_noeth
        
    def __repr__(self):
        return self.name

class RModule:
    def __init__(self, name, ring, ann, supp, V_ann):
        self.name = name
        self.ring = ring
        self.ann = ann
        self.supp = set(supp)
        self.V_ann = set(V_ann)
        
    def __repr__(self):
        return self.name

# Top-level setup: predefined rings and modules for the witness to reference
Z = CommutativeRing("Z", is_comm=True, is_noeth=True)
Q_ring = CommutativeRing("Q", is_comm=True, is_noeth=True)
R_non_noeth = CommutativeRing("k[x1, x2, ...]", is_comm=True, is_noeth=False)
R_non_comm = CommutativeRing("M_2(R)", is_comm=False, is_noeth=True)

# Modules over Z
# V_ann represents the set of prime ideals containing Ann(M)
# supp represents the support of M, Supp(M)
M_Q = RModule("Q", Z, ann="0", supp=["0", "p"], V_ann=["0", "p"])
M_Q_mod_Z = RModule("Q/Z", Z, ann="0", supp=["p"], V_ann=["0", "p"])
M_direct_sum_Z_p = RModule("bigoplus_p Z/pZ", Z, ann="0", supp=["p"], V_ann=["0", "p"])
M_Z = RModule("Z", Z, ann="0", supp=["0", "p"], V_ann=["0", "p"])
M_Z2 = RModule("Z/2Z", Z, ann="2", supp=["2"], V_ann=["2"])
M_Z_half = RModule("Z[1/2]", Z, ann="0", supp=["0", "p!=2"], V_ann=["0", "p"])

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a module (e.g., M_Q_mod_Z) or a tuple (Ring, Module).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            M = witness
            R = getattr(M, "ring", None)
            
        if not hasattr(R, "is_commutative") or not hasattr(M, "supp"):
            return [False, False]
            
        # H_1: R is a commutative Noetherian ring
        h1_ok = bool(R.is_commutative and R.is_noetherian)
        
        # Ensure the module is actually over the specified ring
        if getattr(M, "ring", None) != R:
            h1_ok = False
            
        # ¬Q: Supp(M) is NOT equal to the set of prime ideals of R containing Ann(M)
        neg_q_ok = bool(M.supp != M.V_ann)
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: Supp(M) is not equal to the set of prime ideals of R containing Ann(M)"
]

N_HYP = 1
NEG_Q_INDEX = 1