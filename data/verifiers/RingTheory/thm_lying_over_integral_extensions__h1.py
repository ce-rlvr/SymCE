import itertools
import sympy
from sympy import eye, zeros

# Top-level setup for standard objects
I2 = eye(2)
O2 = zeros(2, 2)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the Lying Over Theorem conjecture.
    
    The witness should provide:
      - S: list of elements in the extension ring
      - R: list of elements in the subring
      - P: list of elements in the prime ideal of R
      - add(a, b): addition function
      - mul(a, b): multiplication function
      - zero: the additive identity
    """
    try:
        S = witness.S
        R = witness.R
        P = witness.P
        add = witness.add
        mul = witness.mul
        zero = witness.zero
    except AttributeError:
        try:
            S = witness['S']
            R = witness['R']
            P = witness['P']
            add = witness['add']
            mul = witness['mul']
            zero = witness['zero']
        except Exception:
            return [False, False, False, False]

    def contains(lst, item):
        return any(x == item for x in lst)

    def index_of(lst, item):
        for i, x in enumerate(lst):
            if x == item:
                return i
        raise ValueError("Item not found")

    # H_1: R is a subring of S
    try:
        h1 = True
        if not all(contains(S, r) for r in R): h1 = False
        if not contains(R, zero): h1 = False
        if h1:
            for a in R:
                for b in R:
                    if not contains(R, add(a, b)): h1 = False
                    if not contains(R, mul(a, b)): h1 = False
                if not any(add(a, x) == zero for x in R): h1 = False
            
            has_id = False
            for e in R:
                if all(mul(e, r) == r and mul(r, e) == r for r in R):
                    has_id = True
                    break
            if not has_id: h1 = False
    except Exception:
        h1 = False

    # H_2: S is an integral extension of R
    try:
        h2 = True
        id_R = None
        for e in R:
            if all(mul(e, r) == r and mul(r, e) == r for r in R):
                id_R = e
                break
        if id_R is None:
            h2 = False
        else:
            for s in S:
                powers = [zero] * 5
                p = id_R
                powers[0] = p
                for i in range(1, 5):
                    p = mul(p, s)
                    powers[i] = p
                
                found = False
                for d in range(1, 5):
                    for coeffs in itertools.product(R, repeat=d):
                        val = powers[d]
                        for i, c in enumerate(coeffs):
                            term = mul(c, powers[i])
                            val = add(val, term)
                        if val == zero:
                            found = True
                            break
                    if found:
                        break
                if not found:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H_3: P is a prime ideal of R
    try:
        h3 = True
        if not all(contains(R, p) for p in P): h3 = False
        if not contains(P, zero): h3 = False
        if len(P) == len(R): h3 = False
        if h3:
            for a in P:
                for b in P:
                    if not contains(P, add(a, b)): h3 = False
            for p in P:
                for r in R:
                    if not contains(P, mul(p, r)): h3 = False
                    if not contains(P, mul(r, p)): h3 = False
            for a in R:
                for b in R:
                    subset = True
                    for r in R:
                        if not contains(P, mul(a, mul(r, b))):
                            subset = False
                            break
                    if subset:
                        if not contains(P, a) and not contains(P, b):
                            h3 = False
    except Exception:
        h3 = False

    # ¬Q: There does not exist a prime ideal Q of S such that Q \cap R = P
    try:
        neg_q = True
        
        def get_ideal_gen_by(x):
            gen = []
            for s1 in S:
                for s2 in S:
                    val = mul(s1, mul(x, s2))
                    if not contains(gen, val):
                        gen.append(val)
            changed = True
            while changed:
                changed = False
                new_elements = []
                for a in gen:
                    for b in gen:
                        c = add(a, b)
                        if not contains(gen, c) and not contains(new_elements, c):
                            new_elements.append(c)
                if new_elements:
                    gen.extend(new_elements)
                    changed = True
            return tuple(sorted([index_of(S, e) for e in gen]))
            
        principal_ideals = []
        for x in S:
            pi = get_ideal_gen_by(x)
            if pi not in principal_ideals:
                principal_ideals.append(pi)
        
        all_ideals = set()
        for i in range(len(principal_ideals) + 1):
            for combo in itertools.combinations(principal_ideals, i):
                current = [index_of(S, zero)]
                for pi_indices in combo:
                    next_current = []
                    for a_idx in current:
                        for b_idx in pi_indices:
                            c = add(S[a_idx], S[b_idx])
                            c_idx = index_of(S, c)
                            if c_idx not in next_current:
                                next_current.append(c_idx)
                    current = next_current
                all_ideals.add(tuple(sorted(current)))
                
        prime_ideals = []
        for Q_indices in all_ideals:
            if len(Q_indices) == len(S): continue
            Q = [S[i] for i in Q_indices]
            is_prime = True
            for a in S:
                for b in S:
                    subset = True
                    for s in S:
                        if not contains(Q, mul(a, mul(s, b))):
                            subset = False
                            break
                    if subset:
                        if not contains(Q, a) and not contains(Q, b):
                            is_prime = False
                            break
                if not is_prime:
                    break
            if is_prime:
                prime_ideals.append(Q)
                
        P_indices = sorted([index_of(S, p) for p in P])
        for Q in prime_ideals:
            intersect = []
            for q in Q:
                if contains(R, q):
                    intersect.append(index_of(S, q))
            intersect = sorted(intersect)
            if intersect == P_indices:
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a subring of S",
    "H_2: S is an integral extension of R",
    "H_3: P is a prime ideal of R",
    "¬Q: There does not exist a prime ideal Q of S such that Q \\cap R = P"
]

N_HYP = 3
NEG_Q_INDEX = 3