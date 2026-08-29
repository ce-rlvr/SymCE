import sympy
from sympy import symbols, QQ, ZZ
import itertools
import functools
import math

# Top-level setup for RingTheory
x, y, z = symbols('x y z')

def _extract_phi(phi_func, R_elems, S_elems):
    if isinstance(phi_func, dict):
        return [S_elems.index(phi_func[u]) for u in R_elems]
    elif isinstance(phi_func, list):
        if all(isinstance(v, int) and 0 <= v < len(S_elems) for v in phi_func):
            return phi_func
        else:
            return [S_elems.index(v) for v in phi_func]
    else:
        return [S_elems.index(phi_func(u)) for u in R_elems]

def check_ring(size, add, mul):
    if size < 1: 
        return False, None, None, None
        
    # Check bounds and commutativity
    for i in range(size):
        for j in range(size):
            if not (0 <= add[i][j] < size): return False, None, None, None
            if not (0 <= mul[i][j] < size): return False, None, None, None
            if add[i][j] != add[j][i]: return False, None, None, None
            if mul[i][j] != mul[j][i]: return False, None, None, None
            
    # Check associativity and distributivity
    for i in range(size):
        for j in range(size):
            for k in range(size):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False, None, None, None
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False, None, None, None
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False, None, None, None

    # Find additive identity (zero)
    zero = None
    for i in range(size):
        if all(add[i][j] == j for j in range(size)):
            zero = i
            break
    if zero is None: 
        return False, None, None, None
    
    # Check additive inverses
    for i in range(size):
        if not any(add[i][j] == zero for j in range(size)):
            return False, None, None, None
            
    # Find multiplicative identity (one)
    one = None
    for i in range(size):
        if all(mul[i][j] == j for j in range(size)):
            one = i
            break
    if one is None: 
        return False, None, None, None
    
    # Local rings are conventionally non-trivial (1 != 0)
    if one == zero:
        return False, None, None, None
        
    # Find units
    units = set()
    for i in range(size):
        if any(mul[i][j] == one for j in range(size)):
            units.add(i)
            
    non_units = set(range(size)) - units
    
    # A finite commutative ring is local iff its non-units form an ideal.
    # Since it's already closed under multiplication by any element, 
    # we only need to check closure under addition.
    for u in non_units:
        for v in non_units:
            if add[u][v] not in non_units:
                return False, None, None, None
                
    return True, zero, one, units

def conditions(witness):
    try:
        parsed = None
        if isinstance(witness, dict) and 'R_size' in witness:
            parsed = (witness['R_size'], witness['R_add'], witness['R_mul'],
                      witness['S_size'], witness['S_add'], witness['S_mul'],
                      witness['phi'])
        elif isinstance(witness, tuple) and len(witness) == 7:
            parsed = witness
        elif isinstance(witness, dict) and 'R_elements' in witness and 'S_elements' in witness and 'phi' in witness:
            R_elems = list(witness['R_elements'])
            S_elems = list(witness['S_elements'])
            R_add = [[R_elems.index(u + v) for v in R_elems] for u in R_elems]
            R_mul = [[R_elems.index(u * v) for v in R_elems] for u in R_elems]
            S_add = [[S_elems.index(u + v) for v in S_elems] for u in S_elems]
            S_mul = [[S_elems.index(u * v) for v in S_elems] for u in S_elems]
            phi = _extract_phi(witness['phi'], R_elems, S_elems)
            parsed = (len(R_elems), R_add, R_mul, len(S_elems), S_add, S_mul, phi)
        elif hasattr(witness, 'R_elements') and hasattr(witness, 'S_elements') and hasattr(witness, 'phi'):
            R_elems = list(witness.R_elements)
            S_elems = list(witness.S_elements)
            R_add = [[R_elems.index(u + v) for v in R_elems] for u in R_elems]
            R_mul = [[R_elems.index(u * v) for v in R_elems] for u in R_elems]
            S_add = [[S_elems.index(u + v) for v in S_elems] for u in S_elems]
            S_mul = [[S_elems.index(u * v) for v in S_elems] for u in S_elems]
            phi = _extract_phi(witness.phi, R_elems, S_elems)
            parsed = (len(R_elems), R_add, R_mul, len(S_elems), S_add, S_mul, phi)
        elif hasattr(witness, 'R') and hasattr(witness, 'S') and hasattr(witness, 'phi'):
            R = witness.R
            S = witness.S
            R_elems = list(R.elements)
            S_elems = list(S.elements)
            R_add = [[R_elems.index(R.add(u, v)) for v in R_elems] for u in R_elems]
            R_mul = [[R_elems.index(R.mul(u, v)) for v in R_elems] for u in R_elems]
            S_add = [[S_elems.index(S.add(u, v)) for v in S_elems] for u in S_elems]
            S_mul = [[S_elems.index(S.mul(u, v)) for v in S_elems] for u in S_elems]
            phi = _extract_phi(witness.phi, R_elems, S_elems)
            parsed = (len(R_elems), R_add, R_mul, len(S_elems), S_add, S_mul, phi)
        elif isinstance(witness, tuple) and len(witness) == 3:
            R_elems, S_elems, phi_func = witness
            R_elems = list(R_elems)
            S_elems = list(S_elems)
            R_add = [[R_elems.index(u + v) for v in R_elems] for u in R_elems]
            R_mul = [[R_elems.index(u * v) for v in R_elems] for u in R_elems]
            S_add = [[S_elems.index(u + v) for v in S_elems] for u in S_elems]
            S_mul = [[S_elems.index(u * v) for v in S_elems] for u in S_elems]
            phi = _extract_phi(phi_func, R_elems, S_elems)
            parsed = (len(R_elems), R_add, R_mul, len(S_elems), S_add, S_mul, phi)
            
        if parsed is None:
            return [False, False, False]
            
        R_size, R_add, R_mul, S_size, S_add, S_mul, phi = parsed
        
        if callable(phi):
            phi = [phi(i) for i in range(R_size)]
            
    except Exception:
        return [False, False, False]

    # H1: R and S are commutative local rings
    try:
        R_is_local, R_zero, R_one, R_units = check_ring(R_size, R_add, R_mul)
        S_is_local, S_zero, S_one, S_units = check_ring(S_size, S_add, S_mul)
        h1_ok = bool(R_is_local and S_is_local)
    except Exception:
        h1_ok = False

    # H2: \phi: R \to S is a local ring homomorphism
    try:
        h2_ok = False
        if h1_ok:
            is_hom = True
            if len(phi) != R_size:
                is_hom = False
            else:
                for i in range(R_size):
                    if not (0 <= phi[i] < S_size):
                        is_hom = False
                        break
                    for j in range(R_size):
                        if phi[R_add[i][j]] != S_add[phi[i]][phi[j]]:
                            is_hom = False
                            break
                        if phi[R_mul[i][j]] != S_mul[phi[i]][phi[j]]:
                            is_hom = False
                            break
                    if not is_hom:
                        break
                if is_hom and phi[R_one] != S_one:
                    is_hom = False
            
            if is_hom:
                is_local_hom = True
                for i in range(R_size):
                    is_R_unit = i in R_units
                    is_S_unit = phi[i] in S_units
                    # A local homomorphism maps non-units to non-units.
                    # Since it's a homomorphism, units map to units.
                    # Thus, x is a unit iff phi(x) is a unit.
                    if is_R_unit != is_S_unit:
                        is_local_hom = False
                        break
                h2_ok = bool(is_local_hom)
    except Exception:
        h2_ok = False

    # neg_Q: \phi is NOT injective
    try:
        neg_q_ok = False
        if h1_ok and h2_ok:
            images = set()
            injective = True
            for i in range(R_size):
                if phi[i] in images:
                    injective = False
                    break
                images.add(phi[i])
            neg_q_ok = not injective
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R and S are commutative local rings",
    "H_2: \\phi: R \\to S is a local ring homomorphism",
    "¬Q: \\phi is not injective"
]

N_HYP = 2
NEG_Q_INDEX = 2