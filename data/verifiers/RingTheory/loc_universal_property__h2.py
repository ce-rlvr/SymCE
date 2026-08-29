import itertools
import sympy
from sympy import Rational, Integer

# Top-level setup
# The witness is expected to provide its own finite rings as objects with attributes:
# elements (list), add (dict or func), mul (dict or func), zero, one.
# No specific named objects are required for this abstract ring theory conjecture.

CONDITION_LABELS = [
    "H_1: R and T are commutative rings with identity",
    "H_2: f: R \\to T is a ring homomorphism",
    "H_3: f(s) is a unit in T for all s \\in S",
    "H_4: \\phi: R \\to S^{-1}R is the canonical localization map",
    "¬Q: There does not exist a unique ring homomorphism g: S^{-1}R \\to T such that f = g \\circ \\phi"
]

N_HYP = 4
NEG_Q_INDEX = 4

def apply_map(m, x):
    if isinstance(m, dict):
        return m[x]
    return m(x)

def apply_op(op, a, b):
    if isinstance(op, dict):
        return op[(a, b)]
    return op(a, b)

def is_comm_ring_with_id(R):
    try:
        elems = R.elements
        z = R.zero
        o = R.one
        if z not in elems or o not in elems: 
            return False
        for a in elems:
            if apply_op(R.add, a, z) != a or apply_op(R.add, z, a) != a: 
                return False
            if apply_op(R.mul, a, o) != a or apply_op(R.mul, o, a) != a: 
                return False
            has_inv = any(apply_op(R.add, a, b) == z and apply_op(R.add, b, a) == z for b in elems)
            if not has_inv: 
                return False
        for a in elems:
            for b in elems:
                if apply_op(R.add, a, b) != apply_op(R.add, b, a): 
                    return False
                if apply_op(R.mul, a, b) != apply_op(R.mul, b, a): 
                    return False
                if apply_op(R.add, a, b) not in elems: 
                    return False
                if apply_op(R.mul, a, b) not in elems: 
                    return False
                for c in elems:
                    if apply_op(R.add, apply_op(R.add, a, b), c) != apply_op(R.add, a, apply_op(R.add, b, c)): 
                        return False
                    if apply_op(R.mul, apply_op(R.mul, a, b), c) != apply_op(R.mul, a, apply_op(R.mul, b, c)): 
                        return False
                    if apply_op(R.mul, a, apply_op(R.add, b, c)) != apply_op(R.add, apply_op(R.mul, a, b), apply_op(R.mul, a, c)): 
                        return False
        return True
    except Exception:
        return False

def is_ring_hom(f, R, T):
    try:
        if apply_map(f, R.one) != T.one: 
            return False
        for a in R.elements:
            for b in R.elements:
                if apply_map(f, apply_op(R.add, a, b)) != apply_op(T.add, apply_map(f, a), apply_map(f, b)): 
                    return False
                if apply_map(f, apply_op(R.mul, a, b)) != apply_op(T.mul, apply_map(f, a), apply_map(f, b)): 
                    return False
        return True
    except Exception:
        return False

def is_unit(x, T):
    try:
        return any(apply_op(T.mul, x, y) == T.one and apply_op(T.mul, y, x) == T.one for y in T.elements)
    except Exception:
        return False

def conditions(witness):
    # H_1: R and T are commutative rings with identity
    try:
        h1 = is_comm_ring_with_id(witness.R) and is_comm_ring_with_id(witness.T)
    except Exception:
        h1 = False

    # H_2: f: R \to T is a ring homomorphism
    try:
        h2 = is_ring_hom(witness.f, witness.R, witness.T)
    except Exception:
        h2 = False

    # H_3: f(s) is a unit in T for all s \in S
    try:
        h3 = all(is_unit(apply_map(witness.f, s), witness.T) for s in witness.S)
    except Exception:
        h3 = False

    # H_4: \phi: R \to S^{-1}R is the canonical localization map
    try:
        h4 = True
        for a in witness.R.elements:
            if apply_map(witness.phi, a) not in witness.S_inv_R.elements: 
                h4 = False
                break
        
        # If S_inv_R is a ring, check if it satisfies the structural properties of canonical localization
        if h4 and is_comm_ring_with_id(witness.S_inv_R):
            if not is_ring_hom(witness.phi, witness.R, witness.S_inv_R): 
                h4 = False
            else:
                for s in witness.S:
                    if not is_unit(apply_map(witness.phi, s), witness.S_inv_R): 
                        h4 = False
                        break
                if h4:
                    for x in witness.S_inv_R.elements:
                        is_frac = False
                        for r in witness.R.elements:
                            for s in witness.S:
                                phi_s = apply_map(witness.phi, s)
                                for y in witness.S_inv_R.elements:
                                    if apply_op(witness.S_inv_R.mul, phi_s, y) == witness.S_inv_R.one:
                                        if apply_op(witness.S_inv_R.mul, apply_map(witness.phi, r), y) == x:
                                            is_frac = True
                                            break
                                if is_frac: break
                            if is_frac: break
                        if not is_frac: 
                            h4 = False
                            break
    except Exception:
        h4 = False

    # neg_Q: There does not exist a unique ring homomorphism g: S^{-1}R \to T such that f = g \circ \phi
    try:
        valid_g_count = 0
        S_elems = witness.S_inv_R.elements
        T_elems = witness.T.elements
        
        fixed_g = {}
        possible = True
        for r in witness.R.elements:
            pr = apply_map(witness.phi, r)
            fr = apply_map(witness.f, r)
            if pr in fixed_g and fixed_g[pr] != fr:
                possible = False
                break
            fixed_g[pr] = fr
            
        if possible:
            unfixed_elems = [x for x in S_elems if x not in fixed_g]
            for g_vals in itertools.product(T_elems, repeat=len(unfixed_elems)):
                g_map = fixed_g.copy()
                g_map.update(dict(zip(unfixed_elems, g_vals)))
                
                if is_ring_hom(g_map, witness.S_inv_R, witness.T):
                    valid_g_count += 1
                    if valid_g_count > 1:
                        break
        neg_q = (valid_g_count != 1)
    except Exception:
        # If S_inv_R is not a ring, is_ring_hom will fail, meaning no such ring hom exists.
        neg_q = True

    return [h1, h2, h3, h4, neg_q]