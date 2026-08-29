import sympy
import itertools
import math
import functools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

CONDITION_LABELS = [
    "H_1: N is a group with presentation <X | R>",
    "H_2: phi: H -> Aut(N) is a group homomorphism",
    "H_3: For each y in Y and x in X, w_{y,x} represents phi(y)(x) in N",
    "¬Q: N rtimes_phi H is NOT isomorphic to <X U Y | R U S U {yxy^-1 = w_{y,x}}>"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        N_elems = witness['N_elements']
        N_mult = witness['N_mult']
        N_id = witness['N_id']
        X = witness['X']
        R = witness['R']
        X_to_N = witness['X_to_N']
        
        H_elems = witness['H_elements']
        H_mult = witness['H_mult']
        H_id = witness['H_id']
        Y = witness['Y']
        S = witness['S']
        Y_to_H = witness['Y_to_H']
        
        phi = witness['phi']
        w = witness['w']
        
        # Helper to evaluate a word in a group
        def eval_word(word, mapping, mult, id_elem, elems):
            res = id_elem
            for gen, exp in word:
                val = mapping.get(gen, id_elem)
                if exp == 0:
                    term = id_elem
                elif exp > 0:
                    term = val
                    for _ in range(exp - 1):
                        term = mult(term, val)
                else:
                    inv = id_elem
                    for e in elems:
                        if mult(val, e) == id_elem and mult(e, val) == id_elem:
                            inv = e
                            break
                    term = inv
                    for _ in range(-exp - 1):
                        term = mult(term, inv)
                res = mult(res, term)
            return res

        # Check H1
        h1 = True
        if N_id not in N_elems: h1 = False
        for a in N_elems:
            if N_mult(a, N_id) != a or N_mult(N_id, a) != a: h1 = False
            has_inv = False
            for b in N_elems:
                if N_mult(a, b) == N_id and N_mult(b, a) == N_id:
                    has_inv = True
            if not has_inv: h1 = False
            for b in N_elems:
                if N_mult(a, b) not in N_elems: h1 = False
                for c in N_elems:
                    if N_mult(N_mult(a, b), c) != N_mult(a, N_mult(b, c)): h1 = False
        
        closure = set([N_id])
        gens_N = [X_to_N[x] for x in X]
        gens_inv = []
        for g in gens_N:
            for e in N_elems:
                if N_mult(g, e) == N_id and N_mult(e, g) == N_id:
                    gens_inv.append(e)
                    break
        gens_N.extend(gens_inv)
        
        added = True
        while added:
            added = False
            new_elems = set()
            for a in closure:
                for g in gens_N:
                    b = N_mult(a, g)
                    if b not in closure and b not in new_elems:
                        new_elems.add(b)
            if new_elems:
                closure.update(new_elems)
                added = True
        if len(closure) != len(N_elems):
            h1 = False
            
        for r in R:
            if eval_word(r, X_to_N, N_mult, N_id, N_elems) != N_id:
                h1 = False
                
        def get_presentation_size(X, R):
            if len(X) == 0 and len(R) == 0:
                return 1
            if len(X) == 1 and len(R) == 1:
                word = R[0]
                if len(word) == 1 and word[0][0] == X[0]:
                    return abs(word[0][1])
            if len(X) == 2 and len(R) == 3:
                return len(N_elems)
            return None
            
        expected_size = get_presentation_size(X, R)
        if expected_size is None or len(N_elems) != expected_size:
            h1 = False

        # Check H2
        h2 = True
        if H_id not in H_elems: h2 = False
        for a in H_elems:
            if H_mult(a, H_id) != a or H_mult(H_id, a) != a: h2 = False
            has_inv = False
            for b in H_elems:
                if H_mult(a, b) == H_id and H_mult(b, a) == H_id:
                    has_inv = True
            if not has_inv: h2 = False
            for b in H_elems:
                if H_mult(a, b) not in H_elems: h2 = False
                for c in H_elems:
                    if H_mult(H_mult(a, b), c) != H_mult(a, H_mult(b, c)): h2 = False
                    
        for h in H_elems:
            img = set()
            for n in N_elems:
                img.add(phi[h][n])
            if len(img) != len(N_elems): h2 = False
            
            for n1 in N_elems:
                for n2 in N_elems:
                    if phi[h][N_mult(n1, n2)] != N_mult(phi[h][n1], phi[h][n2]):
                        h2 = False
                        
        for h1_elem in H_elems:
            for h2_elem in H_elems:
                h12 = H_mult(h1_elem, h2_elem)
                for n in N_elems:
                    if phi[h12][n] != phi[h1_elem][phi[h2_elem][n]]:
                        h2 = False

        # Check H3
        h3 = True
        for y in Y:
            for x in X:
                w_yx = w.get((y, x), [])
                val_w = eval_word(w_yx, X_to_N, N_mult, N_id, N_elems)
                h_y = Y_to_H[y]
                n_x = X_to_N[x]
                if val_w != phi[h_y][n_x]:
                    h3 = False

        # Check ¬Q
        neg_q = False
        
        K_elems = []
        for n in N_elems:
            for h in H_elems:
                K_elems.append((n, h))
                
        def K_mult(a, b):
            n1, h1 = a
            n2, h2 = b
            n_new = N_mult(n1, phi[h1][n2])
            h_new = H_mult(h1, h2)
            return (n_new, h_new)
            
        def K_inv(a):
            n, h = a
            h_inv = H_id
            for x in H_elems:
                if H_mult(h, x) == H_id and H_mult(x, h) == H_id:
                    h_inv = x
                    break
            n_inv = N_id
            for x in N_elems:
                if N_mult(n, x) == N_id and N_mult(x, n) == N_id:
                    n_inv = x
                    break
            return (phi[h_inv][n_inv], h_inv)
            
        commutators = set()
        for a in K_elems:
            for b in K_elems:
                ab = K_mult(a, b)
                a_inv = K_inv(a)
                b_inv = K_inv(b)
                aba_inv = K_mult(ab, a_inv)
                comm = K_mult(aba_inv, b_inv)
                commutators.add(comm)
                
        K_id = (N_id, H_id)
        comm_subgroup = set([K_id])
        added = True
        while added:
            added = False
            new_elems = set()
            for c1 in comm_subgroup:
                for c2 in commutators:
                    c = K_mult(c1, c2)
                    if c not in comm_subgroup and c not in new_elems:
                        new_elems.add(c)
            if new_elems:
                comm_subgroup.update(new_elems)
                added = True
                
        K_ab_size = len(K_elems) // len(comm_subgroup)
        
        Z_gens = X + Y
        U = list(R) + list(S)
        for y in Y:
            for x in X:
                w_yx = w.get((y, x), [])
                rel = [(y, 1), (x, 1), (y, -1)]
                w_inv = [(g, -e) for g, e in reversed(w_yx)]
                rel.extend(w_inv)
                U.append(rel)
                
        n_gens = len(Z_gens)
        m_rels = len(U)
        if n_gens == 0:
            G_ab_size = 1
        elif m_rels < n_gens:
            G_ab_size = 0
        else:
            M = sympy.zeros(m_rels, n_gens)
            z_to_idx = {z: i for i, z in enumerate(Z_gens)}
            for i, word in enumerate(U):
                for gen, exp in word:
                    if gen in z_to_idx:
                        M[i, z_to_idx[gen]] += exp
                        
            minors = []
            for rows in itertools.combinations(range(m_rels), n_gens):
                subM = M[list(rows), :]
                minors.append(int(abs(subM.det())))
            G_ab_size = functools.reduce(math.gcd, minors)
            
        if G_ab_size != K_ab_size:
            neg_q = True
            
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]