import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Standard algebra objects
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

def is_in_variety(G, variety_name):
    if variety_name == "abelian":
        return G.is_abelian
    elif variety_name.startswith("exponent_"):
        n = int(variety_name.split("_")[1])
        # In a variety of exponent n, g^n = 1 for all g, so the order of g must divide n.
        return all(n % g.order() == 0 for g in G.elements)
    elif variety_name == "trivial":
        return G.order() == 1
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis was that each G_i belongs to the variety V.
    """
    try:
        if isinstance(witness, dict):
            variety_name = witness.get('V', witness.get('variety', witness.get('variety_name')))
            G_list = witness.get('G_list', witness.get('groups'))
        else:
            variety_name, G_list = witness
            
        if isinstance(G_list, PermutationGroup):
            G_list = [G_list]
        else:
            G_list = list(G_list)
            
        variety_name = str(variety_name)
    except Exception:
        return [False, False]
    
    # H_1: V is a variety of groups defined by a set of identities
    try:
        valid_varieties = ["abelian", "trivial", "exponent_2", "exponent_3", "exponent_4", "exponent_5", "exponent_6"]
        h1_ok = (variety_name in valid_varieties) and len(G_list) > 0
        if h1_ok:
            h1_ok = all(isinstance(G, PermutationGroup) for G in G_list)
    except Exception:
        h1_ok = False
        
    # ¬Q: The unrestricted direct product of G_i does NOT belong to the variety V
    try:
        # A variety is closed under subgroups. Since each G_i is isomorphic to a subgroup
        # of the direct product, the direct product is in V if and only if all G_i are in V.
        # Thus, the direct product does NOT belong to V iff at least one G_i does NOT belong to V.
        neg_q_ok = not all(is_in_variety(G, variety_name) for G in G_list)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a variety of groups defined by a set of identities",
    "¬Q: The unrestricted direct product of G_i does not belong to the variety V"
]

N_HYP = 1
NEG_Q_INDEX = 1