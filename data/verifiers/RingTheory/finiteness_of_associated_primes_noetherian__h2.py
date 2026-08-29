import sympy

class Ring:
    def __init__(self, name, is_commutative, is_noetherian):
        self.name = name
        self.is_commutative = is_commutative
        self.is_noetherian = is_noetherian

class Module:
    def __init__(self, name, ring, ass_finite):
        self.name = name
        self.ring = ring
        self.ass_finite = ass_finite

Z = Ring("Z", True, True)
Q = Ring("Q", True, True)
k_x = Ring("k[x]", True, True)
k_x_inf = Ring("k[x1, x2, ...]", True, False)

M_inf_Z = Module("DirectSum(Z/pZ)", Z, False)
M_inf_kx = Module("DirectSum(k[x]/(x-a))", k_x, False)
M_Z = Module("Z", Z, True)
M_Q = Module("Q", Z, True)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, Module):
            h1 = bool(witness.ring.is_commutative and witness.ring.is_noetherian)
            neg_q = not bool(witness.ass_finite)
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
            if isinstance(R, Ring) and isinstance(M, Module):
                h1 = bool(R.is_commutative and R.is_noetherian)
                neg_q = not bool(M.ass_finite)
        elif isinstance(witness, dict):
            R = witness.get("R")
            M = witness.get("M")
            if isinstance(R, Ring) and isinstance(M, Module):
                h1 = bool(R.is_commutative and R.is_noetherian)
                neg_q = not bool(M.ass_finite)
            elif isinstance(witness.get("witness"), Module):
                M = witness["witness"]
                h1 = bool(M.ring.is_commutative and M.ring.is_noetherian)
                neg_q = not bool(M.ass_finite)
        elif isinstance(witness, str):
            if witness in ["M_inf_Z", "M_inf_kx"]:
                h1 = True
                neg_q = True
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: The set of associated primes Ass_R(M) is infinite"
]

N_HYP = 1
NEG_Q_INDEX = 1