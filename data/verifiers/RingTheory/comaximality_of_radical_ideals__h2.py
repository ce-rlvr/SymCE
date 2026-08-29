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
# Standard integers that can be used as modulo n for finite rings Z_n
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should be a tuple (n, R_set, I_set, J_set) or a dictionary
    with keys 'n', 'R', 'I', 'J', representing a subring R of Z_n and two ideals I, J.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            R_set = witness.get('R')
            I_set = witness.get('I')
            J_set = witness.get('J')
        else:
            n, R_set, I_set, J_set = witness
            
        n = int(n)
        R_set = set(R_set)
        I_set = set(I_set)
        J_set = set(J_set)
        
        if not (n > 0):
            return [False, False, False, False]
        if not R_set.issubset(set(range(n))):
            return [False, False, False, False]
            
        # H1: R is a commutative ring (closed under +, -, *, and commutative)
        h1 = True
        if not R_set:
            h1 = False
        else:
            for a in R_set:
                for b in R_set:
                    if (a + b) % n not in R_set: h1 = False
                    if (a * b) % n not in R_set: h1 = False
                    if (a - b) % n not in R_set: h1 = False
                    if (a * b) % n != (b * a) % n: h1 = False
                    
        # H2: I is an ideal of R
        h2 = True
        if not I_set or not I_set.issubset(R_set):
            h2 = False
        else:
            for a in I_set:
                for b in I_set:
                    if (a + b) % n not in I_set: h2 = False
                    if (a - b) % n not in I_set: h2 = False
            for r in R_set:
                for a in I_set:
                    if (r * a) % n not in I_set: h2 = False
                    
        # H3: J is an ideal of R
        h3 = True
        if not J_set or not J_set.issubset(R_set):
            h3 = False
        else:
            for a in J_set:
                for b in J_set:
                    if (a + b) % n not in J_set: h3 = False
                    if (a - b) % n not in J_set: h3 = False
            for r in R_set:
                for a in J_set:
                    if (r * a) % n not in J_set: h3 = False
                    
        # neg_Q: I and J comaximal iff rad(I) and rad(J) comaximal is FALSE
        rad_I = set()
        for x in R_set:
            curr = x
            for k in range(1, len(R_set) + 2):
                if curr in I_set:
                    rad_I.add(x)
                    break
                curr = (curr * x) % n
                
        rad_J = set()
        for x in R_set:
            curr = x
            for k in range(1, len(R_set) + 2):
                if curr in J_set:
                    rad_J.add(x)
                    break
                curr = (curr * x) % n
                
        I_plus_J = set((i + j) % n for i in I_set for j in J_set)
        rad_I_plus_rad_J = set((i + j) % n for i in rad_I for j in rad_J)
        
        I_J_comaximal = (I_plus_J == R_set)
        rad_I_J_comaximal = (rad_I_plus_rad_J == R_set)
        
        neg_q = (I_J_comaximal != rad_I_J_comaximal)
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "H_3: J is an ideal of R",
    "¬Q: The equivalence (I, J comaximal <=> rad(I), rad(J) comaximal) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3