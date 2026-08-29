import itertools
import math
from functools import reduce

from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer, Symbol

# Top-level setup for named objects that a witness expression might reference.
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _get_ideals(R, add, mul):
    """Helper to compute all ideals of a finite ring/semiring given its elements and operations."""
    n = len(R)
    ideals = []
    for i in range(1, 1 << n):
        subset = [R[j] for j in range(n) if (i & (1 << j))]
        is_ideal = True
        # Check closure under addition
        for x in subset:
            for y in subset:
                if add(x, y) not in subset:
                    is_ideal = False
                    break
            if not is_ideal: break
        if not is_ideal: continue
        
        # Check closure under left and right multiplication by all elements
        for r in R:
            for x in subset:
                if mul(r, x) not in subset or mul(x, r) not in subset:
                    is_ideal = False
                    break
            if not is_ideal: break
        if is_ideal:
            ideals.append(frozenset(subset))
    return ideals

def get_equivalence_classes(R, I, add):
    """Compute equivalence classes for R/I under the relation a ~ b iff exists x, y in I, a + x = b + y."""
    n = len(R)
    adj = [[False]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            rel = False
            for x in I:
                for y in I:
                    if add(R[i], x) == add(R[j], y):
                        rel = True
                        break
                if rel: break
            adj[i][j] = rel
            
    visited = [False]*n
    classes = []
    for i in range(n):
        if not visited[i]:
            comp = []
            q = [i]
            visited[i] = True
            while q:
                curr = q.pop(0)
                comp.append(R[curr])
                for j in range(n):
                    if adj[curr][j] and not visited[j]:
                        visited[j] = True
                        q.append(j)
            classes.append(frozenset(comp))
    return classes

def conditions(witness) -> list[bool]:
    try:
        # Witness can be a tuple (R, I, add, mul) or an object with these attributes
        if isinstance(witness, tuple) and len(witness) == 4:
            R, I, add, mul = witness
        else:
            R = witness.R
            I = witness.I
            add = witness.add
            mul = witness.mul
            
        if not (isinstance(R, (list, tuple)) and isinstance(I, (list, tuple))):
            return [False, False, False]
            
        if len(R) == 0 or len(I) == 0:
            return [False, False, False]
            
        ideals = _get_ideals(R, add, mul)
        I_set = frozenset(I)
        R_set = frozenset(R)
        
        # H1: I is a proper ideal of R
        H1 = (I_set in ideals) and (I_set != R_set)
        
        # H2: \pi: R -> R/I is the canonical projection homomorphism
        # This is structurally true by our construction of R/I
        H2 = True
        
        # Construct R/I
        classes = get_equivalence_classes(R, I, add)
        
        def add_coset(c1, c2):
            r1 = next(iter(c1))
            r2 = next(iter(c2))
            r3 = add(r1, r2)
            for c in classes:
                if r3 in c: return c
            return None

        def mul_coset(c1, c2):
            r1 = next(iter(c1))
            r2 = next(iter(c2))
            r3 = mul(r1, r2)
            for c in classes:
                if r3 in c: return c
            return None
            
        ideals_RI = _get_ideals(classes, add_coset, mul_coset)
        
        # Find maximal ideals of R
        proper_ideals = [ideal for ideal in ideals if ideal != R_set]
        max_ideals = []
        for ideal in proper_ideals:
            is_max = True
            for other in proper_ideals:
                if ideal < other:
                    is_max = False
                    break
            if is_max:
                max_ideals.append(ideal)
                
        max_ideals_containing_I = [ideal for ideal in max_ideals if I_set.issubset(ideal)]
        
        # Find maximal ideals of R/I
        classes_set = frozenset(classes)
        proper_ideals_RI = [ideal for ideal in ideals_RI if ideal != classes_set]
        max_ideals_RI = []
        for ideal in proper_ideals_RI:
            is_max = True
            for other in proper_ideals_RI:
                if ideal < other:
                    is_max = False
                    break
            if is_max:
                max_ideals_RI.append(ideal)
                
        # Map M \mapsto \pi(M)
        mapped_max_ideals = []
        for M in max_ideals_containing_I:
            M_proj = set()
            for m in M:
                for c in classes:
                    if m in c:
                        M_proj.add(c)
                        break
            mapped_max_ideals.append(frozenset(M_proj))
            
        # Check if the map establishes a bijection
        is_bijection = True
        if len(mapped_max_ideals) != len(max_ideals_RI):
            is_bijection = False
        else:
            unique_mapped = set(mapped_max_ideals)
            if len(unique_mapped) != len(mapped_max_ideals):
                is_bijection = False
            else:
                if unique_mapped != set(max_ideals_RI):
                    is_bijection = False
                    
        neg_Q = not is_bijection
        
        return [bool(H1), bool(H2), bool(neg_Q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "H_2: \\pi: R -> R/I is the canonical projection homomorphism",
    "¬Q: The map M \\mapsto \\pi(M) does not establish a bijection between the maximal ideals of R containing I and the maximal ideals of R/I"
]

N_HYP = 2
NEG_Q_INDEX = 2