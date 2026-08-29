import sympy
from sympy import Rational, Integer
import itertools
import math
import functools

# Top-level setup
# (No specific named bindings required for this generic ring theory verifier)

def extract(witness):
    if isinstance(witness, dict):
        return (witness['R'], witness['S'], witness['add_R'], witness['mul_R'], 
                witness['add_S'], witness['mul_S'], witness['f'], witness['N'])
    elif isinstance(witness, tuple):
        return witness
    else:
        return (witness.R, witness.S, witness.add_R, witness.mul_R, 
                witness.add_S, witness.mul_S, witness.f, witness.N)

def get_zero(elements, add):
    for e in elements:
        if all(add(e, a) == a and add(a, e) == a for a in elements):
            return e
    return None

def get_neg(a, zero, elements, add):
    for b in elements:
        if add(a, b) == zero and add(b, a) == zero:
            return b
    return None

def ideal_generated_by(X, elements, add, mul, zero):
    ideal = set(X)
    ideal.add(zero)
    while True:
        size = len(ideal)
        new_ideal = set(ideal)
        for a in ideal:
            for b in ideal:
                new_ideal.add(add(a, b))
            neg_a = get_neg(a, zero, elements, add)
            if neg_a is not None:
                new_ideal.add(neg_a)
            for r in elements:
                new_ideal.add(mul(a, r))
                new_ideal.add(mul(r, a))
        ideal = new_ideal
        if len(ideal) == size:
            break
    return ideal

def is_ideal(I, elements, add, mul, zero):
    I_set = set(I)
    elements_set = set(elements)
    if not I_set.issubset(elements_set):
        return False
    if zero not in I_set:
        return False
    for a in I_set:
        for b in I_set:
            if add(a, b) not in I_set:
                return False
        neg_a = get_neg(a, zero, elements, add)
        if neg_a is not None and neg_a not in I_set:
            return False
        for r in elements:
            if mul(a, r) not in I_set:
                return False
            if mul(r, a) not in I_set:
                return False
    return True

def is_nilpotent(I, elements, add, mul, zero):
    if not I:
        return True
    if all(x == zero for x in I):
        return True
        
    powers = {}
    powers[1] = set(I)
    
    max_n = len(elements) + 2
    for n in range(2, max_n + 1):
        products = set()
        for i in range(1, n):
            for a in powers[i]:
                for b in powers[n-i]:
                    products.add(mul(a, b))
        
        powers[n] = ideal_generated_by(products, elements, add, mul, zero)
        if all(x == zero for x in powers[n]):
            return True
            
    return False

def conditions(witness):
    try:
        R, S, add_R, mul_R, add_S, mul_S, f, N = extract(witness)
        R = list(R)
        S = list(S)
        N = list(N)
        
        zero_R = get_zero(R, add_R)
        zero_S = get_zero(S, add_S)
        
        if zero_R is None or zero_S is None:
            return [False, False, False, False]
            
        def evaluate_f(x):
            if isinstance(f, dict):
                return f[x]
            return f(x)
            
        # H1: f is a ring homomorphism
        h1 = True
        S_set = set(S)
        for a in R:
            fa = evaluate_f(a)
            if fa not in S_set:
                h1 = False
            for b in R:
                if evaluate_f(add_R(a, b)) != add_S(evaluate_f(a), evaluate_f(b)):
                    h1 = False
                if evaluate_f(mul_R(a, b)) != mul_S(evaluate_f(a), evaluate_f(b)):
                    h1 = False
                    
        # H2: N is a nilpotent ideal of S
        h2 = is_ideal(N, S, add_S, mul_S, zero_S) and is_nilpotent(N, S, add_S, mul_S, zero_S)
        
        # H3: ker(f) is a nilpotent ideal of R
        ker_f = [x for x in R if evaluate_f(x) == zero_S]
        h3 = is_ideal(ker_f, R, add_R, mul_R, zero_R) and is_nilpotent(ker_f, R, add_R, mul_R, zero_R)
        
        # neg_Q: f^{-1}(N) is NOT a nilpotent ideal of R
        preimage = [x for x in R if evaluate_f(x) in N]
        is_id = is_ideal(preimage, R, add_R, mul_R, zero_R)
        is_nil = is_nilpotent(preimage, R, add_R, mul_R, zero_R)
        neg_q = not (is_id and is_nil)
        
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S",
    "H_2: N is a nilpotent ideal of S",
    "H_3: ker(f) is a nilpotent ideal of R",
    "¬Q: The preimage f^{-1}(N) is not a nilpotent ideal of R"
]
N_HYP = 3
NEG_Q_INDEX = 3