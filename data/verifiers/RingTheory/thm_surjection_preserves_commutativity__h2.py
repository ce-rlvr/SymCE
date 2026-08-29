import sympy
from sympy.matrices import eye, zeros
import itertools
import functools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is surjective",
    "H_3: R is a commutative ring",
    "¬Q: S is not commutative"
]

N_HYP = 3
NEG_Q_INDEX = 3

def evaluate_op(op, a, b):
    if isinstance(op, dict):
        return op[(a, b)]
    elif isinstance(op, list):
        for k, v in op:
            if k == (a, b):
                return v
        raise KeyError((a, b))
    else:
        return op(a, b)

def evaluate_f(f, a):
    if isinstance(f, dict):
        return f[a]
    elif isinstance(f, list):
        for k, v in f:
            if k == a:
                return v
        raise KeyError(a)
    else:
        return f(a)

def is_ring(elements, add, mul):
    elements = list(elements)
    if not elements: 
        return False
    if len(elements) > 50: 
        return False  # Prevent timeout for infinite or excessively large rings
    
    # Add closure
    for a in elements:
        for b in elements:
            if evaluate_op(add, a, b) not in elements: 
                return False
            
    # Add commutativity
    for a in elements:
        for b in elements:
            if evaluate_op(add, a, b) != evaluate_op(add, b, a): 
                return False
            
    # Add associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if evaluate_op(add, evaluate_op(add, a, b), c) != evaluate_op(add, a, evaluate_op(add, b, c)): 
                    return False
                
    # Add identity
    zero = None
    for e in elements:
        if all(evaluate_op(add, e, a) == a for a in elements):
            zero = e
            break
    if zero is None: 
        return False
    
    # Add inverse
    for a in elements:
        if not any(evaluate_op(add, a, b) == zero for b in elements): 
            return False
        
    # Mul closure
    for a in elements:
        for b in elements:
            if evaluate_op(mul, a, b) not in elements: 
                return False
            
    # Mul associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if evaluate_op(mul, evaluate_op(mul, a, b), c) != evaluate_op(mul, a, evaluate_op(mul, b, c)): 
                    return False
                
    # Distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                left1 = evaluate_op(mul, a, evaluate_op(add, b, c))
                right1 = evaluate_op(add, evaluate_op(mul, a, b), evaluate_op(mul, a, c))
                if left1 != right1: 
                    return False
                
                left2 = evaluate_op(mul, evaluate_op(add, a, b), c)
                right2 = evaluate_op(add, evaluate_op(mul, a, c), evaluate_op(mul, b, c))
                if left2 != right2: 
                    return False
                
    return True

def normalize_witness(witness):
    if isinstance(witness, dict):
        if 'R_set' in witness:
            return (
                list(witness['R_set']), witness['R_add'], witness['R_mul'],
                list(witness['S_set']), witness['S_add'], witness['S_mul'],
                witness['f']
            )
        elif 'R' in witness and 'S' in witness and 'f' in witness:
            R = witness['R']
            S = witness['S']
            f = witness['f']
            if isinstance(R, dict):
                return (
                    list(R['set']), R['add'], R['mul'],
                    list(S['set']), S['add'], S['mul'],
                    f
                )
            else:
                return (
                    list(R.elements), R.add, R.mul,
                    list(S.elements), S.add, S.mul,
                    f
                )
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 7:
            return (
                list(witness[0]), witness[1], witness[2],
                list(witness[3]), witness[4], witness[5],
                witness[6]
            )
        elif len(witness) == 3:
            R, S, f = witness
            if isinstance(R, dict):
                return (
                    list(R['set']), R['add'], R['mul'],
                    list(S['set']), S['add'], S['mul'],
                    f
                )
            else:
                return (
                    list(R.elements), R.add, R.mul,
                    list(S.elements), S.add, S.mul,
                    f
                )
    elif hasattr(witness, 'R_set') and hasattr(witness, 'S_set'):
        return (
            list(witness.R_set), witness.R_add, witness.R_mul,
            list(witness.S_set), witness.S_add, witness.S_mul,
            witness.f
        )
    elif hasattr(witness, 'R') and hasattr(witness, 'S') and hasattr(witness, 'f'):
        R = witness.R
        S = witness.S
        return (
            list(R.elements), R.add, R.mul,
            list(S.elements), S.add, S.mul,
            witness.f
        )
    raise ValueError("Unrecognized witness format")

def conditions(witness) -> list[bool]:
    try:
        R_set, R_add, R_mul, S_set, S_add, S_mul, f = normalize_witness(witness)
    except Exception:
        return [False, False, False, False]

    # H1: R and S are rings
    try:
        h1_ok = is_ring(R_set, R_add, R_mul) and is_ring(S_set, S_add, S_mul)
    except Exception:
        h1_ok = False

    # H2: f is surjective
    try:
        image = []
        for r in R_set:
            val = evaluate_f(f, r)
            if val not in S_set:
                h2_ok = False
                break
            if val not in image:
                image.append(val)
        else:
            h2_ok = True
            for s in S_set:
                if s not in image:
                    h2_ok = False
                    break
    except Exception:
        h2_ok = False

    # H3: R is a commutative ring
    try:
        h3_ok = True
        for a in R_set:
            for b in R_set:
                if evaluate_op(R_mul, a, b) != evaluate_op(R_mul, b, a):
                    h3_ok = False
                    break
            if not h3_ok:
                break
    except Exception:
        h3_ok = False

    # neg_Q: S is not commutative
    try:
        neg_q_ok = False
        for a in S_set:
            for b in S_set:
                if evaluate_op(S_mul, a, b) != evaluate_op(S_mul, b, a):
                    neg_q_ok = True
                    break
            if neg_q_ok:
                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]