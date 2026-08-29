import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import totient
import math
import itertools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # DihedralGroup(2) is isomorphic to the Klein four-group V4
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_automorphisms(G):
    """Computes all automorphisms of a PermutationGroup G."""
    elements = list(G.generate())
    n = len(elements)
    if n == 1:
        return [{elements[0]: elements[0]}]
    if n > 100:
        return None  # Group too large to safely brute-force within time limits
        
    gens = list(G.generators)
    gen_orders = [g.order() for g in gens]
    
    possible_targets = []
    for order in gen_orders:
        targets = [e for e in elements if e.order() == order]
        possible_targets.append(targets)
        
    valid_autos = []
    
    for target_tuple in itertools.product(*possible_targets):
        H = PermutationGroup(*target_tuple)
        if H.order() != n:
            continue
            
        mapping = {gens[i]: target_tuple[i] for i in range(len(gens))}
        
        identity = elements[0]**0
        full_map = {identity: identity}
        queue = [identity]
        is_valid = True
        
        # BFS to build the full homomorphism mapping and check for well-definedness
        while queue and is_valid:
            curr = queue.pop(0)
            curr_mapped = full_map[curr]
            
            for g in gens:
                nxt = curr * g
                nxt_mapped = curr_mapped * mapping[g]
                
                if nxt in full_map:
                    if full_map[nxt] != nxt_mapped:
                        is_valid = False
                        break
                else:
                    full_map[nxt] = nxt_mapped
                    queue.append(nxt)
                    
        if is_valid and len(full_map) == n:
            valid_autos.append(full_map)
            
    return valid_autos

def is_isomorphic_to_Un(G):
    """Checks if Aut(G) is isomorphic to U(n), where n = |G|."""
    n = G.order()
    if n == 1:
        return True
        
    autos = get_automorphisms(G)
    if autos is None:
        raise ValueError("Group too large to compute automorphisms")
        
    if len(autos) != totient(n):
        return False
        
    # U(n) is always abelian. If Aut(G) is not abelian, they are not isomorphic.
    for f in autos:
        for g in autos:
            for x in G.generators:
                if f[g[x]] != g[f[x]]:
                    return False
                    
    # If Aut(G) is abelian and has the correct order, we compare the multisets of element orders.
    # Two finite abelian groups are isomorphic iff they have the same multiset of element orders.
    Un_elements = [x for x in range(1, n) if math.gcd(x, n) == 1]
    Un_orders = []
    for x in Un_elements:
        k = 1
        curr = x
        while curr != 1:
            curr = (curr * x) % n
            k += 1
        Un_orders.append(k)
    Un_orders.sort()
    
    def is_id(m):
        return all(m[x] == x for x in G.generators)
        
    Aut_orders = []
    elements = list(G.generate())
    for f in autos:
        k = 1
        curr_f = f
        while not is_id(curr_f):
            next_f = {}
            for x in elements:
                next_f[x] = f[curr_f[x]]
            curr_f = next_f
            k += 1
        Aut_orders.append(k)
    Aut_orders.sort()
    
    return Un_orders == Aut_orders

def conditions(witness):
    try:
        # H_1: G is a finite group
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        # H_2: The order of G is n (Trivially holds as a definition if G is a finite group)
        h2 = h1
    except Exception:
        h2 = False

    try:
        # ¬Q: Aut(G) is NOT isomorphic to U(n)
        if not h1:
            neg_q = False
        else:
            neg_q = not is_isomorphic_to_Un(witness)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is n",
    "¬Q: Aut(G) is not isomorphic to U(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2