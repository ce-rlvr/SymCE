import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and fails the conclusion.
    The witness is expected to be a tuple (G, u, v) or a dictionary with keys 'G', 'u', 'v',
    where G represents the automorphism group Aut(Γ) acting on the vertices, and u, v are vertices.
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            u = witness.get('u')
            v = witness.get('v')
        elif isinstance(witness, tuple) and len(witness) == 3:
            G, u, v = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # Ensure G is a PermutationGroup if it's given as a list of permutations
    try:
        if not hasattr(G, 'is_transitive') and not hasattr(G, 'stabilizer'):
            G = PermutationGroup(G)
    except Exception:
        pass

    # H_1: The automorphism group Aut(Γ) acts transitively on the vertex set V(Γ)
    try:
        if callable(G.is_transitive):
            h1 = bool(G.is_transitive())
        else:
            h1 = bool(G.is_transitive)
    except Exception:
        h1 = False

    # H_2: u and v are vertices in V(Γ)
    try:
        degree = G.degree() if callable(G.degree) else G.degree
        h2 = int(u) in range(degree) and int(v) in range(degree)
    except Exception:
        h2 = False

    # ¬Q: The point stabilizer of u in Aut(Γ) is NOT isomorphic to the point stabilizer of v in Aut(Γ)
    try:
        stab_u = G.stabilizer(u)
        stab_v = G.stabilizer(v)
        
        if hasattr(stab_u, 'is_isomorphic'):
            iso = stab_u.is_isomorphic(stab_v)
        else:
            # Fallback heuristic if is_isomorphic is not available
            order_u = stab_u.order() if callable(stab_u.order) else stab_u.order
            order_v = stab_v.order() if callable(stab_v.order) else stab_v.order
            ab_u = stab_u.is_abelian() if callable(stab_u.is_abelian) else stab_u.is_abelian
            ab_v = stab_v.is_abelian() if callable(stab_v.is_abelian) else stab_v.is_abelian
            iso = (order_u == order_v and ab_u == ab_v)
            
        neg_q = not bool(iso)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Aut(Γ) acts transitively on V(Γ)",
    "H_2: u and v are vertices in V(Γ)",
    "¬Q: The point stabilizer of u in Aut(Γ) is not isomorphic as a group to the point stabilizer of v in Aut(Γ)"
]

N_HYP = 2
NEG_Q_INDEX = 2