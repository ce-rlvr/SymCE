import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

class InfGroup:
    def __init__(self, name, torsion_free, q_rank):
        self.name = name
        self.torsion_free = torsion_free
        self.q_rank = q_rank
        
    def __mul__(self, other):
        if isinstance(other, InfGroup):
            return InfGroup(f"({self.name} x {other.name})", 
                            self.torsion_free and other.torsion_free,
                            self.q_rank + other.q_rank)
        return NotImplemented

    def __add__(self, other):
        return self.__mul__(other)
        
    def __pow__(self, n):
        if isinstance(n, int) and n > 0:
            return InfGroup(f"{self.name}^{n}", self.torsion_free, self.q_rank * n)
        return NotImplemented

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

Z = InfGroup("Z", True, 1)
Q = InfGroup("Q", True, 1)
R = InfGroup("R", True, float('inf'))

def is_torsion_free(G):
    if isinstance(G, InfGroup):
        return G.torsion_free
    if isinstance(G, str):
        return G in ["Z", "Z x Z", "Q", "R", "Z^2", "Z^3", "Z x Z x Z"]
    if isinstance(G, tuple):
        return all(is_torsion_free(g) for g in G)
    try:
        if hasattr(G, 'is_PermutationGroup') and G.is_PermutationGroup:
            return G.order() == 1
    except Exception:
        pass
    return False

def is_subgroup_of_Q(G):
    if isinstance(G, InfGroup):
        return G.torsion_free and G.q_rank <= 1
    if isinstance(G, str):
        return G in ["Z", "Q"]
    if isinstance(G, tuple):
        if len(G) == 0:
            return True
        if len(G) == 1:
            return is_subgroup_of_Q(G[0])
        return False
    try:
        if hasattr(G, 'is_PermutationGroup') and G.is_PermutationGroup:
            return G.order() == 1
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        H_1_ok = bool(is_torsion_free(witness))
    except Exception:
        H_1_ok = False
        
    try:
        neg_Q_ok = not bool(is_subgroup_of_Q(witness))
    except Exception:
        neg_Q_ok = False
        
    return [H_1_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: G is torsion-free",
    "¬Q: G is not isomorphic to a subgroup of (Q, +)"
]

N_HYP = 1
NEG_Q_INDEX = 1