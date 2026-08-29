import sympy
from sympy import eye, zeros
import itertools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    Expected witness format:
    A dictionary or a tuple (n, M_prime, M, M_double_prime, f, g) where:
    - n: integer, the modulus of the ring R = Z/nZ
    - M_prime, M, M_double_prime: lists of integers representing the invariant factors of the modules
    - f: matrix (list of lists) or callable representing the map M' -> M
    - g: matrix (list of lists) or callable representing the map M -> M''
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            M_prime = witness.get('M_prime')
            M = witness.get('M')
            M_double_prime = witness.get('M_double_prime')
            f = witness.get('f')
            g = witness.get('g')
        else:
            n, M_prime, M, M_double_prime, f, g = witness
            
        if not isinstance(n, int) or n < 1:
            return [False, False, False]
            
        for mod in [M_prime, M, M_double_prime]:
            if not isinstance(mod, list) or not all(isinstance(x, int) for x in mod):
                return [False, False, False]
                
        is_r_module = True
        for mod in [M_prime, M, M_double_prime]:
            for d in mod:
                if d <= 0 or n % d != 0:
                    is_r_module = False
                    break
            if not is_r_module:
                break
                
        size_M_prime = 1
        for d in M_prime: size_M_prime *= d
        size_M = 1
        for d in M: size_M *= d
        size_M_double = 1
        for d in M_double_prime: size_M_double *= d
        
        if size_M_prime > 100000 or size_M > 100000 or size_M_double > 100000:
            return [False, False, False]
            
        if hasattr(f, 'tolist'):
            f = f.tolist()
        if hasattr(g, 'tolist'):
            g = g.tolist()
            
        def get_elements(D):
            if not D: return [()]
            return list(itertools.product(*[range(d) for d in D]))
            
        def eval_map(map_obj, x, codomain_D):
            if callable(map_obj):
                y = map_obj(x)
                if not codomain_D: return ()
                return tuple(int(y[i]) % codomain_D[i] for i in range(len(codomain_D)))
            else:
                if not codomain_D: return ()
                y = []
                for i in range(len(codomain_D)):
                    val = sum(int(map_obj[i][j]) * int(x[j]) for j in range(len(x)))
                    y.append(val % codomain_D[i])
                return tuple(y)
                
        elements_M_prime = get_elements(M_prime)
        elements_M = get_elements(M)
        elements_M_double_prime = get_elements(M_double_prime)
        
        exact = True
        # Check homomorphism property for f
        for x in elements_M_prime:
            for y in elements_M_prime:
                xy = tuple((x[i] + y[i]) % M_prime[i] for i in range(len(M_prime)))
                fx = eval_map(f, x, M)
                fy = eval_map(f, y, M)
                fxy = eval_map(f, xy, M)
                fx_plus_fy = tuple((fx[i] + fy[i]) % M[i] for i in range(len(M)))
                if fxy != fx_plus_fy:
                    exact = False
                    break
            if not exact: break
            
        if exact:
            # Check homomorphism property for g
            for x in elements_M:
                for y in elements_M:
                    xy = tuple((x[i] + y[i]) % M[i] for i in range(len(M)))
                    gx = eval_map(g, x, M_double_prime)
                    gy = eval_map(g, y, M_double_prime)
                    gxy = eval_map(g, xy, M_double_prime)
                    gx_plus_gy = tuple((gx[i] + gy[i]) % M_double_prime[i] for i in range(len(M_double_prime)))
                    if gxy != gx_plus_gy:
                        exact = False
                        break
                if not exact: break
                
        if exact:
            im_f = set()
            for x in elements_M_prime:
                im_f.add(eval_map(f, x, M))
                
            if len(im_f) != len(elements_M_prime):
                exact = False
            else:
                ker_g = set()
                im_g = set()
                for y in elements_M:
                    gy = eval_map(g, y, M_double_prime)
                    im_g.add(gy)
                    if all(v == 0 for v in gy):
                        ker_g.add(y)
                        
                if im_f != ker_g:
                    exact = False
                elif len(im_g) != len(elements_M_double_prime):
                    exact = False
                    
        def get_invariant_factors(D):
            if not D:
                return []
            prime_powers = {}
            for d in D:
                if d <= 1:
                    continue
                factors = sympy.factorint(d)
                for p, e in factors.items():
                    if p not in prime_powers:
                        prime_powers[p] = []
                    prime_powers[p].append(e)
                    
            if not prime_powers:
                return []
                
            max_len = max(len(powers) for powers in prime_powers.values())
            for p in prime_powers:
                while len(prime_powers[p]) < max_len:
                    prime_powers[p].append(0)
                prime_powers[p].sort()
                
            inv_factors = []
            for i in range(max_len):
                inv_factor = 1
                for p in prime_powers:
                    e = prime_powers[p][i]
                    if e > 0:
                        inv_factor *= (p ** e)
                if inv_factor > 1:
                    inv_factors.append(inv_factor)
                    
            return inv_factors
            
        rank_M = get_invariant_factors(M).count(n)
        rank_M_prime = get_invariant_factors(M_prime).count(n)
        rank_M_double_prime = get_invariant_factors(M_double_prime).count(n)
        
        h1 = exact and is_r_module
        h2 = is_r_module
        neg_q = (rank_M != rank_M_prime + rank_M_double_prime)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: 0 -> M' -> M -> M'' -> 0 is a short exact sequence of R-modules",
    "H_2: M, M', and M'' are finitely generated R-modules",
    "¬Q: The rank of M does not equal the rank of M' plus the rank of M''"
]

N_HYP = 2
NEG_Q_INDEX = 2