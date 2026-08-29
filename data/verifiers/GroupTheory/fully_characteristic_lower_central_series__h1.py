import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from itertools import product

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        if len(witness) == 3:
            G, i, H = witness
            try:
                lcs = G.lower_central_series()
                H_expected = lcs[i]
                h1 = (H == H_expected)
            except Exception:
                h1 = False
        elif len(witness) == 2:
            G, i = witness
            try:
                lcs = G.lower_central_series()
                H = lcs[i]
                h1 = True
            except Exception:
                h1 = False
        else:
            return [False, False]
    except Exception:
        return [False, False]

    if not h1:
        return [False, False]

    try:
        gens = G.generators
        if not gens:
            is_fc = True
        else:
            try:
                identity = G.identity
            except Exception:
                identity = gens[0] ** 0
                
            elements = []
            for count, e in enumerate(G.generate()):
                if count > 2000:
                    break
                elements.append(e)
            
            if len(elements) > 2000:
                return [h1, False]
                
            valid_images_per_gen = []
            for g in gens:
                try:
                    order_g = g.order()
                    valid_images = [e for e in elements if order_g % e.order() == 0]
                except Exception:
                    valid_images = elements
                valid_images_per_gen.append(valid_images)
                
            candidates = list(product(*valid_images_per_gen))
            if len(candidates) > 50000:
                return [h1, False]
                
            is_fc = True
            for images in candidates:
                mapping = {identity: identity}
                queue = [identity]
                gen_to_img = list(zip(gens, images))
                
                is_homo = True
                idx = 0
                while idx < len(queue):
                    curr = queue[idx]
                    idx += 1
                    curr_img = mapping[curr]
                    
                    for g, img_g in gen_to_img:
                        nxt = curr * g
                        nxt_img = curr_img * img_g
                        
                        if nxt in mapping:
                            if mapping[nxt] != nxt_img:
                                is_homo = False
                                break
                        else:
                            mapping[nxt] = nxt_img
                            queue.append(nxt)
                    if not is_homo:
                        break
                        
                if is_homo:
                    h_inv = True
                    for h_gen in H.generators:
                        if h_gen in mapping:
                            if mapping[h_gen] not in H:
                                h_inv = False
                                break
                    if not h_inv:
                        is_fc = False
                        break
                        
        neg_q = not is_fc
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: \\gamma_i(G) is the i-th term of the lower central series of G",
    "¬Q: \\gamma_i(G) is not a fully characteristic subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1