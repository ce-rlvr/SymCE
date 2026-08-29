import sympy
from sympy.combinatorics.named_groups import CyclicGroup, AlternatingGroup, SymmetricGroup, DihedralGroup
from sympy.combinatorics import PermutationGroup
from math import gcd
from sympy.ntheory import factorint

# Top-level setup: named object bindings for witness expressions
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z5 = CyclicGroup(5)
Z6 = CyclicGroup(6)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
trivial = CyclicGroup(1)

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: M(X) denotes the Schur multiplier of a finite group X",
    "¬Q: The Schur multiplier M(G) is NOT isomorphic to the direct product M(S_1) x ... x M(S_k)"
]

def conditions(witness):
    try:
        # Extract factors from witness. The witness can be a list of simple groups [S_1, ..., S_k],
        # a single group G, or a tuple (G, [S_1, ..., S_k]).
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[1], list):
            factors = witness[1]
            is_list = True
        elif isinstance(witness, list):
            factors = witness
            is_list = True
        else:
            factors = [witness]
            is_list = False
            
        # H1: witness provides valid finite groups
        if len(factors) > 0 and all(hasattr(g, 'elements') and hasattr(g, 'order') for g in factors):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False
        factors = []
        is_list = False

    try:
        if not h1:
            neg_q = False
        else:
            if is_list:
                # For a list of groups, the conjecture M(G) ≅ M(S_1) x ... x M(S_k) holds iff 
                # the cross terms in the Schur multiplier of the direct product are trivial.
                # By Schur's formula, the cross terms are trivial iff gcd(|S_i^ab|, |S_j^ab|) == 1 for all i < j.
                ab_sizes = []
                for g in factors:
                    der = g.derived_subgroup()
                    ab_sizes.append(g.order() // der.order())
                    
                cross_terms_non_trivial = False
                for i in range(len(ab_sizes)):
                    for j in range(i + 1, len(ab_sizes)):
                        if gcd(ab_sizes[i], ab_sizes[j]) > 1:
                            cross_terms_non_trivial = True
                            break
                    if cross_terms_non_trivial:
                        break
                neg_q = cross_terms_non_trivial
            else:
                # For a single semisimple group G, the conjecture holds iff G^ab is cyclic.
                g = factors[0]
                gab_cyclic = None
                
                # Try using sympy's built-in abelian_invariants if available
                try:
                    if hasattr(g, 'abelian_invariants'):
                        invs = g.abelian_invariants()
                        primes = []
                        for x in invs:
                            primes.extend(factorint(x).keys())
                        # It is cyclic iff all prime factors in the invariants are distinct
                        gab_cyclic = (len(primes) == len(set(primes)))
                except Exception:
                    pass
                    
                if gab_cyclic is None:
                    # Fallback manual check for G^ab being cyclic
                    der = g.derived_subgroup()
                    n_ab = g.order() // der.order()
                    if n_ab <= 1:
                        gab_cyclic = True
                    elif g.order() > 2000:
                        gab_cyclic = False # Safety limit for manual element iteration
                    else:
                        max_order = 1
                        der_elements = set(der.elements)
                        for e in g.elements:
                            k = 1
                            curr = e
                            while curr not in der_elements:
                                curr = curr * e
                                k += 1
                            if k > max_order:
                                max_order = k
                            if max_order == n_ab:
                                break
                        gab_cyclic = (max_order == n_ab)
                        
                neg_q = not gab_cyclic
    except Exception:
        neg_q = False

    return [h1, neg_q]