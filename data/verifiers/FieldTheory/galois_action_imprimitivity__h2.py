import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools

# Top-level setup for potential witness objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f(x) is an irreducible separable polynomial over K",
    "H_2: R is the set of roots of f(x) in L",
    "H_3: Gal(L/K) acts imprimitively on R with a non-trivial block system",
    "H_4: \\alpha is a root in R",
    "¬Q: K(\\alpha) has no intermediate fields"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the Galois Action Imprimitivity Theorem conjecture.
    Supports both an abstract group-theoretic witness (using PermutationGroups) and a polynomial witness.
    """
    # H_1: f(x) is an irreducible separable polynomial over K
    try:
        if hasattr(witness, 'G'):
            # Group theory equivalent: The Galois group of the splitting field acts transitively on the roots.
            h1 = bool(witness.G.is_transitive())
        else:
            poly_f = sympy.Poly(witness.f)
            h1 = bool(poly_f.is_irreducible)
    except Exception:
        h1 = False

    # H_2: R is the set of roots of f(x) in L
    try:
        if hasattr(witness, 'G'):
            # Group theory equivalent: R is the set of roots fixed by Gal(E/L) (represented by subgroup H).
            degree = witness.G.degree
            fixed_points = {i for i in range(degree) if all(h(i) == i for h in witness.H.generators)}
            h2 = set(witness.R) == fixed_points
        else:
            poly_f = sympy.Poly(witness.f)
            h2 = all(poly_f.eval(r) == 0 for r in witness.R) and len(set(witness.R)) == len(witness.R)
    except Exception:
        h2 = False

    # H_3: Gal(L/K) acts imprimitively on R with a non-trivial block system
    try:
        if not witness.R:
            h3 = False
        else:
            block_sets = [set(b) for b in witness.blocks]
            is_partition = set().union(*block_sets) == set(witness.R) and sum(len(b) for b in block_sets) == len(witness.R)
            non_trivial = 1 < len(block_sets) < len(witness.R)
            
            if hasattr(witness, 'G'):
                # Gal(L/K) corresponds to N_G(H)/H. We check the action of N_G(H) on R.
                if hasattr(witness, 'N_generators'):
                    N_G_H = witness.N_generators
                else:
                    N_G_H = [g for g in witness.G.generate() if all((g * h * ~g) in witness.H for h in witness.H.generators)]
                
                R_list = list(witness.R)
                orbit = {R_list[0]}
                while True:
                    new_orbit = orbit.copy()
                    for g in N_G_H:
                        for x in orbit:
                            new_orbit.add(g(x))
                    if len(new_orbit) == len(orbit):
                        break
                    orbit = new_orbit
                is_transitive = orbit == set(witness.R)
                
                preserves = True
                for g in N_G_H:
                    for b in block_sets:
                        mapped_b = {g(x) for x in b}
                        if mapped_b not in block_sets:
                            preserves = False
                            break
                    if not preserves:
                        break
            else:
                preserves = True
                for g in witness.Gal:
                    for b in block_sets:
                        mapped_b = {g(x) for x in b}
                        if mapped_b not in block_sets:
                            preserves = False
                            break
                    if not preserves:
                        break
                
                R_list = list(witness.R)
                orbit = {R_list[0]}
                while True:
                    new_orbit = orbit.copy()
                    for g in witness.Gal:
                        for x in orbit:
                            new_orbit.add(g(x))
                    if len(new_orbit) == len(orbit):
                        break
                    orbit = new_orbit
                is_transitive = orbit == set(witness.R)
                
            h3 = bool(is_partition and non_trivial and is_transitive and preserves)
    except Exception:
        h3 = False

    # H_4: \alpha is a root in R
    try:
        h4 = bool(witness.alpha in witness.R)
    except Exception:
        h4 = False

    # ¬Q: K(\alpha) has no intermediate fields
    try:
        if hasattr(witness, 'G'):
            # Group theory equivalent: K(\alpha) has no intermediate fields iff G acts primitively on the roots.
            neg_q = bool(witness.G.is_primitive())
        else:
            # If deg(f) is prime, K(\alpha) has prime degree and thus no intermediate fields.
            deg = sympy.Poly(witness.f).degree()
            neg_q = bool(sympy.ntheory.isprime(deg))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]