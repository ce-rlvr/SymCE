import sympy
from sympy import ZZ, QQ
from sympy.matrices import eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class CommutativeRing:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"CommutativeRing({self.name})"

class RModule:
    def __init__(self, ring, name):
        self.ring = ring
        self.name = name
    def __repr__(self):
        return f"RModule({self.name} over {self.ring})"

class MultiplicativelyClosedSet:
    def __init__(self, ring, name="S"):
        self.ring = ring
        self.name = name
    def __repr__(self):
        return f"MultiplicativelyClosedSet({self.name} in {self.ring})"

Z_ring = CommutativeRing("Z")
Q_ring = CommutativeRing("Q")
M_Z = RModule(Z_ring, "M")
N_Z = RModule(Z_ring, "N")
S_Z = MultiplicativelyClosedSet(Z_ring, "S")

def is_comm_ring(R):
    if isinstance(R, CommutativeRing):
        return True
    if R in [sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes, ZZ, QQ]:
        return True
    if R in ['Z', 'Q', 'R', 'C', 'ZZ', 'QQ', 'RR', 'CC']:
        return True
    return False

def is_module(M, R):
    if isinstance(M, RModule):
        return M.ring == R or M.ring == getattr(R, 'name', R)
    if M == R:
        return True
    
    Z_reps = [sympy.S.Integers, ZZ, 'Z', 'ZZ', Z_ring]
    Q_reps = [sympy.S.Rationals, QQ, 'Q', 'QQ', Q_ring]
    R_reps = [sympy.S.Reals, 'R', 'RR']
    C_reps = [sympy.S.Complexes, 'C', 'CC']
    
    if M in Z_reps and R in Z_reps:
        return True
    if M in Q_reps and R in (Z_reps + Q_reps):
        return True
    if M in R_reps and R in (Z_reps + Q_reps + R_reps):
        return True
    if M in C_reps and R in (Z_reps + Q_reps + R_reps + C_reps):
        return True
        
    if hasattr(M, 'is_Matrix') and M.is_Matrix:
        return True
        
    return False

def is_mult_closed(S, R):
    if isinstance(S, MultiplicativelyClosedSet):
        return S.ring == R or S.ring == getattr(R, 'name', R)
    if isinstance(S, set):
        if not S: return False
        try:
            for a in S:
                for b in S:
                    if (a*b) not in S:
                        return False
            return True
        except Exception:
            return False
    if isinstance(S, (list, tuple)):
        return is_mult_closed(set(S), R)
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            M = witness.get('M')
            S = witness.get('S')
            N = witness.get('N')
        else:
            R, M, S, N = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = is_comm_ring(R)
    except Exception:
        h1 = False
        
    try:
        h2 = is_module(M, R)
    except Exception:
        h2 = False
        
    try:
        h3 = is_mult_closed(S, R)
    except Exception:
        h3 = False
        
    try:
        # The conclusion is that there is an isomorphism.
        # This requires N to be an R-module.
        # If N is not an R-module, the tensor product is undefined, so the conclusion fails.
        neg_q = not is_module(N, R)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: M is an R-module",
    "H_3: S is a multiplicatively closed subset of R",
    "¬Q: There is no S^{-1}R-module isomorphism (e.g. N is not an R-module)"
]

N_HYP = 3
NEG_Q_INDEX = 3