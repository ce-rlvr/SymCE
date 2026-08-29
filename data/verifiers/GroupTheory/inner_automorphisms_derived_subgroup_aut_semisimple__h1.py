import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a semisimple group",
    "H_2: Let Aut(G) be the automorphism group of G",
    "H_3: Let Inn(G) be the group of inner automorphisms of G",
    "¬Q: Inn(G) is not a subgroup of the derived subgroup of Aut(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_semisimple(G):
    """
    A finite group is semisimple if it has no non-trivial abelian normal subgroups.
    Equivalently, its solvable radical is trivial.
    """
    try:
        if not hasattr(G, 'normal_subgroups'):
            return False
        if G.order() == 1:
            return True
        for N in G.normal_subgroups():
            if N.order() > 1 and N.is_abelian:
                return False
        return True
    except Exception:
        return False

def get_automorphisms(G):
    """
    Computes all automorphisms of a permutation group G.
    Returns the list of automorphisms (as tuples of mapped indices),
    along with element indexing and multiplication table for further use.
    """
    elements = list(G.generate())
    n = len(elements)
    elem_idx = {e: i for i, e in enumerate(elements)}
    
    identity = None
    for e in elements:
        if e * e == e:
            identity = e
            break
            
    gens = G.generators
    gen_indices = [elem_idx[g] for g in gens]
    
    mul_table = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mul_table[i][j] = elem_idx[elements[i] * elements[j]]
            
    orders = [e.order() for e in elements]
    gen_orders = [orders[i] for i in gen_indices]
    
    # An automorphism must map a generator to an element of the same order
    candidates = [[i for i in range(n) if orders[i] == go] for go in gen_orders]
    
    automorphisms = []
    for prod in itertools.product(*candidates):
        valid = True
        map_full = [-1] * n
        map_full[elem_idx[identity]] = elem_idx[identity]
        
        queue = [0] * n
        queue[0] = elem_idx[identity]
        head = 0
        tail = 1
        
        # BFS to build the homomorphism and check for contradictions simultaneously
        while head < tail:
            curr = queue[head]
            head += 1
            mapped_curr = map_full[curr]
            
            for j_idx, g_idx in enumerate(gen_indices):
                nxt = mul_table[curr][g_idx]
                mapped_nxt = mul_table[mapped_curr][prod[j_idx]]
                
                if map_full[nxt] != -1:
                    if map_full[nxt] != mapped_nxt:
                        valid = False
                        break
                else:
                    map_full[nxt] = mapped_nxt
                    queue[tail] = nxt
                    tail += 1
            if not valid:
                break
                
        if valid and tail == n:
            # Check bijectivity
            if len(set(map_full)) == n:
                automorphisms.append(tuple(map_full))
                
    return automorphisms, elem_idx, elements, mul_table

def check_conclusion(G):
    automorphisms, elem_idx, elements, mul_table = get_automorphisms(G)
    n = len(elements)
    
    aut_perms = [Permutation(list(m)) for m in automorphisms]
    if not aut_perms:
        return False
        
    AutG = PermutationGroup(aut_perms)
    AutG_derived = AutG.derived_subgroup()
    
    inn_perms = []
    for g in elements:
        g_idx = elem_idx[g]
        g_inv_idx = elem_idx[g**-1]
        map_g = [0] * n
        for x_idx in range(n):
            map_g[x_idx] = mul_table[mul_table[g_idx][x_idx]][g_inv_idx]
        inn_perms.append(Permutation(map_g))
        
    InnG = PermutationGroup(inn_perms)
    
    # Check if InnG is a subgroup of AutG_derived
    for gen in InnG.generators:
        if not AutG_derived.contains(gen):
            return False
    return True

def conditions(witness):
    try:
        h1 = is_semisimple(witness)
    except Exception:
        h1 = False
        
    # H2 and H3 are definitions
    h2 = True
    h3 = True
    
    try:
        q = check_conclusion(witness)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]