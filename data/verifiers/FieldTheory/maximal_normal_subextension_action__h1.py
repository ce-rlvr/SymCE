import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple of 3 PermutationGroup objects: (Gamma, N, M)
    representing the Galois group of the Galois closure, and the subgroups
    corresponding to E and K respectively via the Galois correspondence.
    """
    try:
        Gamma, N, M = witness
        
        def is_subgroup(sub, parent):
            return all(g in parent for g in sub.generators)
            
        # H_1: K is an intermediate field between F and E.
        # In Galois correspondence, F corresponds to Gamma, E to N, K to M.
        # F <= K <= E translates to N <= M <= Gamma.
        h1 = is_subgroup(N, M) and is_subgroup(M, Gamma)
        
        # Find the normalizer of N in Gamma: N_Gamma(N)
        # This corresponds to the automorphisms of E fixing F, i.e., G = Aut(E/F)
        N_gens = N.generators
        N_Gamma_N_gens = []
        for g in Gamma.generate():
            # g normalizes N if g * n * ~g is in N for all generators n of N
            if all((g * n * ~g) in N for n in N_gens):
                N_Gamma_N_gens.append(g)
                
        # J corresponds to the intersection \bigcap_{\sigma \in G} \sigma(K)
        # Intersection of fields corresponds to the join of their subgroups.
        # J = < g * m * ~g | g in N_Gamma(N), m in M.generators >
        J_gens = []
        for g in N_Gamma_N_gens:
            for m in M.generators:
                J_gens.append(g * m * ~g)
        
        if not J_gens:
            id_perm = Gamma.generators[0]**0 if Gamma.generators else Permutation()
            J_gens = [id_perm]
        J = PermutationGroup(J_gens)
        
        # M_Gamma corresponds to the maximal normal extension of F contained in K.
        # This is the normal closure of M in Gamma.
        # M_Gamma = < g * m * ~g | g in Gamma, m in M.generators >
        M_Gamma_gens = []
        for g in Gamma.generate():
            for m in M.generators:
                M_Gamma_gens.append(g * m * ~g)
                
        if not M_Gamma_gens:
            id_perm = Gamma.generators[0]**0 if Gamma.generators else Permutation()
            M_Gamma_gens = [id_perm]
        M_Gamma = PermutationGroup(M_Gamma_gens)
        
        # Conclusion: The intersection is the maximal normal extension of F contained in K.
        # This translates to J == M_Gamma.
        # Since J <= M_Gamma by construction, we just check if M_Gamma <= J.
        conclusion = is_subgroup(M_Gamma, J)
        
        # The negated conclusion must be True for a valid counterexample
        neg_q = not conclusion
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: K is an intermediate field between F and E",
    "¬Q: The intersection of sigma(K) is not the maximal normal extension of F contained in K"
]

N_HYP = 1
NEG_Q_INDEX = 1