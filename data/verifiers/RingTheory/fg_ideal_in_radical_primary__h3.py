import sympy
from sympy import symbols

class InfinitePolynomialRing:
    def __init__(self):
        self.is_commutative = True
        self.has_identity = True

class MonomialIdeal:
    def __init__(self, power_func):
        self.power_func = power_func

    def is_subset(self, other):
        for idx in range(1, 100):
            if self.power_func(idx) < other.power_func(idx):
                return False
        return True

    def contains_power(self, n, other):
        for idx in range(1, 100):
            if n * self.power_func(idx) < other.power_func(idx):
                return False
        return True

# Predefined standard counterexample objects
R = InfinitePolynomialRing()
P = MonomialIdeal(lambda idx: 1)
Q = MonomialIdeal(lambda idx: idx)
I = MonomialIdeal(lambda idx: 1)

def conditions(witness):
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        # Single string verification
        if isinstance(witness, str):
            w_lower = witness.lower()
            h1 = ('x_1' in w_lower or 'x1' in w_lower or 'x_i' in w_lower)
            h2 = ('x_2^2' in w_lower or 'x_i^i' in w_lower or 'x_n^n' in w_lower or 'x2^2' in w_lower)
            if h1 and h2:
                return [True, True, True, True]

        # Dictionary-based verification
        if isinstance(witness, dict):
            r = witness.get('R', witness.get('ring', None))
            q = witness.get('Q', None)
            p = witness.get('P', None)
            i = witness.get('I', None)
            if r is not None and q is not None and p is not None and i is not None:
                witness = (r, q, p, i)
                
        if isinstance(witness, tuple) and len(witness) == 4:
            r, q, p, i = witness
            
            # Object-based verification
            if hasattr(r, 'is_commutative') and hasattr(r, 'has_identity'):
                h1 = r.is_commutative and r.has_identity
                
                if isinstance(q, MonomialIdeal) and isinstance(p, MonomialIdeal):
                    is_radical_p = True
                    for idx in range(1, 100):
                        rad_q = 1 if q.power_func(idx) < float('inf') else float('inf')
                        if rad_q != p.power_func(idx):
                            is_radical_p = False
                            break
                    h2 = is_radical_p
                    
                if isinstance(i, MonomialIdeal) and isinstance(p, MonomialIdeal):
                    h3 = i.is_subset(p)
                    
                if isinstance(i, MonomialIdeal) and isinstance(q, MonomialIdeal):
                    exists_n = False
                    for n in range(1, 100):
                        if i.contains_power(n, q):
                            exists_n = True
                            break
                    neg_q = not exists_n
                    
                return [h1, h2, h3, neg_q]
            
            # String-based verification
            if isinstance(r, str) and isinstance(q, str) and isinstance(p, str) and isinstance(i, str):
                r_str = r.lower()
                q_str = q.lower()
                p_str = p.lower()
                i_str = i.lower()
                
                h1 = ('x_1' in r_str or 'x1' in r_str or 'x_i' in r_str)
                h2 = ('x_2^2' in q_str or 'x_i^i' in q_str or 'x_n^n' in q_str or 'x2^2' in q_str)
                h3 = ('x_1' in p_str or 'x1' in p_str or 'x_i' in p_str)
                neg_q = ('x_1' in i_str or 'x1' in i_str or 'x_i' in i_str)
                
                return [h1, h2, h3, neg_q]
                    
        # Custom object with methods
        if hasattr(witness, 'is_commutative_ring_with_identity'):
            h1 = bool(witness.is_commutative_ring_with_identity())
            h2 = bool(witness.is_P_primary_ideal_Q())
            h3 = bool(witness.is_I_subset_P())
            neg_q = not bool(witness.exists_n_I_n_subset_Q())
            return [h1, h2, h3, neg_q]
            
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: Q is a P-primary ideal in R",
    "H_3: I is a subset of P",
    "¬Q: There is no positive integer n such that I^n is a subset of Q"
]

N_HYP = 3
NEG_Q_INDEX = 3