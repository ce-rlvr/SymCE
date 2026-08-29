import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def extract_G_A(witness):
    if isinstance(witness, dict):
        return witness['G'], witness['A']
    return witness[0], witness[1]

def conditions(witness) -> list[bool]:
    # H_1: A is an abelian group
    try:
        G, A = extract_G_A(witness)
        h1 = bool(A.is_abelian)
    except Exception:
        h1 = False

    # H_2: Hom(G, A) is the set of all group homomorphisms from G to A
    try:
        G, A = extract_G_A(witness)
        # Verify that G and A are valid groups so the definition makes sense
        _ = G.generators
        _ = A.generators
        h2 = True
    except Exception:
        h2 = False

    # neg_Q: Hom(G, A) does NOT form an abelian group under pointwise multiplication
    try:
        G, A = extract_G_A(witness)
        G_elems = list(G.generate())
        A_elems = list(A.generate())
        gens = G.generators
        homs = []
        
        # Find all valid homomorphisms from G to A
        for p in itertools.product(A_elems, repeat=len(gens)):
            mapping = dict(zip(gens, p))
            hom = {G.identity: A.identity}
            queue = [G.identity]
            valid = True
            
            # BFS to construct the homomorphism mapping
            while queue:
                curr = queue.pop(0)
                for g in gens:
                    nxt = curr * g
                    val = hom[curr] * mapping[g]
                    if nxt in hom:
                        if hom[nxt] != val:
                            valid = False
                            break
                    else:
                        hom[nxt] = val
                        queue.append(nxt)
                if not valid:
                    break
                    
            # Rigorous check to ensure it's a valid homomorphism
            if valid and len(hom) == len(G_elems):
                is_hom = True
                for x in G_elems:
                    for y in G_elems:
                        if hom[x * y] != hom[x] * hom[y]:
                            is_hom = False
                            break
                    if not is_hom:
                        break
                if is_hom:
                    homs.append(hom)
        
        # Remove duplicates
        unique_homs = []
        seen = set()
        for h in homs:
            tup = tuple(h[x] for x in G_elems)
            if tup not in seen:
                seen.add(tup)
                unique_homs.append(h)
                
        if not unique_homs:
            # A group cannot be empty
            neg_q = True
        else:
            hom_tups = [tuple(h[x] for x in G_elems) for h in unique_homs]
            hom_set = set(hom_tups)
            
            is_group = True
            
            # Check closure and commutativity
            for f in unique_homs:
                for g in unique_homs:
                    fg_tup = tuple(f[x] * g[x] for x in G_elems)
                    if fg_tup not in hom_set:
                        is_group = False
                        break
                    gf_tup = tuple(g[x] * f[x] for x in G_elems)
                    if fg_tup != gf_tup:
                        is_group = False
                        break
                if not is_group:
                    break
                    
            # Check identity
            if is_group:
                e_tup = tuple(A.identity for x in G_elems)
                if e_tup not in hom_set:
                    is_group = False
                    
            # Check inverses
            if is_group:
                for f in unique_homs:
                    f_inv_tup = tuple(f[x]**-1 for x in G_elems)
                    if f_inv_tup not in hom_set:
                        is_group = False
                        break
                        
            neg_q = not is_group
            
    except Exception:
        # If any operation fails (e.g., pointwise multiplication is undefined), it's not a group
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an abelian group",
    "H_2: Hom(G, A) is the set of all group homomorphisms from G to A",
    "¬Q: Hom(G, A) does not form an abelian group under pointwise multiplication"
]
N_HYP = 2
NEG_Q_INDEX = 2