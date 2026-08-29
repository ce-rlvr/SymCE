import itertools

class Z_n:
    def __init__(self, n):
        self.elements = list(range(n))
        self.zero = 0
        self.one = 1
        self.add = lambda a, b: (a + b) % n
        self.mul = lambda a, b: (a * b) % n

Z2 = Z_n(2)
Z3 = Z_n(3)
Z4 = Z_n(4)
Z6 = Z_n(6)
Z8 = Z_n(8)
Z12 = Z_n(12)

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is a proper ideal of R",
    "H_3: I = q_1 \\cap ... \\cap q_n is an irredundant primary decomposition of I",
    "H_4: P_i = \\sqrt{q_i} for i = 1, ..., n are the associated primes of I",
    "¬Q: There exists x in R where (x is a zero divisor on R/I) != (x belongs to P_1 \\cup ... \\cup P_n)"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            ring, I, q_list, P_list = witness
            elements = ring.elements
            add = ring.add
            mul = ring.mul
            zero = ring.zero
            one = ring.one
        elif isinstance(witness, dict):
            elements = witness.get('elements', [])
            add = witness.get('add')
            mul = witness.get('mul')
            zero = witness.get('zero')
            one = witness.get('one')
            I = witness.get('I', [])
            q_list = witness.get('q_list', [])
            P_list = witness.get('P_list', [])
        else:
            elements = getattr(witness, 'elements', [])
            add = getattr(witness, 'add', None)
            mul = getattr(witness, 'mul', None)
            zero = getattr(witness, 'zero', None)
            one = getattr(witness, 'one', None)
            I = getattr(witness, 'I', [])
            q_list = getattr(witness, 'q_list', [])
            P_list = getattr(witness, 'P_list', [])
    except Exception:
        return [False] * 5

    # H1: R is a commutative ring with identity
    h1 = False
    try:
        if elements and add and mul and zero in elements and one in elements:
            is_ring = True
            for a in elements:
                if add(a, zero) != a or add(zero, a) != a: is_ring = False; break
                if mul(a, one) != a or mul(one, a) != a: is_ring = False; break
                has_inv = False
                for b in elements:
                    if add(a, b) == zero and add(b, a) == zero:
                        has_inv = True
                        break
                if not has_inv: is_ring = False; break
                for b in elements:
                    if add(a, b) not in elements: is_ring = False; break
                    if mul(a, b) not in elements: is_ring = False; break
                    if add(a, b) != add(b, a): is_ring = False; break
                    if mul(a, b) != mul(b, a): is_ring = False; break
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)): is_ring = False; break
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): is_ring = False; break
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): is_ring = False; break
            h1 = is_ring
    except Exception:
        h1 = False

    # H2: I is a proper ideal of R
    h2 = False
    try:
        if h1 and I and len(I) < len(elements) and zero in I:
            is_ideal = True
            for a in I:
                for b in I:
                    if add(a, b) not in I: is_ideal = False; break
                for r in elements:
                    if mul(r, a) not in I: is_ideal = False; break
                has_inv = False
                for b in I:
                    if add(a, b) == zero: has_inv = True; break
                if not has_inv: is_ideal = False; break
            h2 = is_ideal
    except Exception:
        h2 = False

    # H3: I = q_1 \cap ... \cap q_n is an irredundant primary decomposition of I
    h3 = False
    try:
        if h2 and q_list:
            is_decomp = True
            for q in q_list:
                if len(q) == len(elements) or zero not in q: is_decomp = False; break
                for a in q:
                    for b in q:
                        if add(a, b) not in q: is_decomp = False; break
                    for r in elements:
                        if mul(r, a) not in q: is_decomp = False; break
            if is_decomp:
                intersection = set(q_list[0])
                for q in q_list[1:]:
                    intersection = intersection.intersection(set(q))
                if set(I) != intersection: is_decomp = False
            if is_decomp:
                for i in range(len(q_list)):
                    inter_others = set(elements)
                    for j in range(len(q_list)):
                        if i != j:
                            inter_others = inter_others.intersection(set(q_list[j]))
                    if inter_others.issubset(set(q_list[i])): is_decomp = False; break
            if is_decomp:
                for q in q_list:
                    for a in elements:
                        for b in elements:
                            if mul(a, b) in q and a not in q:
                                b_m = b
                                found = False
                                for m in range(1, len(elements) + 2):
                                    if b_m in q:
                                        found = True
                                        break
                                    b_m = mul(b_m, b)
                                if not found: is_decomp = False; break
                        if not is_decomp: break
                    if not is_decomp: break
            h3 = is_decomp
    except Exception:
        h3 = False

    # H4: P_i = \sqrt{q_i} for i = 1, ..., n are the associated primes of I
    h4 = False
    try:
        if h3 and len(q_list) == len(P_list):
            is_h4 = True
            for q, P in zip(q_list, P_list):
                radical = set()
                for x in elements:
                    x_m = x
                    for m in range(1, len(elements) + 2):
                        if x_m in q:
                            radical.add(x)
                            break
                        x_m = mul(x_m, x)
                if set(P) != radical: is_h4 = False; break
            if is_h4:
                ass_primes = []
                for x in elements:
                    if x in I: continue
                    ann = set()
                    for y in elements:
                        if mul(x, y) in I:
                            ann.add(y)
                    is_prime = True
                    if len(ann) == len(elements): is_prime = False
                    else:
                        for a in elements:
                            for b in elements:
                                if mul(a, b) in ann:
                                    if a not in ann and b not in ann:
                                        is_prime = False; break
                            if not is_prime: break
                    if is_prime:
                        if ann not in ass_primes:
                            ass_primes.append(ann)
                P_sets = [set(P) for P in P_list]
                if len(P_sets) != len(ass_primes): is_h4 = False
                else:
                    for P in P_sets:
                        if P not in ass_primes: is_h4 = False; break
            h4 = is_h4
    except Exception:
        h4 = False

    # neg_Q: An element x in R is a zero divisor on R/I if and only if x belongs to the union of the associated primes P_1 \cup ... \cup P_n
    neg_q = False
    try:
        if h4:
            union_P = set()
            for P in P_list:
                union_P.update(P)
            
            for x in elements:
                is_zd = False
                if x not in I:
                    for y in elements:
                        if y not in I and mul(x, y) in I:
                            is_zd = True
                            break
                
                in_union = x in union_P
                
                if is_zd != in_union:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]