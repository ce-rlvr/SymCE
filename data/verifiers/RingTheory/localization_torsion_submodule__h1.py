import sympy
from sympy import symbols

# Top-level setup
x, y, z = symbols('x y z')

class MonomialIdeal:
    def __init__(self, gens):
        self.gens = self._minimize(gens)
        
    def _minimize(self, gens):
        res = []
        for g in gens:
            if not any(all(a >= b for a, b in zip(g, h)) for h in res):
                res = [h for h in res if not all(a >= b for a, b in zip(h, g))]
                res.append(g)
        return res
        
    def contains(self, mono):
        return any(all(a >= b for a, b in zip(mono, g)) for g in self.gens)
        
    def quotient_mono(self, mono):
        new_gens = []
        for g in self.gens:
            new_gen = tuple(max(0, b - a) for a, b in zip(mono, g))
            new_gens.append(new_gen)
        return MonomialIdeal(new_gens)
        
    def saturate(self, mono):
        new_gens = []
        for g in self.gens:
            new_gen = tuple(0 if m > 0 else a for a, m in zip(g, mono))
            new_gens.append(new_gen)
        return MonomialIdeal(new_gens)
        
    def __eq__(self, other):
        return set(self.gens) == set(other.gens)

def minimal_primes(ideal_gens, n_vars):
    def get_min_primes(gens):
        if not gens:
            return [set()]
        g = gens[0]
        vars_in_g = [i for i, e in enumerate(g) if e > 0]
        if not vars_in_g:
            return [{i for i in range(n_vars)}]
            
        primes = []
        for v in vars_in_g:
            remaining_gens = [h for h in gens if h[v] == 0]
            for p in get_min_primes(remaining_gens):
                p_new = set(p)
                p_new.add(v)
                primes.append(p_new)
                
        min_primes = []
        for p in primes:
            if not any(q < p for q in primes):
                if p not in min_primes:
                    min_primes.append(p)
        return min_primes

    return get_min_primes(ideal_gens)

def is_contained_in_prime(J_gens, P):
    if not J_gens:
        return True
    for g in J_gens:
        if not any(g[v] > 0 for v in P):
            return False
    return True

def contains_regular_element(J_gens, min_primes):
    for P in min_primes:
        if is_contained_in_prime(J_gens, P):
            return False
    return True

def add_monos(m1, m2):
    return tuple(a + b for a, b in zip(m1, m2))

def is_square_free(gens):
    for g in gens:
        if any(e > 1 for e in g):
            return False
    return True

def conditions(witness) -> list[bool]:
    """
    The witness is expected to be a dictionary representing a counterexample
    using monomial ideals in a polynomial ring k[x_1, ..., x_n].
    Format:
    {
        'n_vars': int,
        'R_ideal': list[tuple[int, ...]],  # generators of the ideal defining R
        'S_gen': tuple[int, ...],          # monomial generating the multiplicatively closed set S
        'M_ideal': list[tuple[int, ...]],  # generators of the ideal defining M = R / M_ideal
        'm': tuple[int, ...],              # witness element m in M
        'z': tuple[int, ...]               # witness element z in R
    }
    """
    try:
        n_vars = witness['n_vars']
        R_ideal_gens = witness['R_ideal']
        S_gen = witness['S_gen']
        M_ideal_gens = witness['M_ideal']
        m = witness['m']
        z_elem = witness['z']
        
        R_ideal = MonomialIdeal(R_ideal_gens)
        M_ideal = MonomialIdeal(M_ideal_gens)
        
        # H1: M is an R-module
        # By definition of M = R / M_ideal, it is naturally an R-module.
        H1 = True
        
        # H2: S is a multiplicatively closed subset of R
        # By definition of S = {S_gen^k | k >= 0}, it is multiplicatively closed.
        H2 = True
        
        # H3: 0 is not an element of S
        # This means S_gen^k is not in R_ideal for any k.
        H3 = True
        for g in R_ideal.gens:
            if all(S_gen[i] > 0 for i in range(n_vars) if g[i] > 0):
                H3 = False
                break
                
        # neg_Q: T(S^{-1} M) is not isomorphic to S^{-1} T(M)
        # We verify this by checking if m/1 is in T(S^{-1} M) but not in S^{-1} T(M).
        # For our algebraic checker to be sound, R_ideal must be square-free.
        if not is_square_free(R_ideal.gens):
            return [H1, H2, H3, False]
            
        # 1. z_elem is regular in S^{-1} R
        R_sat = R_ideal.saturate(S_gen)
        R_sat_z = R_sat.quotient_mono(z_elem)
        z_is_regular = (R_sat == R_sat_z)
        
        # 2. z_elem * m = 0 in S^{-1} M
        zm = add_monos(z_elem, m)
        M_sat = M_ideal.saturate(S_gen)
        zm_is_zero = M_sat.contains(zm)
        
        # 3. m != 0 in S^{-1} M
        m_is_not_zero = not M_sat.contains(m)
        
        # 4. m is not in S^{-1} T(M)
        J = M_sat.quotient_mono(m)
        min_primes = minimal_primes(R_ideal.gens, n_vars)
        m_not_in_S_inv_T = not contains_regular_element(J.gens, min_primes)
        
        neg_Q = bool(z_is_regular and zm_is_zero and m_is_not_zero and m_not_in_S_inv_T)
        
        return [H1, H2, H3, neg_Q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: M is an R-module",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: 0 is not an element of S",
    "¬Q: T(S^{-1} M) is not isomorphic to S^{-1} T(M)"
]

N_HYP = 3
NEG_Q_INDEX = 3