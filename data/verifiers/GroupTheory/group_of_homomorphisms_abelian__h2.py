import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness objects
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, A = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(A, PermutationGroup)
    except Exception:
        h2 = False
        
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            gens = G.generators
            G_elements = list(G.elements)
            A_elements = list(A.elements)
            
            homs = []
            # Find all homomorphisms from G to A by mapping generators
            for target in itertools.product(A_elements, repeat=len(gens)):
                mapping = {G.identity: A.identity}
                queue = [G.identity]
                valid = True
                gen_map = dict(zip(gens, target))
                
                # BFS to build the homomorphism and check relations
                while queue:
                    curr = queue.pop(0)
                    for g in gens:
                        nxt = curr * g
                        nxt_val = mapping[curr] * gen_map[g]
                        if nxt in mapping:
                            if mapping[nxt] != nxt_val:
                                valid = False
                                break
                        else:
                            mapping[nxt] = nxt_val
                            queue.append(nxt)
                    if not valid:
                        break
                
                if valid and len(mapping) == len(G_elements):
                    homs.append(mapping)
            
            forms_group = True
            
            # Check if Hom(G, A) forms an abelian group under pointwise operation
            for f in homs:
                for g in homs:
                    # Check if pointwise operation is commutative (Abelian)
                    for x in G_elements:
                        if f[x] * g[x] != g[x] * f[x]:
                            forms_group = False
                            break
                    if not forms_group:
                        break
                    
                    # Check closure: is the pointwise product f*g a homomorphism?
                    for x in G_elements:
                        for y in G_elements:
                            if (f[x*y] * g[x*y]) != (f[x] * g[x]) * (f[y] * g[y]):
                                forms_group = False
                                break
                        if not forms_group:
                            break
                if not forms_group:
                    break
            
            # Check inverses: is the pointwise inverse of f a homomorphism?
            if forms_group:
                for f in homs:
                    for x in G_elements:
                        for y in G_elements:
                            if (f[x*y]**-1) != (f[x]**-1) * (f[y]**-1):
                                forms_group = False
                                break
                        if not forms_group:
                            break
                    if not forms_group:
                        break
            
            neg_q = not forms_group
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Hom(G, A) is the set of all group homomorphisms from G to A",
    "¬Q: Hom(G, A) does not form an abelian group under pointwise operation"
]

N_HYP = 2
NEG_Q_INDEX = 2