import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import itertools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_automorphisms(G):
    elements = list(G.elements)
    # Find the identity element
    identity = next(e for e in elements if e * e == e)
    gens = G.generators
    
    # Group elements by their order to optimize finding valid images for generators
    elements_by_order = {}
    for x in elements:
        o = x.order()
        if o not in elements_by_order:
            elements_by_order[o] = []
        elements_by_order[o].append(x)
        
    valid_images = []
    for g in gens:
        valid_images.append(elements_by_order.get(g.order(), []))
        
    auts = []
    for img_tuple in itertools.product(*valid_images):
        mapping = {identity: identity}
        queue = [identity]
        is_homo = True
        
        head = 0
        # BFS to build the homomorphism
        while head < len(queue):
            curr = queue[head]
            head += 1
            for i, g in enumerate(gens):
                nxt = curr * g
                nxt_img = mapping[curr] * img_tuple[i]
                if nxt in mapping:
                    if mapping[nxt] != nxt_img:
                        is_homo = False
                        break
                else:
                    mapping[nxt] = nxt_img
                    queue.append(nxt)
            if not is_homo:
                break
                
        # An injective homomorphism from a finite set to itself is bijective
        if is_homo and len(mapping) == len(elements):
            auts.append(mapping)
            
    return auts, elements

def conditions(witness) -> list[bool]:
    try:
        auts, elements = get_automorphisms(witness)
        center_size = 0
        
        for phi in auts:
            in_center = True
            for psi in auts:
                for x in elements:
                    # Check if phi and psi commute: phi(psi(x)) == psi(phi(x))
                    if phi[psi[x]] != psi[phi[x]]:
                        in_center = False
                        break
                if not in_center:
                    break
            
            if in_center:
                center_size += 1
                # If we find more than 1 element in the center, it's not trivial
                if center_size > 1:
                    break
                    
        # The conclusion fails if the center of Aut(G) is NOT trivial
        neg_q = (center_size > 1)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The center of the automorphism group of G is not the trivial group"
]
N_HYP = 0
NEG_Q_INDEX = 0