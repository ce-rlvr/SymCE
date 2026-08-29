import sympy
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for RingTheory
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f is a surjective ring homomorphism",
    "H_2: M is a maximal ideal of S",
    "¬Q: The preimage f^{-1}(M) is not a maximal ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to provide finite rings R and S, their operations,
    the function f, and the ideal M.
    """
    try:
        R = witness.R
        S = witness.S
        add_R = witness.add_R
        mul_R = witness.mul_R
        add_S = witness.add_S
        mul_S = witness.mul_S
        f = witness.f
        M = witness.M
    except AttributeError:
        try:
            R = witness['R']
            S = witness['S']
            add_R = witness['add_R']
            mul_R = witness['mul_R']
            add_S = witness['add_S']
            mul_S = witness['mul_S']
            f = witness['f']
            M = witness['M']
        except Exception:
            return [False, False, False]

    def get_zero(elements, add):
        for e in elements:
            if all(add(e, a) == a for a in elements) and all(add(a, e) == a for a in elements):
                return e
        return None

    def get_inverses(elements, add, zero):
        inv = {}
        for a in elements:
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    inv[a] = b
                    break
        return inv

    def is_ring(elements, add, mul, zero, inv):
        if len(inv) != len(elements): 
            return False
        for a in elements:
            for b in elements:
                if add(a, b) != add(b, a): 
                    return False
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): 
                        return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): 
                        return False
        for a in elements:
            for b in elements:
                for c in elements:
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): 
                        return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): 
                        return False
        return True

    def is_ideal(elements, add, mul, zero, inv, I):
        if not I: 
            return False
        I_set = set(I)
        if zero not in I_set: 
            return False
        for a in I_set:
            for b in I_set:
                if add(a, inv[b]) not in I_set: 
                    return False
        for r in elements:
            for x in I_set:
                if mul(r, x) not in I_set: 
                    return False
                if mul(x, r) not in I_set: 
                    return False
        return True

    def is_maximal_ideal(elements, add, mul, zero, inv, I):
        if not is_ideal(elements, add, mul, zero, inv, I): 
            return False
        if set(I) == set(elements): 
            return False
        
        for r in elements:
            if r in I: 
                continue
            gen = set(I)
            gen.add(r)
            while True:
                size_before = len(gen)
                new_elements = set()
                for a in gen:
                    for b in gen:
                        new_elements.add(add(a, b))
                        new_elements.add(add(a, inv[b]))
                for x in elements:
                    for a in gen:
                        new_elements.add(mul(x, a))
                        new_elements.add(mul(a, x))
                gen.update(new_elements)
                if len(gen) == size_before:
                    break
            if set(gen) != set(elements):
                return False
        return True

    h1 = False
    h2 = False
    neg_q = False

    try:
        zero_R = get_zero(R, add_R)
        zero_S = get_zero(S, add_S)
        
        if zero_R is not None and zero_S is not None:
            inv_R = get_inverses(R, add_R, zero_R)
            inv_S = get_inverses(S, add_S, zero_S)
            
            if is_ring(R, add_R, mul_R, zero_R, inv_R) and is_ring(S, add_S, mul_S, zero_S, inv_S):
                
                # Check H1: f is a surjective ring homomorphism
                is_hom = True
                for a in R:
                    for b in R:
                        if f(add_R(a, b)) != add_S(f(a), f(b)):
                            is_hom = False
                            break
                        if f(mul_R(a, b)) != mul_S(f(a), f(b)):
                            is_hom = False
                            break
                    if not is_hom: 
                        break
                
                if is_hom:
                    image = set(f(a) for a in R)
                    if image == set(S):
                        h1 = True

                # Check H2: M is a maximal ideal of S
                if is_maximal_ideal(S, add_S, mul_S, zero_S, inv_S, M):
                    h2 = True

                # Check neg_Q: f^{-1}(M) is NOT a maximal ideal of R
                preimage = [a for a in R if f(a) in M]
                q = is_maximal_ideal(R, add_R, mul_R, zero_R, inv_R, preimage)
                neg_q = not q

    except Exception:
        pass

    return [h1, h2, neg_q]