import sympy
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup

# Top-level setup
# No specific named groups are needed since the witness will provide presentations directly.

def free_reduce(word):
    if not isinstance(word, list):
        return []
    reduced = []
    for term in word:
        g, p = term
        if p == 0: continue
        if reduced and reduced[-1][0] == g:
            new_p = reduced[-1][1] + p
            reduced.pop()
            if new_p != 0:
                reduced.append((g, new_p))
        else:
            reduced.append((g, p))
    return reduced

def apply_phi(word, phi):
    result = []
    for term in word:
        g, p = term
        if g not in phi:
            return None
        img = phi[g]
        if p > 0:
            for _ in range(p):
                result.extend(img)
        elif p < 0:
            inv_img = [(ig, -ip) for ig, ip in reversed(img)]
            for _ in range(-p):
                result.extend(inv_img)
    return free_reduce(result)

def check_words(words, gens):
    if not isinstance(words, list): return False
    for w in words:
        if not isinstance(w, list): return False
        for term in w:
            if not (isinstance(term, tuple) or isinstance(term, list)) or len(term) != 2: return False
            g, p = term
            if g not in gens or not isinstance(p, int): return False
    return True

def conditions(witness):
    try:
        X1 = witness.get('X1', [])
        R1 = witness.get('R1', [])
        X2 = witness.get('X2', [])
        R2 = witness.get('R2', [])
        A_gens = witness.get('A_gens', [])
        A_rels = witness.get('A_rels', [])
        phi1 = witness.get('phi1', {})
        phi2 = witness.get('phi2', {})
        ker_w = witness.get('ker_w', [])
        ker_phi = witness.get('ker_phi', 1)
        
        # H1: G1 has presentation <X1 | R1> and G2 has presentation <X2 | R2>
        h1 = True
        if not isinstance(X1, list) or not all(isinstance(x, str) for x in X1): h1 = False
        if not isinstance(X2, list) or not all(isinstance(x, str) for x in X2): h1 = False
        if not check_words(R1, X1): h1 = False
        if not check_words(R2, X2): h1 = False
                
        # H2: X1 and X2 are disjoint sets
        h2 = False
        if h1 and isinstance(X1, list) and isinstance(X2, list):
            h2 = set(X1).isdisjoint(set(X2))
        
        # H3: A is a group (presented by A_gens, A_rels)
        h3 = True
        if not isinstance(A_gens, list) or not all(isinstance(x, str) for x in A_gens): h3 = False
        if not check_words(A_rels, A_gens): h3 = False
                
        # Check that phi1 and phi2 are valid homomorphisms
        h_phi = True
        if not isinstance(phi1, dict) or not isinstance(phi2, dict):
            h_phi = False
        else:
            for g, img in phi1.items():
                if g not in A_gens: h_phi = False
                if not check_words([img], X1): h_phi = False
            for g, img in phi2.items():
                if g not in A_gens: h_phi = False
                if not check_words([img], X2): h_phi = False
                
        if h_phi:
            for r in A_rels:
                img1 = apply_phi(r, phi1)
                img2 = apply_phi(r, phi2)
                if img1 is None or free_reduce(img1) != []: h_phi = False
                if img2 is None or free_reduce(img2) != []: h_phi = False
            
        # neg_Q: The amalgamated free product does not admit the presentation
        # This happens if the maps phi1 or phi2 are not injective (monomorphisms).
        # We verify this by checking if the provided ker_w is a non-trivial element in the kernel.
        neg_q = False
        if h_phi and A_rels == [] and check_words([ker_w], A_gens):
            red_ker = free_reduce(ker_w)
            if red_ker != []:
                if ker_phi == 1:
                    img = apply_phi(ker_w, phi1)
                    if img is not None and free_reduce(img) == []:
                        neg_q = True
                elif ker_phi == 2:
                    img = apply_phi(ker_w, phi2)
                    if img is not None and free_reduce(img) == []:
                        neg_q = True
                        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: G1 has presentation <X1 | R1> and G2 has presentation <X2 | R2>",
    "H_2: X1 and X2 are disjoint sets",
    "H_3: A is a group",
    "¬Q: The amalgamated free product G1 *_A G2 does not admit the presentation (e.g. maps are not injective)"
]

N_HYP = 3
NEG_Q_INDEX = 3