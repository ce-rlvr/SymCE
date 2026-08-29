import math
import sympy
from sympy import minpoly, degree, real_roots, factor, isprime, sqrt, cbrt, I, exp, pi, Rational, cos, sin
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def galois_group_order(a, p_a=None):
    """
    Computes the order of the Galois group Gal(Q(a)/Q) by counting the number 
    of roots of the minimal polynomial of 'a' that lie in Q(a).
    """
    if p_a is None:
        p_a = minpoly(a, x)
    
    # Factor the minimal polynomial over the extension field Q(a)
    f = factor(p_a, extension=a)
    
    order = 0
    if f.is_Mul:
        factors = f.args
    else:
        factors = [f]
        
    for fact in factors:
        if fact.has(x):
            if fact.is_Pow:
                base, exp_val = fact.args
            else:
                base, exp_val = fact, 1
            
            # Each linear factor corresponds to a root in Q(a)
            if degree(base, x) == 1:
                order += exp_val
                
    return order

def intersection_is_Q(a, b):
    """
    Checks if the intersection of K_1 = Q(a) and K_2 = Q(b) is exactly Q.
    """
    p_a = minpoly(a, x)
    p_b = minpoly(b, x)
    d_a = degree(p_a)
    d_b = degree(p_b)
    
    # Condition 1: Degrees are coprime
    if math.gcd(d_a, d_b) == 1:
        return True
        
    p_ab = minpoly(a + b, x)
    d_ab = degree(p_ab)
    
    # Condition 2: Fields are linearly disjoint over Q
    if d_ab == d_a * d_b:
        return True
        
    # Condition 3: Distinct fields of the same prime degree
    if isprime(d_a) and d_b == d_a and d_ab > d_a:
        return True
        
    # Condition 4: Conjugate fields whose Galois group acts 2-transitively (e.g., S_n)
    if p_a == p_b and d_ab == d_a * (d_a - 1):
        eq = False
        try:
            eq = a.equals(b)
        except Exception:
            eq = (a == b)
        if not eq:
            return True
            
    return False

def conclusion_holds(a, b):
    """
    Evaluates whether the conclusion of the theorem holds for K_1 = Q(a) and K_2 = Q(b).
    """
    c = a + b
    p_c = minpoly(c, x)
    d_c = degree(p_c)
    
    # Quick check: If K_1 K_2 is real but its minimal polynomial has complex roots, 
    # it cannot be a Galois extension of Q.
    if c.is_real == True:
        try:
            rr = real_roots(p_c)
            if len(rr) < d_c:
                return False
        except Exception:
            pass
            
    # Part 1: Is K_1 K_2 a Galois extension of Q?
    order_c = galois_group_order(c, p_c)
    if order_c != d_c:
        return False
        
    # Part 2: Is the restriction map an isomorphism?
    # A necessary condition for an isomorphism is that the domain and codomain have the same order.
    p_a = minpoly(a, x)
    p_b = minpoly(b, x)
    order_a = galois_group_order(a, p_a)
    order_b = galois_group_order(b, p_b)
    
    if order_c != order_a * order_b:
        return False
        
    return True

def conditions(witness):
    """
    Given a witness (a, b) representing K_1 = Q(a) and K_2 = Q(b),
    returns a list of booleans evaluating the remaining hypotheses and the negated conclusion.
    """
    try:
        a, b = witness
    except Exception:
        return [False, False]
        
    try:
        h1_ok = bool(intersection_is_Q(a, b))
    except Exception:
        h1_ok = False
        
    try:
        neg_q = not conclusion_holds(a, b)
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: K_1 \\cap K_2 = F",
    "¬Q: K_1 K_2 is not Galois over F, or the restriction map is not an isomorphism"
]

N_HYP = 1
NEG_Q_INDEX = 1