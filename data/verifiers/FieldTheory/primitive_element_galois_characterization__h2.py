import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings that the witness expression may reference.
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

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion at the given witness.
    
    The dropped hypothesis from the true theorem is that G is exactly the Galois group Gal(L/K).
    Without this, G could be a proper subgroup of Gal(L/K) (or another group acting on L), 
    making the equivalence fail.
    
    We model the fields and actions using Galois correspondence:
    Witness is expected to be a tuple: (Galois_group, H_alpha, G)
    where:
      - Galois_group: PermutationGroup representing Gal(L/K).
      - H_alpha: PermutationGroup representing Gal(L/K(alpha)), must be a subgroup of Galois_group.
      - G: PermutationGroup representing the group G acting on L, modeled as a subgroup of Galois_group.
    """
    try:
        # Unpack the witness
        Galois_group, H_alpha, G = witness
        
        # H_1: L/K is a finite Galois extension
        # Represented by Galois_group being a valid finite PermutationGroup
        h1 = isinstance(Galois_group, PermutationGroup)
        
        # H_2: alpha is an element of L
        # Represented by H_alpha being a subgroup of Galois_group (so K(alpha) is an intermediate field)
        h2 = isinstance(H_alpha, PermutationGroup) and H_alpha.is_subgroup(Galois_group)
        
        # G must be a valid group acting on L. We model this by G being a subgroup of Galois_group.
        if not (isinstance(G, PermutationGroup) and G.is_subgroup(Galois_group)):
            return [False, False, False]
            
        # Prevent performance issues with excessively large groups
        if G.order() > 1000:
            return [False, False, False]
            
        # Conclusion: L = K(alpha) iff the stabilizer of alpha in G is trivial
        # L = K(alpha) corresponds to H_alpha being the trivial subgroup {id}
        L_eq_K_alpha = (H_alpha.order() == 1)
        
        # The stabilizer of alpha in G corresponds to the intersection G \cap H_alpha
        try:
            g_elems = list(G.generate())
        except Exception:
            g_elems = list(G.elements)
            
        stab_elements = [g for g in g_elems if g in H_alpha]
        stab_is_trivial = (len(stab_elements) == 1)
        
        # The conjecture claims these two conditions are equivalent
        q = (L_eq_K_alpha == stab_is_trivial)
        
        # We want the conjecture to FAIL (neg_Q must be True)
        neg_q = not q
        
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "H_2: alpha is an element of L",
    "¬Q: L = K(alpha) is not equivalent to the stabilizer of alpha in G being trivial"
]

N_HYP = 2
NEG_Q_INDEX = 2