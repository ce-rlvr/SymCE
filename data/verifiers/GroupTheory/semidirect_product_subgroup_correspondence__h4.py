import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for standard groups
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

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: phi is a group homomorphism from H to Aut(N)",
    "¬Q: The map K -> N x K is NOT a lattice isomorphism from subgroups of H to subgroups of G containing N_tilde"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            N, H, phi = witness
        else:
            N = witness.N
            H = witness.H
            phi = witness.phi
    except Exception:
        return [False, False, False]

    def get_elements(G):
        if hasattr(G, 'elements'):
            return list(G.elements)
        elif hasattr(G, 'generate'):
            return list(G.generate())
        else:
            return list(G)

    def get_op(G):
        if hasattr(G, 'op'):
            return G.op
        else:
            return lambda a, b: a * b

    def get_phi(h, n):
        if callable(phi):
            try:
                return phi(h, n)
            except TypeError:
                return phi(h)(n)
        else:
            return phi[h][n]

    # H_1: N and H are groups
    h1_ok = False
    try:
        N_elements = get_elements(N)
        H_elements = get_elements(H)
        
        N_op_func = get_op(N)
        H_op_func = get_op(H)
        
        N_id = None
        for e in N_elements:
            if all(N_op_func(e, a) == a and N_op_func(a, e) == a for a in N_elements):
                N_id = e
                break
        if N_id is not None:
            N_is_group = True
            for a in N_elements:
                has_inv = False
                for b in N_elements:
                    if N_op_func(a, b) == N_id and N_op_func(b, a) == N_id:
                        has_inv = True
                        break
                if not has_inv:
                    N_is_group = False
                    break
            if N_is_group:
                for a in N_elements:
                    for b in N_elements:
                        if N_op_func(a, b) not in N_elements:
                            N_is_group = False
                            break
        else:
            N_is_group = False
            
        H_id = None
        for e in H_elements:
            if all(H_op_func(e, a) == a and H_op_func(a, e) == a for a in H_elements):
                H_id = e
                break
        if H_id is not None:
            H_is_group = True
            for a in H_elements:
                has_inv = False
                for b in H_elements:
                    if H_op_func(a, b) == H_id and H_op_func(b, a) == H_id:
                        has_inv = True
                        break
                if not has_inv:
                    H_is_group = False
                    break
            if H_is_group:
                for a in H_elements:
                    for b in H_elements:
                        if H_op_func(a, b) not in H_elements:
                            H_is_group = False
                            break
        else:
            H_is_group = False
            
        h1_ok = N_is_group and H_is_group
    except Exception:
        h1_ok = False

    # H_2: phi is a group homomorphism from H to Aut(N)
    h2_ok = True
    try:
        if h1_ok:
            for h in H_elements:
                mapped = []
                for n in N_elements:
                    pn = get_phi(h, n)
                    if pn not in N_elements:
                        h2_ok = False
                        break
                    mapped.append(pn)
                if not h2_ok: break
                
                if len(set(mapped)) != len(N_elements):
                    h2_ok = False
                    break
                    
                for n1 in N_elements:
                    for n2 in N_elements:
                        if get_phi(h, N_op_func(n1, n2)) != N_op_func(get_phi(h, n1), get_phi(h, n2)):
                            h2_ok = False
                            break
                    if not h2_ok: break
                if not h2_ok: break
                
            if h2_ok:
                for h1 in H_elements:
                    for h2 in H_elements:
                        for n in N_elements:
                            if get_phi(H_op_func(h1, h2), n) != get_phi(h1, get_phi(h2, n)):
                                h2_ok = False
                                break
                        if not h2_ok: break
                    if not h2_ok: break
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # neg_Q: The map K -> N x K is NOT a lattice isomorphism
    neg_q = False
    try:
        if h1_ok and h2_ok:
            G_elements = [(n, h) for n in N_elements for h in H_elements]
            G_id = (N_id, H_id)
            
            def G_op(x, y):
                n1, h1 = x
                n2, h2 = y
                return (N_op_func(n1, get_phi(h1, n2)), H_op_func(h1, h2))
                
            def get_all_subgroups_indices(elements_list, op_func, identity):
                n = len(elements_list)
                try:
                    elem_to_idx = {e: i for i, e in enumerate(elements_list)}
                    def get_idx(e): return elem_to_idx[e]
                except TypeError:
                    def get_idx(e): return elements_list.index(e)
                
                op_table = [[0]*n for _ in range(n)]
                for i in range(n):
                    for j in range(n):
                        op_table[i][j] = get_idx(op_func(elements_list[i], elements_list[j]))
                        
                id_idx = get_idx(identity)
                
                def generate_subgroup(generators):
                    sg = set(generators)
                    sg.add(id_idx)
                    active = list(sg)
                    while active:
                        new_active = []
                        for a in active:
                            for b in sg:
                                c = op_table[a][b]
                                if c not in sg:
                                    sg.add(c)
                                    new_active.append(c)
                                c2 = op_table[b][a]
                                if c2 not in sg:
                                    sg.add(c2)
                                    new_active.append(c2)
                        active = new_active
                    return frozenset(sg)

                subgroups = set()
                cyclic_subgroups = set()
                for i in range(n):
                    sg = generate_subgroup([i])
                    cyclic_subgroups.add(sg)
                    subgroups.add(sg)
                    
                active = list(cyclic_subgroups)
                while active:
                    new_subgroups = set()
                    for sg1 in active:
                        for sg2 in subgroups:
                            if sg1.issubset(sg2): continue
                            joined = generate_subgroup(sg1 | sg2)
                            if joined not in subgroups and joined not in new_subgroups:
                                new_subgroups.add(joined)
                    subgroups.update(new_subgroups)
                    active = list(new_subgroups)
                    
                return subgroups, get_idx

            H_subgroups_idx, H_get_idx = get_all_subgroups_indices(H_elements, H_op_func, H_id)
            G_subgroups_idx, G_get_idx = get_all_subgroups_indices(G_elements, G_op, G_id)
            
            N_tilde_idx = frozenset([G_get_idx((n, H_id)) for n in N_elements])
            G_subgroups_containing_N_idx = {sg for sg in G_subgroups_idx if N_tilde_idx.issubset(sg)}
            
            mapped_subgroups_idx = set()
            is_bijection = True
            for K_idx in H_subgroups_idx:
                K_elems = [H_elements[i] for i in K_idx]
                S_K_idx = frozenset([G_get_idx((n, k)) for n in N_elements for k in K_elems])
                if S_K_idx not in G_subgroups_containing_N_idx:
                    is_bijection = False
                    break
                mapped_subgroups_idx.add(S_K_idx)
                
            if is_bijection and len(mapped_subgroups_idx) != len(G_subgroups_containing_N_idx):
                is_bijection = False
                
            if not is_bijection:
                neg_q = True
            else:
                is_lattice_iso = True
                for K1_idx in H_subgroups_idx:
                    for K2_idx in H_subgroups_idx:
                        K1_elems = [H_elements[i] for i in K1_idx]
                        K2_elems = [H_elements[i] for i in K2_idx]
                        S_K1_idx = frozenset([G_get_idx((n, k)) for n in N_elements for k in K1_elems])
                        S_K2_idx = frozenset([G_get_idx((n, k)) for n in N_elements for k in K2_elems])
                        if K1_idx.issubset(K2_idx) != S_K1_idx.issubset(S_K2_idx):
                            is_lattice_iso = False
                            break
                    if not is_lattice_iso:
                        break
                if not is_lattice_iso:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]