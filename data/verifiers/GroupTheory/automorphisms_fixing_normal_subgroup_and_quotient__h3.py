import itertools
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_A(G, N):
    """
    Computes the group of automorphisms A of G that fix N as a set 
    and induce the identity on G/N (i.e., fix G/N elementwise).
    """
    elements = sorted(list(G.elements), key=lambda p: p.array_form)
    gens = sorted(list(G.generators), key=lambda p: p.array_form)
    N_elements = sorted(list(N.elements), key=lambda p: p.array_form)
    
    identity = elements[0] * (~elements[0])
    
    # Precompute a word in the generators for each element in G
    word_for = {}
    word_for[identity] = []
    queue = [identity]
    while queue:
        curr = queue.pop(0)
        for i, g in enumerate(gens):
            nxt = curr * g
            if nxt not in word_for:
                word_for[nxt] = word_for[curr] + [i]
                queue.append(nxt)
                
    A_funcs = []
    choices = []
    # For phi to induce the identity on G/N, we must have phi(g) in gN
    for g in gens:
        choices.append([g * n for n in N_elements])
        
    for mapping in itertools.product(*choices):
        phi = {}
        # Evaluate the homomorphism defined by this mapping
        for elem in elements:
            word = word_for[elem]
            val = identity
            for idx in word:
                val = val * mapping[idx]
            phi[elem] = val
            
        # Verify it is a valid homomorphism
        valid = True
        for elem in elements:
            for i, g in enumerate(gens):
                if phi[elem * g] != phi[elem] * mapping[i]:
                    valid = False
                    break
            if not valid:
                break
                
        # Verify it is bijective (surjective is enough for finite sets)
        if valid and len(set(phi.values())) == len(elements):
            A_funcs.append(phi)
            
    return A_funcs

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1 = hasattr(G, 'elements') and hasattr(G, 'generators')
    except Exception:
        h1 = False
        
    # H_2: N is an abelian normal subgroup of G
    try:
        is_sub = all(n in G.elements for n in N.elements)
        
        is_norm = True
        for g in G.elements:
            for n in N.elements:
                if g * n * (~g) not in N.elements:
                    is_norm = False
                    break
            if not is_norm:
                break
                
        is_ab = True
        for x in N.elements:
            for y in N.elements:
                if x * y != y * x:
                    is_ab = False
                    break
            if not is_ab:
                break
                
        h2 = is_sub and is_norm and is_ab
    except Exception:
        h2 = False
        
    # ¬Q: A is NOT an abelian subgroup of Aut(G)
    try:
        A_funcs = get_A(G, N)
        elements = list(G.elements)
        is_A_ab = True
        for phi in A_funcs:
            for psi in A_funcs:
                for x in elements:
                    if phi[psi[x]] != psi[phi[x]]:
                        is_A_ab = False
                        break
                if not is_A_ab:
                    break
            if not is_A_ab:
                break
        neg_q = not is_A_ab
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is an abelian normal subgroup of G",
    "¬Q: A is not an abelian subgroup of Aut(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2