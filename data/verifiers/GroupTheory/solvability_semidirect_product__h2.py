import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup

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

def conditions(witness):
    try:
        N, H, phi = witness
    except Exception:
        return [False, False]
        
    # H_1: N and H are groups
    try:
        h1 = (hasattr(N, 'elements') or hasattr(N, 'generate')) and \
             (hasattr(H, 'elements') or hasattr(H, 'generate')) and \
             hasattr(N, 'is_solvable') and hasattr(H, 'is_solvable')
        h1 = bool(h1)
    except Exception:
        h1 = False
        
    # Conclusion: N \rtimes_\phi H is a solvable group iff both N and H are solvable groups
    try:
        def apply_phi(phi, h, n):
            if isinstance(phi, dict):
                if (h, n) in phi:
                    return phi[(h, n)]
                elif h in phi:
                    val = phi[h]
                    if isinstance(val, dict) and n in val:
                        return val[n]
                    elif callable(val):
                        return val(n)
            elif callable(phi):
                try:
                    return phi(h, n)
                except Exception:
                    return phi(h)(n)
            raise ValueError("Invalid phi")
            
        try:
            N_elems = list(N.elements)
        except AttributeError:
            N_elems = list(N.generate())
            
        try:
            H_elems = list(H.elements)
        except AttributeError:
            H_elems = list(H.generate())
            
        G_elems = [(n, h) for n in N_elems for h in H_elems]
        elem_to_idx = {elem: i for i, elem in enumerate(G_elems)}
        
        n_G = len(G_elems)
        mul_table = []
        is_group = True
        for x in G_elems:
            row = []
            for y in G_elems:
                n1, h1 = x
                n2, h2 = y
                
                try:
                    mapped_n2 = apply_phi(phi, h1, n2)
                except Exception:
                    is_group = False
                    break
                    
                if mapped_n2 not in N_elems:
                    is_group = False
                    break
                    
                n_res = n1 * mapped_n2
                h_res = h1 * h2
                
                res = (n_res, h_res)
                if res not in elem_to_idx:
                    is_group = False
                    break
                row.append(elem_to_idx[res])
            if not is_group:
                break
            mul_table.append(row)
            
        if is_group:
            # Check associativity
            for i in range(n_G):
                for j in range(n_G):
                    for k in range(n_G):
                        if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]:
                            is_group = False
                            break
                    if not is_group: break
                if not is_group: break
                
        if is_group:
            # Check identity
            identity = None
            for i in range(n_G):
                is_id = True
                for j in range(n_G):
                    if mul_table[i][j] != j or mul_table[j][i] != j:
                        is_id = False
                        break
                if is_id:
                    identity = i
                    break
            if identity is None:
                is_group = False
                
        if is_group:
            # Check inverses
            for i in range(n_G):
                has_inv = False
                for j in range(n_G):
                    if mul_table[i][j] == identity and mul_table[j][i] == identity:
                        has_inv = True
                        break
                if not has_inv:
                    is_group = False
                    break
                    
        if is_group:
            perms = []
            for i in range(n_G):
                p = Permutation(mul_table[i])
                perms.append(p)
            G_grp = PermutationGroup(perms)
            P_eval = bool(G_grp.is_solvable)
        else:
            P_eval = False
            
        N_solv = bool(N.is_solvable)
        H_solv = bool(H.is_solvable)
        Q_eval = (P_eval == (N_solv and H_solv))
        neg_q = not Q_eval
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "¬Q: N \\rtimes_\\phi H is a solvable group iff both N and H are solvable groups (fails)"
]
N_HYP = 1
NEG_Q_INDEX = 1