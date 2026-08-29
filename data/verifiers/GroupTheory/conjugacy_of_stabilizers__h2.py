import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False]
        G, g, x, y = witness
        
        # H_1: G is a group acting on a set X
        h1_ok = False
        if hasattr(G, 'is_group') and hasattr(G, 'degree'):
            if isinstance(x, (int, sympy.Integer)) and isinstance(y, (int, sympy.Integer)):
                if 0 <= x < G.degree and 0 <= y < G.degree:
                    h1_ok = True
                    
        # H_2: There exists g \in G such that y = g \cdot x
        h2_ok = False
        if h1_ok:
            if G.contains(g):
                if g(x) == y:
                    h2_ok = True
                    
        # neg_Q: Stab_G(y) != g Stab_G(x) g^{-1}
        neg_q = False
        if h1_ok and h2_ok:
            stab_x = G.stabilizer(x)
            stab_y = G.stabilizer(y)
            
            g_inv = g**-1
            conj_gens = [g * h * g_inv for h in stab_x.generators]
            
            if not conj_gens:
                conj_gens = [g * g_inv]
                
            conj_group = PermutationGroup(conj_gens)
            
            is_subset1 = all(conj_group.contains(gen) for gen in stab_y.generators)
            is_subset2 = all(stab_y.contains(gen) for gen in conj_group.generators)
            
            if not (is_subset1 and is_subset2):
                neg_q = True
                
        return [h1_ok, h2_ok, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: There exists g in G such that y = g \\cdot x",
    "¬Q: Stab_G(y) is not equal to g Stab_G(x) g^{-1}"
]

N_HYP = 2
NEG_Q_INDEX = 2