import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

def count_sylow_3(G):
    try:
        if not isinstance(G, PermutationGroup):
            return None
        
        P = G.sylow_subgroup(3)
        if P.order() == 1:
            return 1
        
        def canonical(H):
            # Sort by array_form to ensure deterministic and comparable representation
            return tuple(sorted([tuple(p.array_form) for p in H.elements]))
        
        P_canon = canonical(P)
        orbit = {P_canon}
        queue = [P]
        
        gens = list(G.generators)
        gens += [~g for g in gens]
        
        while queue:
            curr = queue.pop(0)
            for g in gens:
                conj_gens = [~g * x * g for x in curr.generators]
                H = PermutationGroup(conj_gens)
                H_canon = canonical(H)
                if H_canon not in orbit:
                    orbit.add(H_canon)
                    queue.append(H)
        return len(orbit)
    except Exception:
        return None

def conditions(witness):
    try:
        n3 = count_sylow_3(witness)
        if n3 is None:
            neg_Q = False
        else:
            neg_Q = (n3 != 10)
    except Exception:
        neg_Q = False

    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: The number of Sylow 3-subgroups in the witness is not exactly 10"
]

N_HYP = 0
NEG_Q_INDEX = 0