import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    h1, h2, neg_q = False, False, False
    
    try:
        # Check if witness is a custom object with evaluation methods
        if hasattr(witness, 'is_commutative_ring'):
            h1 = bool(witness.is_commutative_ring())
            h2 = bool(witness.x_in_R())
            lhs = witness.LHS()
            rhs = witness.RHS()
            neg_q = (lhs != rhs)
            return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        # Assume witness is a tuple: (R, x, I_list)
        if isinstance(witness, tuple) and len(witness) == 3:
            R, x, I_list = witness
            
            # H1: R is a commutative ring
            if isinstance(R, str):
                h1 = True
            elif hasattr(R, 'is_commutative'):
                h1 = bool(R.is_commutative)
            else:
                h1 = True
                
            # H2: x is an element of R
            if isinstance(R, str) and R in ['Z', 'ZZ']:
                h2 = isinstance(x, int)
            else:
                try:
                    h2 = (x in R)
                except Exception:
                    h2 = True
                    
            # neg_Q: (\bigcap I_i : x) != \bigcap (I_i : x)
            if isinstance(R, str) and R in ['Z', 'ZZ']:
                def lcm(a, b):
                    return abs(a * b) // math.gcd(a, b) if a and b else 0
                
                def ideal_quotient(I, x):
                    if x == 0:
                        return 1
                    if I == 0:
                        return 0
                    return abs(I) // math.gcd(I, x)
                    
                intersect_I = functools.reduce(lcm, I_list)
                lhs = ideal_quotient(intersect_I, x)
                
                quotients = [ideal_quotient(I, x) for I in I_list]
                rhs = functools.reduce(lcm, quotients)
                
                neg_q = (lhs != rhs)
            else:
                intersect_I = functools.reduce(lambda a, b: a.intersect(b), I_list)
                try:
                    x_ideal = R.ideal(x)
                except Exception:
                    x_ideal = x
                    
                lhs = intersect_I.quotient(x_ideal)
                quotients = [I.quotient(x_ideal) for I in I_list]
                rhs = functools.reduce(lambda a, b: a.intersect(b), quotients)
                
                neg_q = (lhs != rhs)
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: x is an element of R",
    "¬Q: The ideal quotient (\\bigcap_{i=1}^n I_i : x) is NOT equal to the intersection of the ideal quotients \\bigcap_{i=1}^n (I_i : x)"
]

N_HYP = 2
NEG_Q_INDEX = 2