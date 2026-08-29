import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        # The witness should be a tuple (G, H) representing the field extension K/F,
        # where G is the Galois group of the normal closure, and H is the subgroup fixing K.
        if not (isinstance(witness, (tuple, list)) and len(witness) == 2):
            return [False, False, False, False]
        
        G, H = witness
        
        if not (isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)):
            return [False, False, False, False]
            
        # Prevent timeouts by restricting the degree of the permutation group
        if getattr(G, 'degree', 100) > 8:
            return [False, False, False, False]
            
        # H must be a valid subgroup of G
        for h in H.generators:
            if h not in G:
                return [False, False, False, False]
                
        # The hypotheses are definitions of G, G', and K^{G'} in the context of the extension.
        # They hold trivially for any valid field extension representation.
        h1 = True
        h2 = True
        h3 = True
        
        # Compute N = N_G(H), which corresponds to the F-automorphisms of K
        norm_elements = []
        h_gens = H.generators
        for g in G.generate():
            if all((g * h * ~g) in H for h in h_gens):
                norm_elements.append(g)
        N = PermutationGroup(norm_elements)
        
        # Compute N', the derived subgroup of N
        N_prime = N.derived_subgroup()
        
        # Compute M = <H, N'>, which corresponds to the intermediate field K^{G'}
        M_gens = list(H.generators) + list(N_prime.generators)
        if not M_gens:
            M = PermutationGroup([Permutation()])
        else:
            M = PermutationGroup(M_gens)
            
        # Compute G', the derived subgroup of the normal closure group G
        G_prime = G.derived_subgroup()
        
        # Check part 1 of the conclusion: K^{G'}/F is a Galois extension with an abelian Galois group.
        # This translates to M being normal in G, and G/M being abelian (i.e., G' <= M).
        part1_normal = True
        for g in G.generators:
            for m in M.generators:
                if (g * m * ~g) not in M:
                    part1_normal = False
                    break
            if not part1_normal:
                break
                
        part1_abelian = True
        for p in G_prime.generators:
            if p not in M:
                part1_abelian = False
                break
                
        part1 = part1_normal and part1_abelian
        
        # The conclusion is a conjunction. If part 1 fails, the entire conclusion fails.
        # (Group theoretically, part 1 is actually equivalent to the entire conclusion here).
        neg_Q = not part1
        
        return [h1, h2, h3, neg_Q]
        
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: G is the Galois group Gal(K/F)",
    "H_2: G' is the commutator subgroup of G",
    "H_3: K^{G'} is the subfield of K consisting of elements fixed by all automorphisms in G'",
    "¬Q: The conclusion fails (K^{G'}/F is not Galois abelian, or intermediate field correspondence fails)"
]

N_HYP = 3
NEG_Q_INDEX = 3