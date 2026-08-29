import sympy
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup, coset_enumeration_r

try:
    from sympy.matrices.normalforms import smith_normal_form
except ImportError:
    smith_normal_form = None

# Top-level setup for witness construction
F1, x = free_group("x")
F2, a, b = free_group("a, b")
F3, a, b, c = free_group("a, b, c")

CONDITION_LABELS = [
    "H_1: G is a group with presentation <X | R>",
    "H_2: H is a subgroup of G",
    "¬Q: The presentation given by the transversal T is not isomorphic to H"
]

N_HYP = 2
NEG_Q_INDEX = 2

def trace_word(C, w):
    state = 0
    for letter in w:
        idx = C.A.index(letter)
        state = C.table[state][idx]
    return state

def rewrite_word(w, C, state_to_t, S_words, F_H_gens, F_H, F):
    current_state = 0
    rewritten = F_H.identity
    for letter in w:
        gen_idx, exp = letter.array_form[0]
        if exp > 0:
            x_letter = letter
            t = state_to_t[current_state]
            tx = t * x_letter
            tx_bar = state_to_t[trace_word(C, tx)]
            s = tx * tx_bar**-1
            if s != F.identity:
                idx = S_words.index(s)
                rewritten = rewritten * F_H_gens[idx]
            current_state = C.table[current_state][C.A.index(letter)]
        else:
            x_letter = letter**-1
            next_state = C.table[current_state][C.A.index(letter)]
            t = state_to_t[next_state]
            tx = t * x_letter
            tx_bar = state_to_t[trace_word(C, tx)]
            s = tx * tx_bar**-1
            if s != F.identity:
                idx = S_words.index(s)
                rewritten = rewritten * F_H_gens[idx]**-1
            current_state = next_state
    return rewritten

def build_presentation(C, state_to_t, T_list, F, R):
    S_words = []
    for t in T_list:
        for x_gen in F.generators:
            tx = t * x_gen
            tx_bar = state_to_t[trace_word(C, tx)]
            s = tx * tx_bar**-1
            if s != F.identity and s not in S_words:
                S_words.append(s)
                
    if len(S_words) == 0:
        return None, []
        
    F_H = free_group(f"y0:{len(S_words)}")[0]
    F_H_gens = list(F_H.generators)
        
    R_H_words = []
    for t in T_list:
        for r in R:
            w = t * r * t**-1
            rewritten = rewrite_word(w, C, state_to_t, S_words, F_H_gens, F_H, F)
            R_H_words.append(rewritten)
            
    return F_H, R_H_words

def abelian_invariants(F_group, R_words):
    if F_group is None:
        return []
    gens = list(F_group.generators)
    n = len(gens)
    m = len(R_words)
    if n == 0:
        return []
    if m == 0:
        return [0] * n
    
    M = sympy.zeros(m, n)
    for i, r in enumerate(R_words):
        counts = {g: 0 for g in gens}
        for letter in r:
            gen_idx, exp = letter.array_form[0]
            g = F_group.generators[gen_idx]
            counts[g] += exp
        for j, g in enumerate(gens):
            M[i, j] = counts[g]
            
    if smith_normal_form is None:
        return None
    try:
        SNF = smith_normal_form(M)
    except Exception:
        return None
        
    invariants = []
    for i in range(min(m, n)):
        val = abs(SNF[i, i])
        if val == 0:
            invariants.append(0)
        elif val > 1:
            invariants.append(val)
    for i in range(m, n):
        invariants.append(0)
        
    return sorted(invariants)

def conditions(witness):
    try:
        F, R, H_gens, T = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = hasattr(F, 'generators') and isinstance(R, list)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(H_gens, list)
    except Exception:
        h2 = False
        
    neg_q = False
    try:
        G = FpGroup(F, R)
        C = coset_enumeration_r(G, H_gens)
        
        if len(T) != len(C.table):
            neg_q = False
        else:
            seen = set()
            test_state_to_t = {}
            is_transversal = True
            for t in T:
                state = trace_word(C, t)
                if state in seen:
                    is_transversal = False
                    break
                seen.add(state)
                test_state_to_t[state] = t
                
            if not is_transversal:
                neg_q = False
            else:
                test_F_H, test_R_H = build_presentation(C, test_state_to_t, T, F, R)
                test_inv = abelian_invariants(test_F_H, test_R_H)
                
                valid_state_to_t = {0: F.identity}
                queue = [0]
                while queue:
                    state = queue.pop(0)
                    for i, letter in enumerate(C.A):
                        next_state = C.table[state][i]
                        if next_state not in valid_state_to_t:
                            valid_state_to_t[next_state] = valid_state_to_t[state] * letter
                            queue.append(next_state)
                            
                valid_F_H, valid_R_H = build_presentation(C, valid_state_to_t, list(valid_state_to_t.values()), F, R)
                valid_inv = abelian_invariants(valid_F_H, valid_R_H)
                
                if test_inv is None or valid_inv is None:
                    neg_q = False
                else:
                    neg_q = (test_inv != valid_inv)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]