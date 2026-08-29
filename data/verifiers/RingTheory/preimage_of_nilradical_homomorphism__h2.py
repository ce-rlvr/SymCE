import itertools
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

def extract_witness(witness):
    if isinstance(witness, dict):
        if 'R_elems' in witness:
            return (witness['R_elems'], witness['R_add'], witness['R_mul'],
                    witness['S_elems'], witness['S_add'], witness['S_mul'], witness['f'])
        elif 'R' in witness and 'S' in witness and 'f' in witness:
            R = witness['R']
            S = witness['S']
            if isinstance(R, dict):
                return (R['elems'], R['add'], R['mul'],
                        S['elems'], S['add'], S['mul'], witness['f'])
            else:
                return (R.elems, R.add, R.mul,
                        S.elems, S.add, S.mul, witness['f'])
    elif isinstance(witness, tuple):
        if len(witness) == 7:
            return witness
        elif len(witness) == 3:
            R, S, f = witness
            if isinstance(R, dict):
                return (R['elems'], R['add'], R['mul'],
                        S['elems'], S['add'], S['mul'], f)
            else:
                return (R.elems, R.add, R.mul,
                        S.elems, S.add, S.mul, f)
    
    return (witness.R_elems, witness.R_add, witness.R_mul,
            witness.S_elems, witness.S_add, witness.S_mul, witness.f)

def is_comm_ring_with_id(elems, add, mul):
    try:
        elems = list(elems)
        n = len(elems)
        if n == 0: return False
        
        # Check closure
        for a in elems:
            for b in elems:
                if add(a, b) not in elems: return False
                if mul(a, b) not in elems: return False

        # Find zero
        zero = None
        for e in elems:
            if all(add(e, a) == a and add(a, e) == a for a in elems):
                zero = e
                break
        if zero is None: return False
        
        # Check inverses
        for a in elems:
            if not any(add(a, b) == zero and add(b, a) == zero for b in elems):
                return False
                
        # Find one
        one = None
        for e in elems:
            if all(mul(e, a) == a and mul(a, e) == a for a in elems):
                one = e
                break
        if one is None: return False
        
        # Check commutativity, associativity, distributivity
        for a in elems:
            for b in elems:
                if add(a, b) != add(b, a): return False
                if mul(a, b) != mul(b, a): return False
                for c in elems:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
        return True
    except Exception:
        return False

def get_nilradical(elems, add, mul):
    elems = list(elems)
    zero = None
    for e in elems:
        if all(add(e, a) == a for a in elems):
            zero = e
            break
            
    nilradical = []
    for a in elems:
        curr = a
        is_nil = False
        for _ in range(len(elems)):
            if curr == zero:
                is_nil = True
                break
            curr = mul(curr, a)
        if is_nil:
            nilradical.append(a)
    return nilradical

def conditions(witness) -> list[bool]:
    try:
        R_elems, R_add, R_mul, S_elems, S_add, S_mul, f = extract_witness(witness)
        h1 = is_comm_ring_with_id(R_elems, R_add, R_mul) and is_comm_ring_with_id(S_elems, S_add, S_mul)
        
        if h1:
            if isinstance(f, dict):
                f_eval = lambda x: f[x]
            elif isinstance(f, (list, tuple)):
                def f_eval(x):
                    for k, v in f:
                        if k == x: return v
                    raise ValueError("Not found")
            else:
                f_eval = f
                
            # Check that f is a well-defined function from R to S
            for a in R_elems:
                if f_eval(a) not in S_elems:
                    h1 = False
                    break
    except Exception:
        h1 = False
        
    try:
        R_elems, R_add, R_mul, S_elems, S_add, S_mul, f = extract_witness(witness)
        nil_R = get_nilradical(R_elems, R_add, R_mul)
        nil_S = get_nilradical(S_elems, S_add, S_mul)
        
        if isinstance(f, dict):
            f_eval = lambda x: f[x]
        elif isinstance(f, (list, tuple)):
            def f_eval(x):
                for k, v in f:
                    if k == x: return v
                raise ValueError("Not found")
        else:
            f_eval = f
            
        neg_q = False
        for a in nil_R:
            fa = f_eval(a)
            if fa not in nil_S:
                neg_q = True
                break
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "¬Q: The preimage of the nilradical of S under f does not contain the nilradical of R"
]

N_HYP = 1
NEG_Q_INDEX = 1