import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def conditions(witness):
    # H_1: G is a nilpotent group
    h1 = False
    try:
        if isinstance(witness, dict):
            val = witness.get('is_nilpotent', False)
            h1 = bool(val() if callable(val) else val)
        else:
            val = getattr(witness, 'is_nilpotent', False)
            h1 = bool(val() if callable(val) else val)
    except Exception:
        h1 = False

    # neg_Q: The commutator subgroup of G is NOT contained in the Frattini subgroup of G
    neg_q = False
    try:
        if isinstance(witness, dict):
            comm = witness.get('commutator_subgroup')
            if comm is None:
                comm = witness.get('derived_subgroup')
            if callable(comm): 
                comm = comm()
            
            frat = witness.get('frattini_subgroup')
            if callable(frat): 
                frat = frat()
        else:
            comm = getattr(witness, 'commutator_subgroup', None)
            if comm is None:
                comm = getattr(witness, 'derived_subgroup', None)
            if callable(comm): 
                comm = comm()
            
            frat = getattr(witness, 'frattini_subgroup', None)
            if callable(frat): 
                frat = frat()
            
        if comm is not None and frat is not None:
            contained = None
            
            # Try is_subgroup method
            if hasattr(comm, 'is_subgroup'):
                try:
                    contained = comm.is_subgroup(frat)
                except Exception:
                    pass
            
            # Try <= operator (avoiding lists/tuples where <= means lexicographical comparison)
            if contained is None and hasattr(comm, '__le__') and not isinstance(comm, (list, tuple)):
                try:
                    res = comm <= frat
                    if isinstance(res, bool):
                        contained = res
                except Exception:
                    pass
            
            # Try checking generators
            if contained is None:
                gens = getattr(comm, 'generators', getattr(comm, 'gens', None))
                if gens is not None:
                    try:
                        if hasattr(frat, 'contains'):
                            contained = all(frat.contains(g) for g in gens)
                        else:
                            contained = all(g in frat for g in gens)
                    except Exception:
                        pass
            
            # Try iterating over all elements
            if contained is None:
                try:
                    if hasattr(frat, 'contains'):
                        contained = all(frat.contains(g) for g in comm)
                    else:
                        contained = all(g in frat for g in comm)
                except Exception:
                    pass
            
            if contained is not None:
                neg_q = not contained
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: The commutator subgroup of G is not contained in the Frattini subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1