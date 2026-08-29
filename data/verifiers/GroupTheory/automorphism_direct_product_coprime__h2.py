import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for potential witness expressions
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

def direct_product(G, H):
    """Constructs the direct product of two permutation groups."""
    degG = G.degree
    degH = H.degree
    if degG == 0: degG = 1
    if degH == 0: degH = 1
    
    gens = []
    for g in G.generators:
        if g.is_Identity:
            continue
        a = [g(i) for i in range(degG)] + list(range(degG, degG + degH))
        gens.append(Permutation(a))
        
    for h in H.generators:
        if h.is_Identity:
            continue
        a = list(range(degG)) + [degG + h(i) for i in range(degH)]
        gens.append(Permutation(a))
        
    if not gens:
        return PermutationGroup([Permutation(degG + degH - 1)])
    return PermutationGroup(gens)

def get_automorphism_count(G):
    """Computes the order of the automorphism group of a permutation group G."""
    elements = list(G.generate())
    n = len(elements)
    if n == 1:
        return 1
    gens = G.generators
    
    element_orders = {g: g.order() for g in elements}
    
    valid_targets = []
    for g in gens:
        o = g.order()
        valid_targets.append([e for e in elements if element_orders[e] == o])
        
    identity = next(e for e in elements if e.is_Identity)
        
    def build_homomorphism(target_gens):
        mapping = {identity: identity}
        queue = [identity]
        
        while queue:
            curr = queue.pop(0)
            curr_mapped = mapping[curr]
            for g, tg in zip(gens, target_gens):
                nxt = curr * g
                nxt_mapped = curr_mapped * tg
                if nxt in mapping:
                    if mapping[nxt] != nxt_mapped:
                        return None
                else:
                    mapping[nxt] = nxt_mapped
                    queue.append(nxt)
        return mapping

    aut_count = 0
    for target_gens in itertools.product(*valid_targets):
        mapping = build_homomorphism(target_gens)
        # An endomorphism of a finite group is an automorphism iff it is surjective (hence bijective)
        if mapping is not None and len(set(mapping.values())) == n:
            aut_count += 1
            
    return aut_count

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    Returns [H_1_ok, neg_Q_ok]
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        G, H = witness
        
        # H_1: G and H are finite groups
        if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            GxH = direct_product(G, H)
            
            aut_G = get_automorphism_count(G)
            aut_H = get_automorphism_count(H)
            aut_GxH = get_automorphism_count(GxH)
            
            # neg_Q: Aut(G x H) is NOT isomorphic to Aut(G) x Aut(H)
            # Since Aut(G) x Aut(H) naturally embeds into Aut(G x H), 
            # they are isomorphic if and only if they have the same order.
            neg_q = (aut_GxH != aut_G * aut_H)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are finite groups",
    "¬Q: Aut(G x H) is not isomorphic to Aut(G) x Aut(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1