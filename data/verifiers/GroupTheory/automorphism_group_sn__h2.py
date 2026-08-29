import sympy
from sympy.combinatorics.named_groups import SymmetricGroup
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Expected witness format: a tuple (n, phi) or dict {'n': n, 'phi': phi}
    where phi can be a Permutation (for inner automorphisms), a list/tuple of images 
    for the generators of S_n, a dictionary mapping generators to images, or a callable.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            phi_rep = witness.get('phi')
        else:
            n, phi_rep = witness
    except Exception:
        return [False, False, False]

    # H1: Let n be an integer such that n >= 3 and n != 6
    try:
        h1 = isinstance(n, int) and n >= 3 and n != 6
    except Exception:
        h1 = False

    # H2: Let phi be an automorphism of S_n
    h2 = False
    phi_func = None
    try:
        if isinstance(n, int) and n >= 1:
            Sn = SymmetricGroup(n)
            gens = Sn.generators
            id_perm = Permutation(size=n)
            
            if isinstance(phi_rep, Permutation):
                if phi_rep.size <= n:
                    p = Permutation(phi_rep, size=n)
                    phi_func = lambda x, p=p: p * x * (~p)
                    h2 = True
            else:
                if isinstance(phi_rep, (list, tuple)):
                    images = list(phi_rep)
                elif isinstance(phi_rep, dict):
                    norm_phi_rep = {}
                    for k, v in phi_rep.items():
                        try:
                            norm_phi_rep[Permutation(k, size=n)] = v
                        except Exception:
                            pass
                    images = [norm_phi_rep.get(g) for g in gens]
                elif hasattr(phi_rep, '__call__'):
                    images = [phi_rep(g) for g in gens]
                else:
                    images = []
                    
                if len(images) == len(gens) and not any(img is None for img in images):
                    images = [Permutation(img, size=n) for img in images]
                    img_group = PermutationGroup(images)
                    
                    # Check if the images generate a group of the same order
                    if img_group.order() == Sn.order():
                        mapping = {id_perm: id_perm}
                        queue = [id_perm]
                        head = 0
                        is_valid = True
                        max_steps = 500000  # Prevent timeout for excessively large n
                        
                        # BFS to check well-definedness and build the full mapping
                        while head < len(queue) and head < max_steps:
                            curr = queue[head]
                            head += 1
                            curr_img = mapping[curr]
                            
                            for g, img_g in zip(gens, images):
                                nxt = curr * g
                                nxt_img = curr_img * img_g
                                
                                if nxt in mapping:
                                    if mapping[nxt] != nxt_img:
                                        is_valid = False
                                        break
                                else:
                                    mapping[nxt] = nxt_img
                                    queue.append(nxt)
                            if not is_valid:
                                break
                                
                        if is_valid and len(mapping) == Sn.order():
                            phi_func = lambda x, m=mapping, idp=id_perm: m.get(x, idp)
                            h2 = True
    except Exception:
        h2 = False

    # neg_Q: phi is NOT an inner automorphism, OR Aut(S_n) is NOT isomorphic to S_n
    neg_q = False
    try:
        if isinstance(n, int) and n >= 1:
            # Mathematically, Aut(S_n) is isomorphic to S_n iff n != 2 and n != 6
            aut_isomorphic = (n != 2 and n != 6)
            
            is_inner = False
            if phi_func is not None:
                if n <= 1:
                    is_inner = True
                else:
                    # An automorphism of S_n is inner iff it maps transpositions to transpositions
                    t = Permutation(0, 1, size=n)
                    img_t = phi_func(t)
                    cycles = [c for c in img_t.cyclic_form if len(c) > 1]
                    is_inner = (len(cycles) == 1 and len(cycles[0]) == 2)
            
            q = is_inner and aut_isomorphic
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 3 and n != 6",
    "H_2: phi is an automorphism of S_n",
    "¬Q: phi is not an inner automorphism, or Aut(S_n) is not isomorphic to S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2