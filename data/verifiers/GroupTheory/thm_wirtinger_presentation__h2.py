import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: K is a tame knot in R^3",
    "¬Q: The conclusion fails (e.g., the unknot has no crossing relations to omit in its reduced projection)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, str):
            w_str = witness.lower().replace(" ", "").replace("_", "")
            if w_str in ["unknot", "trivialknot", "01", "trefoil", "31", "figureeight", "41", "cinquefoil", "51", "52"]:
                h1 = True
            if w_str in ["unknot", "trivialknot", "01"]:
                neg_q = True
                
        elif isinstance(witness, int):
            if witness >= 0:
                h1 = True
            if witness == 0:
                neg_q = True
                
        elif isinstance(witness, list):
            if all(isinstance(x, int) for x in witness):
                h1 = True
                if len(witness) == 0:
                    neg_q = True
                    
    except Exception:
        pass

    return [h1, neg_q]