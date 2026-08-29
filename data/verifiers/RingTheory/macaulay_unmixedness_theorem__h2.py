import sympy
import itertools
from sympy import symbols

# Top-level setup
a, b, c, d, x, y, z, w = symbols('a b c d x y z w')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (gens, k) or (R, gens, k) where gens is a list 
    of monomial generators for the ideal I, and k is the integer height.
    Alternatively, it can be a dictionary with keys 'ideal' and 'k'.
    """
    try:
        # Parse witness
        if isinstance(witness, dict):
            gens = witness.get('ideal', [])
            k = witness.get('k', None)
            is_cm = witness.get('is_cm', True)
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 2:
                gens, k = witness
                is_cm = True
            elif len(witness) == 3:
                _, gens, k = witness
                is_cm = True
            else:
                return [False, False]
        else:
            return [False, False]
            
        if k is None:
            return [False, False]
            
        if not isinstance(k, int) and not (hasattr(k, 'is_Integer') and k.is_Integer):
            return [False, False]
        k = int(k)
        
        # H1: R is a Cohen-Macaulay ring
        # Polynomial rings over fields are Cohen-Macaulay.
        h1_ok = bool(is_cm)
        
        # Parse generators into dictionaries of variable powers
        gens = list(gens)
        gens_dicts = []
        for g in gens:
            if g == 0:
                continue
            if g == 1:
                gens_dicts.append({})
                continue
            
            g = sympy.expand(g)
            if isinstance(g, sympy.Add):
                # We restrict to monomial ideals for this verifier
                return [False, False]
                
            d_powers = g.as_powers_dict()
            clean_d = {}
            for base, exp in d_powers.items():
                if not base.is_number:
                    if not base.is_Symbol:
                        return [False, False]
                    if not exp.is_Integer or exp <= 0:
                        return [False, False]
                    clean_d[base] = int(exp)
            gens_dicts.append(clean_d)
            
        # Helper functions for primary decomposition of monomial ideals
        def is_divisible(m1, m2):
            for v, e in m2.items():
                if m1.get(v, 0) < e:
                    return False
            return True

        def minimize_generators(g_list):
            res = []
            for i, g1 in enumerate(g_list):
                is_multiple = False
                for j, g2 in enumerate(g_list):
                    if i != j:
                        if is_divisible(g1, g2):
                            if g1 == g2:
                                if i > j:
                                    is_multiple = True
                                    break
                            else:
                                is_multiple = True
                                break
                if not is_multiple:
                    res.append(g1)
            return res

        def split_ideal(g_list):
            g_list = minimize_generators(g_list)
            for i, g in enumerate(g_list):
                if len(g) > 1:
                    var = list(g.keys())[0]
                    exp = g[var]
                    
                    g1 = {var: exp}
                    gens1 = g_list[:i] + [g1] + g_list[i+1:]
                    
                    g2 = dict(g)
                    del g2[var]
                    gens2 = g_list[:i] + [g2] + g_list[i+1:]
                    
                    return split_ideal(gens1) + split_ideal(gens2)
            return [g_list]

        def intersect_components(comps):
            if not comps:
                return []
            intersected = []
            for combo in itertools.product(*comps):
                lcm_gen = {}
                for g in combo:
                    for v, e in g.items():
                        lcm_gen[v] = max(lcm_gen.get(v, 0), e)
                intersected.append(lcm_gen)
            return minimize_generators(intersected)

        def get_irredundant_components(comps):
            n = len(comps)
            active = [True] * n
            target = intersect_components(comps)
            
            def sort_key(g):
                return str(sorted([(str(k_var), v) for k_var, v in g.items()]))
                
            target_sorted = sorted(target, key=sort_key)
            
            for i in range(n):
                active[i] = False
                current_comps = [comps[j] for j in range(n) if active[j]]
                if not current_comps:
                    active[i] = True
                    continue
                current_intersection = intersect_components(current_comps)
                if sorted(current_intersection, key=sort_key) != target_sorted:
                    active[i] = True
            return [comps[i] for i in range(n) if active[i]]

        # Compute associated primes
        if any(not g for g in gens_dicts):
            # Ideal is the whole ring (1), which has no associated primes
            primes = []
        else:
            comps = split_ideal(gens_dicts)
            irr_comps = get_irredundant_components(comps)
            
            primes = []
            for comp in irr_comps:
                prime = set()
                for g in comp:
                    prime.update(g.keys())
                if prime not in primes:
                    primes.append(prime)
                    
        # Check conclusion: Every associated prime has height exactly k, and no embedded primes
        # For monomial ideals, the height of a prime generated by variables is the number of variables
        all_height_k = all(len(p) == k for p in primes)
        
        has_embedded = False
        for p1 in primes:
            for p2 in primes:
                if p1 != p2 and p2.issubset(p1):
                    has_embedded = True
                    break
            if has_embedded:
                break
                
        conclusion = all_height_k and not has_embedded
        neg_q = not conclusion
        
        return [h1_ok, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a Cohen-Macaulay ring",
    "¬Q: Not every associated prime of I has height exactly k, or I has embedded primes"
]
N_HYP = 1
NEG_Q_INDEX = 1