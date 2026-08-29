import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    H1 = False
    H2 = False
    neg_Q = False
    
    try:
        # Parse witness
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, x = witness
            elif len(witness) >= 3:
                G = witness[0]
                x = witness[-1]
        else:
            G = witness
            x = None
            
        # H1: G is a group acting on a set X
        if isinstance(G, PermutationGroup):
            if isinstance(x, (int, sympy.Integer)) and x >= 0:
                H1 = True
    except Exception:
        pass

    try:
        # H2: O_x is the orbit of x under G
        if H1:
            O_x = G.orbit(x)
            if isinstance(O_x, (set, list)):
                H2 = True
    except Exception:
        pass

    try:
        if H1 and H2:
            G_x = G.stabilizer(x)
            id_perm = G.generators[0] * ~G.generators[0] if G.generators else Permutation()
            
            if G.order() <= 2000:
                # Compute pointwise stabilizer of O_x explicitly
                pt_stab_elements = []
                for h in G.elements:
                    fixes_all = True
                    for y in O_x:
                        if h(y) != y:
                            fixes_all = False
                            break
                    if fixes_all:
                        pt_stab_elements.append(h)
                pt_stab = PermutationGroup(pt_stab_elements) if pt_stab_elements else PermutationGroup([id_perm])
                
                # Compute normal core of G_x explicitly
                normal_core = G
                for g in G.elements:
                    conj_gens = [g * h * ~g for h in G_x.generators]
                    if not conj_gens:
                        conj_gens = [id_perm]
                    conj_group = PermutationGroup(conj_gens)
                    normal_core = normal_core.intersect(conj_group)
            else:
                # Fast path for large groups
                pt_stab = G
                for y in O_x:
                    pt_stab = pt_stab.intersect(G.stabilizer(y))
                    
                normal_core = G
                try:
                    transversal = G.orbit_transversal(x)
                    for g in transversal:
                        conj_gens = [g * h * ~g for h in G_x.generators]
                        if not conj_gens:
                            conj_gens = [id_perm]
                        conj_group = PermutationGroup(conj_gens)
                        normal_core = normal_core.intersect(conj_group)
                except Exception:
                    # Fallback if orbit_transversal is not available
                    for y in O_x:
                        normal_core = normal_core.intersect(G.stabilizer(y))
                        
            # Check if they are equal
            is_equal = pt_stab.is_subgroup(normal_core) and normal_core.is_subgroup(pt_stab)
            neg_Q = not is_equal
    except Exception:
        pass

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: O_x is the orbit of x under G",
    "¬Q: The pointwise stabilizer of O_x in G is NOT the normal core of G_x in G"
]

N_HYP = 2
NEG_Q_INDEX = 2