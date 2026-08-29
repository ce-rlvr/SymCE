import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup for standard group theory objects
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

def conditions(witness) -> list[bool]:
    """
    Given a witness object, evaluates the hypotheses and the negated conclusion.
    The witness is expected to provide the prime p, groups G and H, 
    surjective homomorphism f, and Sylow p-subgroup P.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 5:
            p, G, H, f, P = witness
        else:
            p = witness.p
            G = witness.G
            H = witness.H
            f = witness.f
            P = witness.P
    except Exception:
        return [False, False, False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H_2: f: G -> H is a surjective group homomorphism
    try:
        if hasattr(f, 'is_surjective') and hasattr(f, 'is_homomorphism'):
            h2 = bool(f.is_homomorphism() and f.is_surjective())
        elif hasattr(witness, 'is_surjective_homomorphism'):
            h2 = bool(witness.is_surjective_homomorphism())
        else:
            G_elems = G.elements if hasattr(G, 'elements') else G
            H_elems = H.elements if hasattr(H, 'elements') else H
            
            is_homo = True
            image_f = set()
            for g in G_elems:
                fg = f[g] if isinstance(f, dict) else f(g)
                image_f.add(fg)
                for g2 in G_elems:
                    fg2 = f[g2] if isinstance(f, dict) else f(g2)
                    g_op_g2 = G.op(g, g2) if hasattr(G, 'op') else g * g2
                    f_g_op_g2 = f[g_op_g2] if isinstance(f, dict) else f(g_op_g2)
                    H_op_fg_fg2 = H.op(fg, fg2) if hasattr(H, 'op') else fg * fg2
                    
                    if f_g_op_g2 != H_op_fg_fg2:
                        is_homo = False
                        break
                if not is_homo:
                    break
            is_surj = (image_f == set(H_elems))
            h2 = is_homo and is_surj
    except Exception:
        h2 = False

    # H_3: P is a Sylow p-subgroup of G
    try:
        if hasattr(G, 'is_sylow_p_subgroup'):
            h3 = bool(G.is_sylow_p_subgroup(P, p))
        elif hasattr(P, 'is_sylow_p_subgroup'):
            h3 = bool(P.is_sylow_p_subgroup(G, p))
        elif hasattr(witness, 'is_sylow_p_subgroup_G'):
            h3 = bool(witness.is_sylow_p_subgroup_G())
        else:
            if hasattr(P, 'is_subgroup'):
                is_sub = P.is_subgroup(G)
                order_P = P.order()
            else:
                G_elems = G.elements if hasattr(G, 'elements') else G
                is_sub = all(x in G_elems for x in P)
                order_P = len(P)
                
            order_G = G.order() if hasattr(G, 'order') else len(G)
            is_p_group = (order_P > 0) and (order_P == p**sympy.factorint(order_P).get(p, 0))
            index_coprime = (order_G // order_P) % p != 0
            h3 = is_sub and is_p_group and index_coprime
    except Exception:
        h3 = False

    # neg_Q: The image f(P) is NOT a Sylow p-subgroup of H
    try:
        if hasattr(f, 'image'):
            fP = f.image(P)
        elif hasattr(witness, 'fP'):
            fP = witness.fP
        else:
            try:
                fP = f(P)
            except Exception:
                P_elems = P.elements if hasattr(P, 'elements') else P
                fP = {f[x] if isinstance(f, dict) else f(x) for x in P_elems}

        if hasattr(H, 'is_sylow_p_subgroup'):
            neg_q = not bool(H.is_sylow_p_subgroup(fP, p))
        elif hasattr(fP, 'is_sylow_p_subgroup'):
            neg_q = not bool(fP.is_sylow_p_subgroup(H, p))
        elif hasattr(witness, 'is_sylow_p_subgroup_H'):
            neg_q = not bool(witness.is_sylow_p_subgroup_H())
        else:
            if hasattr(fP, 'is_subgroup'):
                is_sub_H = fP.is_subgroup(H)
                order_fP = fP.order()
            else:
                H_elems = H.elements if hasattr(H, 'elements') else H
                is_sub_H = all(x in H_elems for x in fP)
                order_fP = len(fP)
                
            order_H = H.order() if hasattr(H, 'order') else len(H)
            is_p_group_H = (order_fP > 0) and (order_fP == p**sympy.factorint(order_fP).get(p, 0))
            index_coprime_H = (order_H // order_fP) % p != 0
            neg_q = not (is_sub_H and is_p_group_H and index_coprime_H)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: f: G -> H is a surjective group homomorphism",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: The image f(P) is not a Sylow p-subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3