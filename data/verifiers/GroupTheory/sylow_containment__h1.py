import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: H is a p-subgroup of G",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: For all g in G, H is not a subgroup of gPg^(-1)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    # Extract components
    G, p, H, P = None, None, None, None
    if isinstance(witness, dict):
        G = witness.get('G')
        p = witness.get('p')
        H = witness.get('H')
        P = witness.get('P')
    else:
        try:
            G, p, H, P = witness
        except Exception:
            try:
                G = witness.G
                p = witness.p
                H = witness.H
                P = witness.P
            except Exception:
                return [False, False, False, False]

    # H1: p is a prime number
    try:
        if isinstance(witness, dict) and 'is_prime' in witness:
            try:
                h1 = bool(witness['is_prime'](p))
            except Exception:
                h1 = bool(witness['is_prime']())
        elif hasattr(witness, 'is_prime'):
            try:
                h1 = bool(witness.is_prime(p))
            except Exception:
                h1 = bool(witness.is_prime())
        else:
            h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H2: H is a p-subgroup of G
    try:
        if isinstance(witness, dict) and 'is_p_subgroup' in witness:
            try:
                h2 = bool(witness['is_p_subgroup'](H))
            except Exception:
                h2 = bool(witness['is_p_subgroup']())
        elif hasattr(witness, 'is_p_subgroup'):
            try:
                h2 = bool(witness.is_p_subgroup(H))
            except Exception:
                h2 = bool(witness.is_p_subgroup())
        elif hasattr(H, 'is_p_subgroup'):
            h2 = bool(H.is_p_subgroup(G, p))
        else:
            if hasattr(H, 'is_subgroup'):
                is_sub = bool(H.is_subgroup(G))
                order_H = H.order()
            else:
                is_sub = all(h in G for h in H)
                order_H = len(H)
                
            if order_H == 1:
                h2 = is_sub
            elif order_H != sympy.oo:
                factors = sympy.factorint(order_H)
                h2 = is_sub and list(factors.keys()) == [p]
            else:
                h2 = False
    except Exception:
        h2 = False

    # H3: P is a Sylow p-subgroup of G
    try:
        if isinstance(witness, dict) and 'is_sylow_p_subgroup' in witness:
            try:
                h3 = bool(witness['is_sylow_p_subgroup'](P))
            except Exception:
                h3 = bool(witness['is_sylow_p_subgroup']())
        elif hasattr(witness, 'is_sylow_p_subgroup'):
            try:
                h3 = bool(witness.is_sylow_p_subgroup(P))
            except Exception:
                h3 = bool(witness.is_sylow_p_subgroup())
        elif hasattr(P, 'is_sylow_p_subgroup'):
            h3 = bool(P.is_sylow_p_subgroup(G, p))
        else:
            if hasattr(P, 'is_subgroup'):
                is_sub = bool(P.is_subgroup(G))
                order_P = P.order()
            else:
                is_sub = all(x in G for x in P)
                order_P = len(P)
                
            if hasattr(G, 'order'):
                order_G = G.order()
            else:
                order_G = len(G)
                
            if order_G != sympy.oo and order_P != sympy.oo:
                if order_P == 1:
                    h3 = is_sub and (order_G % p != 0)
                else:
                    factors_P = sympy.factorint(order_P)
                    factors_G = sympy.factorint(order_G)
                    h3 = is_sub and list(factors_P.keys()) == [p] and factors_P[p] == factors_G.get(p, 0)
            else:
                h3 = False
    except Exception:
        h3 = False

    # neg_Q: For all g in G, H is NOT a subgroup of gPg^(-1)
    try:
        if isinstance(witness, dict) and 'conclusion_holds' in witness:
            neg_q = not bool(witness['conclusion_holds']())
        elif hasattr(witness, 'conclusion_holds'):
            neg_q = not bool(witness.conclusion_holds())
        elif isinstance(witness, dict) and 'neg_conclusion_holds' in witness:
            neg_q = bool(witness['neg_conclusion_holds']())
        elif hasattr(witness, 'neg_conclusion_holds'):
            neg_q = bool(witness.neg_conclusion_holds())
        else:
            conclusion = False
            count = 0
            elements = getattr(G, 'elements', G)
            for g in elements:
                try:
                    inv_g = ~g
                except Exception:
                    try:
                        inv_g = g**-1
                    except Exception:
                        continue
                
                try:
                    if hasattr(P, 'generators') and hasattr(H, 'is_subgroup'):
                        gens = [g * gen * inv_g for gen in P.generators]
                        P_conj = type(P)(gens)
                        is_sub = H.is_subgroup(P_conj)
                    else:
                        P_conj = {g * x * inv_g for x in P}
                        is_sub = all(h in P_conj for h in H)
                    
                    if is_sub:
                        conclusion = True
                        break
                except Exception:
                    pass
                
                count += 1
                if count > 1000:
                    break
            neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]