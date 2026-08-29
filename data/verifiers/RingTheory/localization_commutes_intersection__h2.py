import itertools
from sympy import Rational, Integer, Symbol
from sympy.abc import x, y, z

def get_attr(witness, attr):
    if isinstance(witness, dict):
        return witness.get(attr)
    else:
        return getattr(witness, attr, None)

def conditions(witness) -> list[bool]:
    try:
        elements = get_attr(witness, 'elements')
        add = get_attr(witness, 'add')
        mul = get_attr(witness, 'mul')
        zero = get_attr(witness, 'zero')
        one = get_attr(witness, 'one')
        I = get_attr(witness, 'I')
        J = get_attr(witness, 'J')
        S = get_attr(witness, 'S')
        
        if any(v is None for v in [elements, add, mul, zero, one, I, J, S]):
            return [False, False, False]
            
        if not callable(add) or not callable(mul):
            return [False, False, False]
            
        elements = list(elements)
        
        # H_1: R is a commutative ring with identity
        h1 = True
        if zero not in elements or one not in elements:
            h1 = False
        else:
            for a in elements:
                if add(a, zero) != a or add(zero, a) != a:
                    h1 = False; break
                has_inv = False
                for b in elements:
                    if add(a, b) == zero and add(b, a) == zero:
                        has_inv = True; break
                if not has_inv:
                    h1 = False; break
                for b in elements:
                    if add(a, b) not in elements or mul(a, b) not in elements:
                        h1 = False; break
                    if add(a, b) != add(b, a) or mul(a, b) != mul(b, a):
                        h1 = False; break
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)):
                            h1 = False; break
                        if mul(mul(a, b), c) != mul(a, mul(b, c)):
                            h1 = False; break
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)):
                            h1 = False; break
                    if not h1: break
                if not h1: break
            if h1:
                for a in elements:
                    if mul(a, one) != a or mul(one, a) != a:
                        h1 = False; break
                        
        # H_2: I and J are ideals of R
        def check_ideal(K):
            if not K or zero not in K: return False
            for a in K:
                if a not in elements: return False
                has_inv = False
                for b in K:
                    if add(a, b) == zero:
                        has_inv = True; break
                if not has_inv: return False
                for b in K:
                    if add(a, b) not in K: return False
                for r in elements:
                    if mul(r, a) not in K: return False
            return True
            
        h2 = False
        if h1:
            h2 = check_ideal(I) and check_ideal(J)
            
        # ¬Q: S^{-1}(I \cap J) != S^{-1}I \cap S^{-1}J as ideals in S^{-1}R
        # This fails when S is not a multiplicative set, causing the sets of fractions to differ.
        neg_q = False
        if h1 and h2 and S and all(s in elements for s in S):
            neg_map = {}
            for a in elements:
                for b in elements:
                    if add(a, b) == zero:
                        neg_map[a] = b
                        break
                        
            I_cap_J = [a for a in I if a in J]
            
            def get_S_inv(K):
                S_inv = set()
                for r in elements:
                    for t in S:
                        is_in = False
                        for a in K:
                            for s in S:
                                rs = mul(r, s)
                                at = mul(a, t)
                                diff = add(rs, neg_map[at])
                                for u in S:
                                    if mul(u, diff) == zero:
                                        is_in = True
                                        break
                                if is_in: break
                            if is_in: break
                        if is_in:
                            S_inv.add((r, t))
                return S_inv
                
            S_inv_I = get_S_inv(I)
            S_inv_J = get_S_inv(J)
            S_inv_I_cap_J = get_S_inv(I_cap_J)
            
            intersection = S_inv_I.intersection(S_inv_J)
            if S_inv_I_cap_J != intersection:
                neg_q = True
                
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I and J are ideals of R",
    "¬Q: S^{-1}(I \\cap J) != S^{-1}I \\cap S^{-1}J as ideals in S^{-1}R"
]
N_HYP = 2
NEG_Q_INDEX = 2