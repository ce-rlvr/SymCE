import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "H_2: M1 and M2 are intermediate fields between K and L",
    "H_3: H1 and H2 are the subgroups of G fixing M1 and M2 respectively",
    "¬Q: M1 and M2 are conjugate extensions over K iff H1 and H2 are conjugate subgroups in G is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if hasattr(witness, 'is_finite_galois'):
            return [
                bool(witness.is_finite_galois()),
                bool(witness.are_intermediate_fields()),
                bool(witness.are_fixing_subgroups()),
                bool(witness.are_conjugate_extensions() != witness.are_conjugate_subgroups())
            ]
    except Exception:
        pass

    try:
        G, H1, H2 = witness[:3]
        conj_ext = witness[3] if len(witness) > 3 else None

        h1 = isinstance(G, PermutationGroup) and G.order() > 0
        h2 = isinstance(H1, PermutationGroup) and isinstance(H2, PermutationGroup) and H1.is_subgroup(G) and H2.is_subgroup(G)
        
        conj_sub = False
        if h2 and H1.order() == H2.order():
            for g in G.elements:
                if all((g * h * ~g) in H2 for h in H1.generators):
                    conj_sub = True
                    break
        
        if conj_ext is None:
            conj_ext = conj_sub
            
        return [bool(h1), bool(h2), bool(h2), bool(conj_ext) != bool(conj_sub)]
    except Exception:
        return [False, False, False, False]