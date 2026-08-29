import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.named_groups import AbelianGroup
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

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: phi is a group homomorphism from H to Aut(N)",
    "¬Q: N' is not a normal subgroup of G isomorphic to N"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False]
        N, H, phi, G = witness
    except Exception:
        return [False, False, False]
        
    # H1: N and H are groups
    try:
        h1 = hasattr(N, 'elements') and hasattr(H, 'elements') and hasattr(N, 'identity') and hasattr(H, 'identity')
    except Exception:
        h1 = False
        
    # H2: phi is a homomorphism from H to Aut(N)
    try:
        h2 = False
        if h1:
            N_elems = list(N.elements)
            H_elems = list(H.elements)
            
            is_hom = True
            # Check if phi(h) is an automorphism
            for h in H_elems:
                f = phi[h] if isinstance(phi, dict) else phi(h)
                mapped = []
                for n in N_elems:
                    fn = f[n] if isinstance(f, dict) else f(n)
                    if fn not in N_elems:
                        is_hom = False
                        break
                    mapped.append(fn)
                if not is_hom: break
                
                unique_mapped = []
                for m in mapped:
                    if m not in unique_mapped:
                        unique_mapped.append(m)
                if len(unique_mapped) != len(N_elems):
                    is_hom = False
                    break
                    
                # Check homomorphism of f
                for n1 in N_elems:
                    for n2 in N_elems:
                        fn1 = f[n1] if isinstance(f, dict) else f(n1)
                        fn2 = f[n2] if isinstance(f, dict) else f(n2)
                        fn12 = f[n1 * n2] if isinstance(f, dict) else f(n1 * n2)
                        if fn12 != fn1 * fn2:
                            is_hom = False
                            break
                    if not is_hom: break
                if not is_hom: break
                
            if is_hom:
                # Check if phi is a homomorphism
                for h1_elem in H_elems:
                    for h2_elem in H_elems:
                        f12 = phi[h1_elem * h2_elem] if isinstance(phi, dict) else phi(h1_elem * h2_elem)
                        f1 = phi[h1_elem] if isinstance(phi, dict) else phi(h1_elem)
                        f2 = phi[h2_elem] if isinstance(phi, dict) else phi(h2_elem)
                        for n in N_elems:
                            f2_n = f2[n] if isinstance(f2, dict) else f2(n)
                            f1_f2_n = f1[f2_n] if isinstance(f1, dict) else f1(f2_n)
                            f12_n = f12[n] if isinstance(f12, dict) else f12(n)
                            if f12_n != f1_f2_n:
                                is_hom = False
                                break
                        if not is_hom: break
                    if not is_hom: break
            h2 = is_hom
    except Exception:
        h2 = False
        
    # Conclusion Q: N' is a normal subgroup of G isomorphic to N
    try:
        q = False
        if h1:
            N_elems = list(N.elements)
            H_elems = list(H.elements)
            e_H = H.identity
            N_prime = [(n, e_H) for n in N_elems]
            
            if callable(G) or isinstance(G, dict):
                def G_op(x, y):
                    if isinstance(G, dict):
                        return G[(x, y)]
                    return G(x, y)
                    
                G_set = [(n, h) for n in N_elems for h in H_elems]
                
                is_group = True
                # Closure
                for g1 in G_set:
                    for g2 in G_set:
                        try:
                            g3 = G_op(g1, g2)
                        except Exception:
                            is_group = False
                            break
                        if g3 not in G_set:
                            is_group = False
                            break
                    if not is_group: break
                    
                if is_group:
                    # Associativity
                    if len(G_set) > 60:
                        samples = []
                        n_g = len(G_set)
                        for i in range(1000):
                            idx1 = (i * 137 + 13) % n_g
                            idx2 = (i * 277 + 17) % n_g
                            idx3 = (i * 331 + 19) % n_g
                            samples.append((G_set[idx1], G_set[idx2], G_set[idx3]))
                    else:
                        samples = [(g1, g2, g3) for g1 in G_set for g2 in G_set for g3 in G_set]
                        
                    for g1, g2, g3 in samples:
                        if G_op(G_op(g1, g2), g3) != G_op(g1, G_op(g2, g3)):
                            is_group = False
                            break
                            
                if is_group:
                    # Identity
                    identity = None
                    for e in G_set:
                        is_id = True
                        for g in G_set:
                            if G_op(e, g) != g or G_op(g, e) != g:
                                is_id = False
                                break
                        if is_id:
                            identity = e
                            break
                    if identity is None:
                        is_group = False
                        
                if is_group:
                    # Inverses
                    inverses = {}
                    for g in G_set:
                        has_inv = False
                        for inv in G_set:
                            if G_op(g, inv) == identity and G_op(inv, g) == identity:
                                has_inv = True
                                inverses[g] = inv
                                break
                        if not has_inv:
                            is_group = False
                            break
                            
                if is_group:
                    # Check N' is normal subgroup
                    is_normal = True
                    if identity not in N_prime:
                        is_normal = False
                    
                    if is_normal:
                        for x in N_prime:
                            for y in N_prime:
                                if G_op(x, y) not in N_prime:
                                    is_normal = False
                                    break
                            if not is_normal: break
                            if inverses[x] not in N_prime:
                                is_normal = False
                                break
                                
                    if is_normal:
                        for g in G_set:
                            g_inv = inverses[g]
                            for x in N_prime:
                                conj = G_op(g, G_op(x, g_inv))
                                if conj not in N_prime:
                                    is_normal = False
                                    break
                            if not is_normal: break
                            
                    if is_normal:
                        # Check isomorphism
                        natural_iso = True
                        for n1 in N_elems:
                            for n2 in N_elems:
                                if G_op((n1, e_H), (n2, e_H)) != (n1 * n2, e_H):
                                    natural_iso = False
                                    break
                            if not natural_iso: break
                            
                        if natural_iso:
                            q = True
                        else:
                            if len(N_elems) <= 7:
                                is_iso = False
                                for p in itertools.permutations(N_prime):
                                    mapping = dict(zip(N_elems, p))
                                    valid = True
                                    for n1 in N_elems:
                                        for n2 in N_elems:
                                            if mapping[n1 * n2] != G_op(mapping[n1], mapping[n2]):
                                                valid = False
                                                break
                                        if not valid: break
                                    if valid:
                                        is_iso = True
                                        break
                                q = is_iso
                            else:
                                q = False
            else:
                try:
                    G_elems = list(G.elements)
                    is_subset = True
                    for x in N_prime:
                        if x not in G_elems:
                            is_subset = False
                            break
                    if is_subset:
                        pass
                except Exception:
                    pass
    except Exception:
        q = False
        
    neg_q = not q
    return [bool(h1), bool(h2), bool(neg_q)]