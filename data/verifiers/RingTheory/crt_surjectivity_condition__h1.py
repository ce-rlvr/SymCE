import math
import itertools
import functools

from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup for standard groups and matrices
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to be a finite ring represented by its size, 
    addition table, multiplication table, and a list of ideals.
    Format: (n, add_table, mul_table, ideals) or a dict with these keys.
    """
    try:
        if isinstance(witness, dict):
            n = witness['n']
            add = witness['add']
            mul = witness['mul']
            ideals = witness['ideals']
        else:
            n, add, mul, ideals = witness
            
        n = int(n)
        if n <= 0:
            return [False, False, False]
            
        R = list(range(n))
        
        # Validate table dimensions
        if len(add) != n or any(len(row) != n for row in add): return [False, False, False]
        if len(mul) != n or any(len(row) != n for row in mul): return [False, False, False]
        
        # Ring axioms checks
        if any(add[x][y] != add[y][x] for x in R for y in R): return [False, False, False]
        if any(add[add[x][y]][z] != add[x][add[y][z]] for x in R for y in R for z in R): return [False, False, False]
        if any(mul[mul[x][y]][z] != mul[x][mul[y][z]] for x in R for y in R for z in R): return [False, False, False]
        if any(mul[x][add[y][z]] != add[mul[x][y]][mul[x][z]] for x in R for y in R for z in R): return [False, False, False]
        if any(mul[add[x][y]][z] != add[mul[x][z]][mul[y][z]] for x in R for y in R for z in R): return [False, False, False]
        
        # Find additive identity
        zero = None
        for e in R:
            if all(add[e][x] == x for x in R):
                zero = e
                break
        if zero is None: return [False, False, False]
        
        # Find additive inverses
        neg = [None] * n
        for x in R:
            for y in R:
                if add[x][y] == zero:
                    neg[x] = y
                    break
            if neg[x] is None: return [False, False, False]
            
        # H_1: I_1, ..., I_n are ideals of R
        h1 = True
        for I in ideals:
            I_set = set(I)
            if not I_set:
                h1 = False; break
            # Closed under addition
            if any(add[x][y] not in I_set for x in I for y in I):
                h1 = False; break
            # Closed under additive inverse
            if any(neg[x] not in I_set for x in I):
                h1 = False; break
            # Closed under left and right multiplication by any element in R
            if any(mul[r][x] not in I_set for r in R for x in I):
                h1 = False; break
            if any(mul[x][r] not in I_set for r in R for x in I):
                h1 = False; break
                
        # H_2: The canonical map phi is surjective
        # phi(x) = (x + I_1, ..., x + I_n)
        image = set()
        for x in R:
            # Represent coset x + I as a frozenset of its elements
            tup = tuple(frozenset(add[x][y] for y in I) for I in ideals)
            image.add(tup)
            
        # The codomain size is the product of the sizes of the quotient rings
        codomain_size = 1
        for I in ideals:
            cosets = set()
            for x in R:
                cosets.add(frozenset(add[x][y] for y in I))
            codomain_size *= len(cosets)
            
        h2 = (len(image) == codomain_size)
        
        # neg_Q: The ideals are NOT pairwise comaximal
        # This means there exists i != j such that I_i + I_j != R
        neg_q = False
        for i in range(len(ideals)):
            for j in range(i + 1, len(ideals)):
                sum_ideal = set(add[x][y] for x in ideals[i] for y in ideals[j])
                if len(sum_ideal) < n:
                    neg_q = True
                    break
            if neg_q:
                break
                
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I_1, ..., I_n are ideals of R",
    "H_2: The canonical map phi to the product of quotient rings is surjective",
    "¬Q: The ideals are not pairwise comaximal (there exist i != j such that I_i + I_j != R)"
]

N_HYP = 2
NEG_Q_INDEX = 2