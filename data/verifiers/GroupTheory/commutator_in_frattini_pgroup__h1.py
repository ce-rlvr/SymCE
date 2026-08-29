import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def frattini_subgroup_elements(G):
    order = G.order()
    elements = list(G.elements)
    
    # Find identity element safely
    identity = None
    for e in elements:
        if e * e == e:
            identity = e
            break
            
    if order == 1:
        return {identity}
        
    factors = factorint(order)
    # Fast path for p-groups: Φ(G) = G^p * G'
    if len(factors) == 1:
        p = list(factors.keys())[0]
        gp_elements = [g**p for g in elements]
        derived = G.derived_subgroup()
        gens = gp_elements + list(derived.generators)
        if not gens:
            gens = [identity]
        Phi = PermutationGroup(gens)
        return set(Phi.elements)
        
    # Fallback for non-p-groups: build subgroup lattice to find maximal subgroups
    G_set = frozenset(elements)
    subgroups = {frozenset([identity]): []}
    queue = [frozenset([identity])]
    
    while queue:
        if len(subgroups) > 500:
            raise ValueError("Group too large to compute Frattini subgroup within limits")
        current_els = queue.pop(0)
        current_gens = subgroups[current_els]
        for g in elements:
            if g not in current_els:
                new_gens = current_gens + [g]
                H = PermutationGroup(new_gens)
                H_els = frozenset(H.elements)
                if H_els not in subgroups:
                    subgroups[H_els] = new_gens
                    queue.append(H_els)
                    
    proper_subgroups = [s for s in subgroups.keys() if s != G_set]
    maximal_subgroups = []
    for M in proper_subgroups:
        is_maximal = True
        for H in proper_subgroups:
            if M != H and M.issubset(H):
                is_maximal = False
                break
        if is_maximal:
            maximal_subgroups.append(M)
            
    if not maximal_subgroups:
        return {identity}
        
    phi_elements = set.intersection(*[set(M) for M in maximal_subgroups])
    return phi_elements

def conditions(witness):
    # H_1: G is a finite p-group
    try:
        order = witness.order()
        if order == 1:
            h1 = True
        else:
            factors = factorint(order)
            h1 = (len(factors) == 1)
    except Exception:
        h1 = False

    # H_2: Φ(G) is the Frattini subgroup of G
    # This is a definitional hypothesis establishing notation.
    try:
        _ = witness.elements
        h2 = True
    except Exception:
        h2 = False

    # ¬Q: The commutator subgroup G' is NOT a subgroup of the Frattini subgroup Φ(G)
    try:
        derived = witness.derived_subgroup()
        derived_els = set(derived.elements)
        phi_els = frattini_subgroup_elements(witness)
        neg_q = not derived_els.issubset(phi_els)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite p-group",
    "H_2: Φ(G) is the Frattini subgroup of G",
    "¬Q: The commutator subgroup G' is NOT a subgroup of the Frattini subgroup Φ(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2