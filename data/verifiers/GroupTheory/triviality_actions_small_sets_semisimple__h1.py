import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def parse_witness(witness):
    """
    Helper to extract the group G and the stabilizer subgroup H from the witness.
    The action of G on the set X is modeled as the action of G on the left cosets G/H.
    """
    # If witness is a tuple (G, H)
    if isinstance(witness, tuple) and len(witness) >= 2:
        G = witness[0]
        H = witness[1]
        if hasattr(G, 'order') and hasattr(H, 'order'):
            return G, H
        
        # If witness is (G, X, action) or similar, try to extract G and find a valid H
        if hasattr(G, 'order') and hasattr(G, 'normal_subgroups'):
            for N in G.normal_subgroups():
                if N.order() < G.order() and G.order() // N.order() <= 4:
                    return G, N
            return G, G

    # If witness is a single group, try to find a proper subgroup of index <= 4
    if hasattr(witness, 'order') and hasattr(witness, 'normal_subgroups'):
        G = witness
        for N in G.normal_subgroups():
            if N.order() < G.order() and G.order() // N.order() <= 4:
                return G, N
        return G, G

    return None, None

def conditions(witness) -> list[bool]:
    G, H = parse_witness(witness)
    
    # H1: G is a semisimple group
    # A finite group is semisimple if it has no non-trivial solvable normal subgroups
    # (i.e., its solvable radical is trivial).
    try:
        h1 = False
        if G is not None and G.order() > 1:
            h1 = True
            for N in G.normal_subgroups():
                if N.order() > 1 and N.is_solvable:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: Let X be a set
    try:
        # In our model, X is the set of left cosets G/H, which is always a valid set.
        h2 = (G is not None and H is not None)
    except Exception:
        h2 = False

    # H3: The cardinality of X is less than or equal to 4
    try:
        if G is not None and H is not None:
            card_X = G.order() // H.order()
            h3 = bool(card_X <= 4)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: G acts on the set X
    try:
        if G is not None and H is not None:
            h4 = bool(H.is_subgroup(G))
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: The action of G on X is not the trivial action
    try:
        if G is not None and H is not None:
            # The action on cosets G/H is trivial iff G acts trivially on all cosets.
            # This means g x H = x H for all g, x.
            # Equivalently, G is contained in the normal core of H.
            # Since H <= G, this means H = G.
            neg_q = bool(H.order() < G.order())
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple group",
    "H_2: Let X be a set",
    "H_3: The cardinality of X is less than or equal to 4",
    "H_4: G acts on the set X",
    "¬Q: The action of G on X is not the trivial action"
]

N_HYP = 4
NEG_Q_INDEX = 4