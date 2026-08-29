import itertools
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness must be an object with the following attributes:
      - elements: list of ring elements
      - zero: the additive identity
      - add: callable add(a, b) returning the sum
      - mul: callable mul(a, b) returning the product
      - components: list of lists, where each inner list is a homogeneous component H_g
      - ideal: list of elements in the ideal P
    """
    try:
        elements = witness.elements
        zero = witness.zero
        add = witness.add
        mul = witness.mul
        components = witness.components
        ideal = witness.ideal
    except Exception:
        return [False, False]

    def check_h1():
        if not isinstance(elements, list) or zero not in elements: 
            return False
        if not callable(add) or not callable(mul): 
            return False

        # 1. Ring axioms (commutative ring)
        for a in elements:
            if add(a, zero) != a: return False
            if add(zero, a) != a: return False
            
            has_inv = False
            for b in elements:
                if add(a, b) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
            for b in elements:
                ab = add(a, b)
                if ab not in elements: return False
                if ab != add(b, a): return False
                
                mab = mul(a, b)
                if mab not in elements: return False
                if mab != mul(b, a): return False
                
                for c in elements:
                    if add(ab, c) != add(a, add(b, c)): return False
                    if mul(mab, c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mab, mul(a, c)): return False

        # 2. Grading axioms
        if not isinstance(components, list) or len(components) == 0: 
            return False
            
        for H in components:
            if not isinstance(H, list): return False
            if zero not in H: return False
            for h in H:
                if h not in elements: return False
            for a in H:
                for b in H:
                    if add(a, b) not in H: return False

        # Unique decomposition (R is the direct sum of the components)
        decomps = []
        for combo in itertools.product(*components):
            s = zero
            for h in combo:
                s = add(s, h)
            for existing_s, _ in decomps:
                if existing_s == s:
                    return False
            decomps.append((s, combo))
            
        if len(decomps) != len(elements): return False
        for x in elements:
            found = False
            for s, _ in decomps:
                if s == x:
                    found = True
                    break
            if not found: return False

        # Multiplication respects grading
        for H_i in components:
            for H_j in components:
                valid_k = False
                for H_k in components:
                    subset = True
                    for a in H_i:
                        for b in H_j:
                            if mul(a, b) not in H_k:
                                subset = False
                                break
                        if not subset: break
                    if subset:
                        valid_k = True
                        break
                if not valid_k: return False

        # 3. Ideal axioms
        if not isinstance(ideal, list): return False
        if zero not in ideal: return False
        for x in ideal:
            if x not in elements: return False
        for a in ideal:
            for b in ideal:
                if add(a, b) not in ideal: return False
        for r in elements:
            for x in ideal:
                if mul(r, x) not in ideal: return False

        # 4. Proper ideal
        is_proper = False
        for x in elements:
            if x not in ideal:
                is_proper = True
                break
        if not is_proper: return False

        # 5. Homogeneous ideal
        for x in ideal:
            combo = None
            for s, c in decomps:
                if s == x:
                    combo = c
                    break
            if combo is None: return False
            for h in combo:
                if h not in ideal: return False

        return True

    try:
        h1_ok = check_h1()
    except Exception:
        h1_ok = False

    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            # Check if P is a prime ideal
            is_prime = True
            for a in elements:
                for b in elements:
                    if mul(a, b) in ideal:
                        if a not in ideal and b not in ideal:
                            is_prime = False
                            break
                if not is_prime: break
                
            # Check if the condition holds for all homogeneous elements
            homo_cond = True
            homo_elements = []
            for H in components:
                for h in H:
                    if h not in homo_elements:
                        homo_elements.append(h)
                        
            for a in homo_elements:
                for b in homo_elements:
                    if mul(a, b) in ideal:
                        if a not in ideal and b not in ideal:
                            homo_cond = False
                            break
                if not homo_cond: break
                
            # The conclusion fails if the equivalence is false
            neg_q_ok = (is_prime != homo_cond)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P is a homogeneous proper ideal of R",
    "¬Q: P is prime iff (for all homogeneous a, b, ab in P implies a in P or b in P) is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1