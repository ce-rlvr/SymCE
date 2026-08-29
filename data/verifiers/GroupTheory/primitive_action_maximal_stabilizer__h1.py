import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: X is a set containing at least two elements",
    "H_2: G acts transitively on X",
    "¬Q: The action is primitive if and only if the stabilizer is a maximal subgroup (fails)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
            
            try:
                h1 = (G.order() // H.order()) >= 2
            except Exception:
                h1 = False
                
            h2 = True
            
            try:
                is_max = False
                if H.order() < G.order():
                    is_max = True
                    for g in G.generate_dimino():
                        if not H.contains(g):
                            gens = list(H.generators) + [g]
                            K = PermutationGroup(gens)
                            if K.order() < G.order():
                                is_max = False
                                break
                                
                is_faithful = True
                for n in G.normal_subgroups():
                    if n.order() > 1 and n.is_subgroup(H):
                        is_faithful = False
                        break
                prim = is_max and is_faithful
                
                neg_q = not (prim == is_max)
            except Exception:
                neg_q = False

        elif isinstance(witness, PermutationGroup):
            G = witness
            
            try:
                h1 = G.degree >= 2
            except Exception:
                h1 = False
                
            try:
                h2 = G.is_transitive()
            except Exception:
                h2 = False
                
            try:
                prim = G.is_primitive()
                
                H = G.stabilizer(0)
                
                is_max = False
                if H.order() < G.order():
                    is_max = True
                    for g in G.generate_dimino():
                        if not H.contains(g):
                            gens = list(H.generators) + [g]
                            K = PermutationGroup(gens)
                            if K.order() < G.order():
                                is_max = False
                                break
                                
                neg_q = not (prim == is_max)
            except Exception:
                neg_q = False

    except Exception:
        pass

    return [h1, h2, neg_q]