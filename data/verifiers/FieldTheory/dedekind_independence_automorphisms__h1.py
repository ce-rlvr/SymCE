import itertools

# Top-level setup
# The witness is expected to provide the field K, ring L, and homomorphisms.
# No special named objects are required here.

CONDITION_LABELS = [
    "H_1: sigma_1, ..., sigma_n are distinct field homomorphisms from K to L",
    "¬Q: The homomorphisms are linearly dependent over L"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    def get(name):
        if isinstance(witness, dict):
            return witness[name]
        return getattr(witness, name)

    try:
        K = list(get('K'))
        L = list(get('L'))
        sigmas = list(get('sigmas'))
        add_K = get('add_K')
        mul_K = get('mul_K')
        add_L = get('add_L')
        mul_L = get('mul_L')
        zero_K = get('zero_K')
        one_K = get('one_K')
        zero_L = get('zero_L')
        one_L = get('one_L')
        
        n = len(sigmas)
        if n < 1:
            h1 = False
        else:
            h1 = True
            
            # Check K is a field
            if zero_K == one_K:
                h1 = False
            else:
                for x in K:
                    for y in K:
                        if mul_K(x, y) != mul_K(y, x):
                            h1 = False
                            break
                    if not h1: break
                
                if h1:
                    for x in K:
                        if x == zero_K: continue
                        has_inv = False
                        for y in K:
                            if mul_K(x, y) == one_K:
                                has_inv = True
                                break
                        if not has_inv:
                            h1 = False
                            break
            
            # Check homomorphisms
            if h1:
                for sigma in sigmas:
                    if sigma(zero_K) != zero_L:
                        h1 = False; break
                    if sigma(one_K) != one_L:
                        h1 = False; break
                    for x in K:
                        for y in K:
                            if sigma(add_K(x, y)) != add_L(sigma(x), sigma(y)):
                                h1 = False; break
                            if sigma(mul_K(x, y)) != mul_L(sigma(x), sigma(y)):
                                h1 = False; break
                        if not h1: break
                    if not h1: break
            
            # Check distinctness
            if h1:
                for i in range(n):
                    for j in range(i + 1, n):
                        same = True
                        for x in K:
                            if sigmas[i](x) != sigmas[j](x):
                                same = False
                                break
                        if same:
                            h1 = False
                            break
                    if not h1: break
    except Exception:
        h1 = False

    try:
        dependent = False
        for c in itertools.product(L, repeat=n):
            if all(ci == zero_L for ci in c):
                continue
            
            is_zero_for_all = True
            for x in K:
                current_sum = zero_L
                for i in range(n):
                    term = mul_L(c[i], sigmas[i](x))
                    current_sum = add_L(current_sum, term)
                if current_sum != zero_L:
                    is_zero_for_all = False
                    break
            if is_zero_for_all:
                dependent = True
                break
        neg_q = dependent
    except Exception:
        neg_q = False

    return [h1, neg_q]