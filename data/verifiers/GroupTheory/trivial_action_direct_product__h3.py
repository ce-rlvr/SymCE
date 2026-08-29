import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
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

def check_H2(N, H, phi):
    N_elems = list(N.generate())
    H_elems = list(H.generate())
    
    # Check if phi(h, n) is in N
    for h in H_elems:
        for n in N_elems:
            if phi(h, n) not in N_elems:
                return False
                
    # Check if phi(h, .) is a homomorphism N -> N
    for h in H_elems:
        for n1 in N_elems:
            for n2 in N_elems:
                if phi(h, n1 * n2) != phi(h, n1) * phi(h, n2):
                    return False
                    
    # Check if phi(h, .) is bijective (surjective is enough for finite sets)
    for h in H_elems:
        mapped = [phi(h, n) for n in N_elems]
        if len(set(mapped)) != len(N_elems):
            return False
            
    # Check if phi is a homomorphism H -> Aut(N)
    # phi(h1 * h2)(n) == phi(h1)(phi(h2)(n))
    for h1 in H_elems:
        for h2 in H_elems:
            for n in N_elems:
                if phi(h1 * h2, n) != phi(h1, phi(h2, n)):
                    return False
                    
    return True

def check_neg_Q(N, H, phi):
    N_elems = list(N.generate())
    H_elems = list(H.generate())
    
    id_N = N_elems[0] ** 0 if N_elems else None
    id_H = H_elems[0] ** 0 if H_elems else None
    id_elem = (id_N, id_H)
    
    G_elems = [(n, h) for n in N_elems for h in H_elems]
    
    def mult_direct(e1, e2):
        return (e1[0] * e2[0], e1[1] * e2[1])
        
    def mult_semi(e1, e2):
        return (e1[0] * phi(e1[1], e2[0]), e1[1] * e2[1])
        
    def is_abelian(elems, mult):
        for a in elems:
            for b in elems:
                if mult(a, b) != mult(b, a):
                    return False
        return True
        
    if is_abelian(G_elems, mult_direct) != is_abelian(G_elems, mult_semi):
        return True
        
    def get_orders(elems, mult):
        orders = []
        for e in elems:
            curr = e
            order = 1
            while curr != id_elem:
                curr = mult(curr, e)
                order += 1
                if order > len(elems) + 1:
                    break
            orders.append(order)
        return sorted(orders)
        
    if get_orders(G_elems, mult_direct) != get_orders(G_elems, mult_semi):
        return True
        
    def center_size(elems, mult):
        size = 0
        for a in elems:
            in_center = True
            for b in elems:
                if mult(a, b) != mult(b, a):
                    in_center = False
                    break
            if in_center:
                size += 1
        return size
        
    if center_size(G_elems, mult_direct) != center_size(G_elems, mult_semi):
        return True
        
    def get_inv(elems, mult):
        inv_dict = {}
        for a in elems:
            for b in elems:
                if mult(a, b) == id_elem:
                    inv_dict[a] = b
                    break
        return lambda x: inv_dict[x]
        
    inv_direct = get_inv(G_elems, mult_direct)
    inv_semi = get_inv(G_elems, mult_semi)
    
    def num_conjugacy_classes(elems, mult, inv):
        classes = set()
        for a in elems:
            c_class = set()
            for g in elems:
                c_class.add(mult(mult(g, a), inv(g)))
            classes.add(frozenset(c_class))
        return len(classes)
        
    if num_conjugacy_classes(G_elems, mult_direct, inv_direct) != num_conjugacy_classes(G_elems, mult_semi, inv_semi):
        return True
        
    return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        N, H, phi = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = check_H2(N, H, phi) if h1_ok else False
    except Exception:
        h2_ok = False
        
    try:
        neg_q = check_neg_Q(N, H, phi) if h1_ok else False
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: phi is a group homomorphism from H to Aut(N)",
    "¬Q: N ⋊_phi H is not isomorphic to N x H"
]

N_HYP = 2
NEG_Q_INDEX = 2