import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.homomorphisms import homomorphism
from sympy.combinatorics import PermutationGroup
from itertools import product

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def upper_central_series_term(G, i):
    """Computes the i-th term of the upper central series of G."""
    Z_elements = {G.identity}
    for _ in range(i):
        next_Z_elements = set()
        for x in G.elements:
            # x is in Z_{k+1} iff [x, g] is in Z_k for all generators g of G
            # Commutator [x, g] = x^-1 * g^-1 * x * g
            if all((x**-1 * g**-1 * x * g) in Z_elements for g in G.generators):
                next_Z_elements.add(x)
        if len(next_Z_elements) == len(Z_elements):
            break
        Z_elements = next_Z_elements
    return PermutationGroup(list(Z_elements))

def is_characteristic(G, H):
    """Checks if H is a characteristic subgroup of G."""
    gens = G.generators
    H_elements = set(H.elements)
    
    gen_orders = [g.order() for g in gens]
    
    # Group elements by order to optimize automorphism search
    elements_by_order = {}
    for g in G.elements:
        o = g.order()
        if o not in elements_by_order:
            elements_by_order[o] = []
        elements_by_order[o].append(g)
        
    valid_images_per_gen = []
    for o in gen_orders:
        valid_images_per_gen.append(elements_by_order.get(o, []))
        
    # Iterate over all possible generator mappings that preserve order
    for images in product(*valid_images_per_gen):
        try:
            phi = homomorphism(G, G, gens, images)
            if phi.is_injective():
                # phi is an automorphism. Check if phi(H) == H.
                # Since H is finite and phi is injective, phi(H) subset H implies phi(H) = H.
                for h in H.generators:
                    if phi(h) not in H_elements:
                        return False
        except Exception:
            # The mapping does not extend to a valid homomorphism
            pass
    return True

def conditions(witness) -> list[bool]:
    try:
        # Parse witness
        if isinstance(witness, dict):
            G = witness.get('G')
            i = witness.get('i')
            H = witness.get('H', None)
        elif isinstance(witness, tuple) and len(witness) == 3:
            G, i, H = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, i = witness
            H = None
        else:
            return [False, False]

        # Validate types
        if G is None or i is None:
            return [False, False]
        if not hasattr(G, 'elements'):
            return [False, False]
        if not isinstance(i, int) or i < 0:
            return [False, False]

        # Evaluate Hypothesis 1
        Z_i = upper_central_series_term(G, i)
        if H is not None:
            h1 = (set(H.elements) == set(Z_i.elements))
        else:
            H = Z_i
            h1 = True
            
        # Evaluate Negated Conclusion
        neg_q = not is_characteristic(G, H)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: Z_i(G) is the i-th term of the upper central series of G",
    "¬Q: Z_i(G) is not a characteristic subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1