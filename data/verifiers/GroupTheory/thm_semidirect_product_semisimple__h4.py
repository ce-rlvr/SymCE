import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_subgroup(sub, G):
    for gen in sub.generators:
        if gen not in G:
            return False
    return True

def is_normal_subgroup(sub, G):
    if not is_subgroup(sub, G):
        return False
    for g in G.generators:
        for n in sub.generators:
            conj = ~g * n * g
            if conj not in sub:
                return False
    return True

def is_semisimple(G):
    """
    A finite group is semisimple if it has no non-trivial abelian normal subgroups.
    Equivalently, no non-trivial element has an abelian normal closure.
    """
    if G.order() == 1:
        return True
    
    gens = list(G.generators)
    gens_inv = [~x for x in gens]
    all_gens = gens + gens_inv
    
    elements = list(G.generate_dimino())
    for g in elements:
        if g.is_Identity:
            continue
        # Optimization: only check elements of prime order.
        # Any non-trivial abelian normal subgroup contains an element of prime order.
        if not isprime(g.order()):
            continue
            
        # Find the conjugacy class of g (which generates its normal closure)
        conjugates_set = {g}
        queue = [g]
        while queue:
            curr = queue.pop(0)
            for gen in all_gens:
                conj = ~gen * curr * gen
                if conj not in conjugates_set:
                    conjugates_set.add(conj)
                    queue.append(conj)
        
        # Check if the normal closure is abelian by checking if its generators mutually commute
        conjugates = list(conjugates_set)
        is_ab = True
        for i in range(len(conjugates)):
            for j in range(i + 1, len(conjugates)):
                if conjugates[i] * conjugates[j] != conjugates[j] * conjugates[i]:
                    is_ab = False
                    break
            if not is_ab:
                break
        
        if is_ab:
            return False
            
    return True

def check_Q(G, N, H):
    if not is_normal_subgroup(H, G):
        return False
    if not is_normal_subgroup(N, G):
        return False
    if N.order() * H.order() != G.order():
        return False
    for n in N.generate_dimino():
        if not n.is_Identity and n in H:
            return False
    return True

def conditions(witness):
    if isinstance(witness, dict):
        G = witness.get('G')
        N = witness.get('N')
        H = witness.get('H')
    else:
        try:
            G, N, H = witness
        except Exception:
            return [False, False, False, False]
            
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = h1 and is_semisimple(G)
    except Exception:
        h2 = False
        
    try:
        h3 = h1 and isinstance(N, PermutationGroup) and is_normal_subgroup(N, G)
    except Exception:
        h3 = False
        
    try:
        # H must be a valid subgroup of G to be considered a valid witness component
        if not (isinstance(H, PermutationGroup) and is_subgroup(H, G)):
            neg_q = False
        else:
            q = check_Q(G, N, H)
            neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "H_3: N is a normal subgroup of G",
    "¬Q: H is not a normal subgroup of G, or G is not the internal direct product of N and H"
]

N_HYP = 3
NEG_Q_INDEX = 3