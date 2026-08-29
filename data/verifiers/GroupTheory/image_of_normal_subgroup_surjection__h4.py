import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            phi = witness.get('phi')
            N = witness.get('N')
        else:
            G, H, phi, N = witness
    except Exception:
        return [False, False, False, False]

    def get_elements(group):
        if hasattr(group, 'generate') and callable(group.generate):
            return list(group.generate())
        elif hasattr(group, 'elements'):
            return list(group.elements)
        else:
            return list(group)

    def check_is_group(obj):
        if isinstance(obj, PermutationGroup) or getattr(obj, 'is_group', False):
            elems = get_elements(obj)
        elif isinstance(obj, (list, tuple, set)):
            elems = list(obj)
        else:
            return False, [], None

        if not elems:
            return False, [], None

        try:
            id_elem = None
            for e in elems:
                if all(e * x == x and x * e == x for x in elems):
                    id_elem = e
                    break
            if id_elem is None:
                return False, [], None

            for x in elems:
                if not any(x * y == id_elem and y * x == id_elem for y in elems):
                    return False, [], None

            if not (isinstance(obj, PermutationGroup) or getattr(obj, 'is_group', False)):
                for x in elems:
                    for y in elems:
                        if x * y not in elems:
                            return False, [], None

            return True, elems, id_elem
        except Exception:
            return False, [], None

    # H1: G is a group
    try:
        h1, G_elems, G_id = check_is_group(G)
    except Exception:
        h1 = False
        G_elems = []
        G_id = None

    # H2: H is a group
    try:
        h2, H_elems, H_id = check_is_group(H)
    except Exception:
        h2 = False
        H_elems = []
        H_id = None

    # H3: phi is a surjective group homomorphism from G to H
    evaluate_phi = None
    try:
        if not (h1 and h2):
            h3 = False
        else:
            if isinstance(phi, dict):
                try:
                    domain_ok = all(g in phi for g in G_elems)
                    evaluate_phi = lambda g: phi[g]
                except TypeError:
                    domain_ok = False
            elif callable(phi):
                evaluate_phi = phi
                domain_ok = True
            else:
                domain_ok = False

            if domain_ok:
                mapped_elements = [evaluate_phi(g) for g in G_elems]
                
                codomain_ok = True
                for m in mapped_elements:
                    if m not in H_elems:
                        codomain_ok = False
                        break
                
                hom_ok = True
                if codomain_ok:
                    for g1 in G_elems:
                        for g2 in G_elems:
                            if evaluate_phi(g1 * g2) != evaluate_phi(g1) * evaluate_phi(g2):
                                hom_ok = False
                                break
                        if not hom_ok:
                            break
                else:
                    hom_ok = False
                    
                if codomain_ok and hom_ok:
                    image = []
                    for m in mapped_elements:
                        if m not in image:
                            image.append(m)
                    surj_ok = len(image) == len(H_elems) and all(h in image for h in H_elems)
                else:
                    surj_ok = False
                    
                h3 = codomain_ok and hom_ok and surj_ok
            else:
                h3 = False
    except Exception:
        h3 = False

    # neg_Q: phi(N) is NOT a normal subgroup of H
    try:
        if not (h1 and h2 and h3 and evaluate_phi is not None):
            neg_q = False
        else:
            if isinstance(N, PermutationGroup) or getattr(N, 'is_group', False):
                N_elems = get_elements(N)
            else:
                N_elems = list(N)
                
            phi_N = []
            for n in N_elems:
                if n in G_elems:
                    val = evaluate_phi(n)
                    if val not in phi_N:
                        phi_N.append(val)
            
            is_subgroup = True
            if not phi_N:
                is_subgroup = False
            elif H_id not in phi_N:
                is_subgroup = False
            else:
                for x in phi_N:
                    for y in phi_N:
                        if x * y not in phi_N:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                
                if is_subgroup:
                    for x in phi_N:
                        has_inv = any(x * y == H_id and y * x == H_id for y in phi_N)
                        if not has_inv:
                            is_subgroup = False
                            break
                            
            if not is_subgroup:
                neg_q = True
            else:
                is_normal = True
                for h in H_elems:
                    h_inv = None
                    for y in H_elems:
                        if h * y == H_id and y * h == H_id:
                            h_inv = y
                            break
                    
                    if h_inv is None:
                        is_normal = False
                        break
                        
                    for n in phi_N:
                        if h * n * h_inv not in phi_N:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                neg_q = not is_normal
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a group",
    "H_3: phi is a surjective group homomorphism from G to H",
    "¬Q: phi(N) is not a normal subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3