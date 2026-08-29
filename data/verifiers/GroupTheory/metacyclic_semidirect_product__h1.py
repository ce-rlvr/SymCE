import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup

# Standard group bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def group_profile(G_elements):
    """Returns a profile to uniquely identify small groups up to isomorphism."""
    order = len(G_elements)
    is_abelian = True
    elements = list(G_elements)
    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            if elements[i] * elements[j] != elements[j] * elements[i]:
                is_abelian = False
                break
        if not is_abelian:
            break
            
    orders = []
    for g in elements:
        k = 1
        curr = g
        while not curr.is_Identity:
            curr = curr * g
            k += 1
        orders.append(k)
        
    return (order, is_abelian, tuple(sorted(orders)))

def get_all_subgroups(G):
    """Generates all subgroups of a small permutation group."""
    elements = list(G.elements)
    id_el = G.identity
    
    all_sgs = set()
    all_sgs.add(tuple([id_el]))
    
    cyclic_sgs = set()
    for g in elements:
        sg = set()
        curr = g
        while curr not in sg:
            sg.add(curr)
            curr = curr * g
        t = tuple(sorted(list(sg), key=lambda p: p.array_form))
        cyclic_sgs.add(t)
        all_sgs.add(t)
        
    def closure(gens):
        sg = set(gens)
        queue = list(gens)
        while queue:
            x = queue.pop(0)
            new_elements = []
            for y in sg:
                xy = x * y
                if xy not in sg:
                    new_elements.append(xy)
                yx = y * x
                if yx not in sg and yx not in new_elements:
                    new_elements.append(yx)
            for e in new_elements:
                sg.add(e)
                queue.append(e)
        return sg

    new_sgs = list(cyclic_sgs)
    while new_sgs:
        next_sgs = []
        for sg1 in new_sgs:
            for sg2 in cyclic_sgs:
                if set(sg2).issubset(set(sg1)):
                    continue
                gens = set(sg1).union(set(sg2))
                cl = closure(gens)
                t = tuple(sorted(list(cl), key=lambda p: p.array_form))
                if t not in all_sgs:
                    all_sgs.add(t)
                    next_sgs.append(t)
        new_sgs = next_sgs
        
    return [set(t) for t in all_sgs]

def is_normal_subgroup(G, sg_elements):
    for h in G.elements:
        for n in sg_elements:
            if (h * n * ~h) not in sg_elements:
                return False
    return True

def check_semidirect_product_and_cyclic_H(G, N=None, H=None):
    try:
        G_elements = list(G.elements)
    except Exception:
        return False, False
        
    all_sgs = get_all_subgroups(G)
    
    if N is not None and H is not None:
        try:
            N_elements = list(N.elements)
            H_elements = list(H.elements)
        except Exception:
            return False, False
            
        is_H_cyclic = False
        for h in H_elements:
            k = 1
            curr = h
            while not curr.is_Identity:
                curr = curr * h
                k += 1
            if k == len(H_elements):
                is_H_cyclic = True
                break
                
        if len(G_elements) != len(N_elements) * len(H_elements):
            is_sdp = False
        else:
            N_profile = group_profile(N_elements)
            H_profile = group_profile(H_elements)
            
            N_candidates = [sg for sg in all_sgs if len(sg) == len(N_elements) and is_normal_subgroup(G, sg) and group_profile(sg) == N_profile]
            H_candidates = [sg for sg in all_sgs if len(sg) == len(H_elements) and group_profile(sg) == H_profile]
            
            is_sdp = False
            id_el = G.identity
            for n_sg in N_candidates:
                for h_sg in H_candidates:
                    if n_sg.intersection(h_sg) == {id_el}:
                        is_sdp = True
                        break
                if is_sdp:
                    break
                    
        return is_H_cyclic, is_sdp

    else:
        found_sdp = False
        found_cyclic_H = False
        
        normal_sgs = [sg for sg in all_sgs if is_normal_subgroup(G, sg)]
        id_el = G.identity
        
        for n_sg in normal_sgs:
            for h_sg in all_sgs:
                if len(n_sg) * len(h_sg) == len(G_elements):
                    if n_sg.intersection(h_sg) == {id_el}:
                        found_sdp = True
                        is_h_cyclic = False
                        for h in h_sg:
                            k = 1
                            curr = h
                            while not curr.is_Identity:
                                curr = curr * h
                                k += 1
                            if k == len(h_sg):
                                is_h_cyclic = True
                                break
                        if is_h_cyclic:
                            found_cyclic_H = True
                            break
            if found_cyclic_H:
                break
                
        if found_cyclic_H:
            return True, True
        elif found_sdp:
            return False, True
        else:
            return False, False

def is_metacyclic(G):
    try:
        elements = list(G.elements)
    except Exception:
        return False
    
    order_G = len(elements)
    
    for g in elements:
        N_elements = set()
        curr = g
        while curr not in N_elements:
            N_elements.add(curr)
            curr = curr * g
            
        is_normal = True
        for h in elements:
            conj = h * g * (~h)
            if conj not in N_elements:
                is_normal = False
                break
                
        if is_normal:
            q_order = order_G // len(N_elements)
            if q_order == 1:
                return True
                
            is_quotient_cyclic = False
            for x in elements:
                x_k = x
                k = 1
                while k < q_order and x_k not in N_elements:
                    x_k = x_k * x
                    k += 1
                if k == q_order and x_k in N_elements:
                    is_quotient_cyclic = True
                    break
            
            if is_quotient_cyclic:
                return True
                
    return False

def conditions(witness):
    N = None
    H = None
    G = None
    
    if isinstance(witness, tuple):
        if len(witness) == 3:
            N, H, G = witness
        elif len(witness) == 1:
            G = witness[0]
        else:
            G = witness
    elif isinstance(witness, dict):
        N = witness.get('N')
        H = witness.get('H')
        G = witness.get('G')
    else:
        G = witness
        
    try:
        h1_ok, h2_ok = check_semidirect_product_and_cyclic_H(G, N, H)
    except Exception:
        h1_ok, h2_ok = False, False
        
    try:
        neg_q = not is_metacyclic(G)
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: H is a cyclic group",
    "H_2: G is an external semidirect product of N and H",
    "¬Q: G is not a metacyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2