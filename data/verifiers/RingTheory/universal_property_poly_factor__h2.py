import sympy
from sympy.combinatorics import *
from sympy.matrices import *
import math
import itertools
import functools

# Top-level setup
x = sympy.Symbol('x')

def check_H1(w):
    try:
        R = w.R
        if not R: return False
        
        # Check closure, commutativity, associativity of add_R and mul_R
        for a in R:
            for b in R:
                s = w.add_R(a, b)
                if s not in R: return False
                if s != w.add_R(b, a): return False
                
                p = w.mul_R(a, b)
                if p not in R: return False
                if p != w.mul_R(b, a): return False
                
                for c in R:
                    if w.add_R(s, c) != w.add_R(a, w.add_R(b, c)): return False
                    if w.mul_R(p, c) != w.mul_R(a, w.mul_R(b, c)): return False
                    if w.mul_R(a, w.add_R(b, c)) != w.add_R(w.mul_R(a, b), w.mul_R(a, c)): return False
                    
        # Check zero_R
        if w.zero_R not in R: return False
        for a in R:
            if w.add_R(a, w.zero_R) != a: return False
            
        # Check additive inverses
        for a in R:
            if not any(w.add_R(a, b) == w.zero_R for b in R): return False
            
        # Check one_R
        if w.one_R not in R: return False
        for a in R:
            if w.mul_R(a, w.one_R) != a: return False
            
        if w.one_R == w.zero_R and len(R) > 1: return False
        return True
    except Exception:
        return False

def check_H2(w):
    try:
        A = w.A
        R = w.R
        if not A or not R: return False
        
        # Check A is a commutative ring (possibly without identity)
        for a in A:
            for b in A:
                s = w.add_A(a, b)
                if s not in A: return False
                if s != w.add_A(b, a): return False
                
                p = w.mul_A(a, b)
                if p not in A: return False
                if p != w.mul_A(b, a): return False
                
                for c in A:
                    if w.add_A(s, c) != w.add_A(a, w.add_A(b, c)): return False
                    if w.mul_A(p, c) != w.mul_A(a, w.mul_A(b, c)): return False
                    if w.mul_A(a, w.add_A(b, c)) != w.add_A(w.mul_A(a, b), w.mul_A(a, c)): return False
                    
        # Check zero_A
        if w.zero_A not in A: return False
        for a in A:
            if w.add_A(a, w.zero_A) != a: return False
            
        # Check additive inverses
        for a in A:
            if not any(w.add_A(a, b) == w.zero_A for b in A): return False
            
        # Check R-module structure and algebra compatibility
        for r in R:
            for a in A:
                ra = w.rmul(r, a)
                if ra not in A: return False
                for b in A:
                    if w.rmul(r, w.add_A(a, b)) != w.add_A(ra, w.rmul(r, b)): return False
                    if w.rmul(r, w.mul_A(a, b)) != w.mul_A(ra, b): return False
                    
        for a in A:
            for r in R:
                for s in R:
                    if w.rmul(w.add_R(r, s), a) != w.add_A(w.rmul(r, a), w.rmul(s, a)): return False
                    if w.rmul(w.mul_R(r, s), a) != w.rmul(r, w.rmul(s, a)): return False
            if w.rmul(w.one_R, a) != a: return False
            
        return True
    except Exception:
        return False

def check_neg_Q(w):
    try:
        A = w.A
        R = w.R
        f = w.f
        
        if not f:
            f = [w.zero_R]
            
        for c in f:
            if c not in R: return False
            
        # Find identity of A if it exists
        id_A = None
        for x in A:
            is_id = True
            for y in A:
                if w.mul_A(x, y) != y or w.mul_A(y, x) != y:
                    is_id = False
                    break
            if is_id:
                id_A = x
                break
                
        # Evaluate roots
        roots = []
        for a in A:
            val = w.zero_A
            valid = True
            for i, c in enumerate(f):
                if i == 0:
                    if c != w.zero_R:
                        if id_A is not None:
                            term = w.rmul(c, id_A)
                            val = w.add_A(val, term)
                        else:
                            valid = False
                            break
                else:
                    apow = a
                    for _ in range(i - 1):
                        apow = w.mul_A(apow, a)
                    term = w.rmul(c, apow)
                    val = w.add_A(val, term)
            if valid and val == w.zero_A:
                roots.append(a)
                
        if not valid:
            return False # Cannot evaluate f(a)
            
        # Find homomorphisms
        homomorphisms = []
        for e in A:
            if w.mul_A(e, e) != e:
                continue
                
            # If A has an identity, standard R-algebra homomorphisms must preserve it
            if id_A is not None and e != id_A:
                continue
                
            for a in A:
                if w.mul_A(a, e) != a:
                    continue
                
                # check phi(f) == 0
                val = w.zero_A
                for i, c in enumerate(f):
                    if i == 0:
                        term = w.rmul(c, e)
                    else:
                        apow = a
                        for _ in range(i - 1):
                            apow = w.mul_A(apow, a)
                        term = w.rmul(c, apow)
                    val = w.add_A(val, term)
                    
                if val == w.zero_A:
                    homomorphisms.append((e, a))
                    
        # Check natural bijection
        natural_bijection = True
        for a in roots:
            count_e = sum(1 for (e_hom, a_hom) in homomorphisms if a_hom == a)
            if count_e != 1:
                natural_bijection = False
                break
                
        for (e, a) in homomorphisms:
            if a not in roots:
                natural_bijection = False
                break
                
        return not natural_bijection
    except Exception:
        return False

def conditions(witness):
    return [
        check_H1(witness),
        check_H2(witness),
        check_neg_Q(witness)
    ]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: A is a commutative R-algebra",
    "¬Q: The natural bijection between R-algebra homomorphisms and roots fails"
]

N_HYP = 2
NEG_Q_INDEX = 2