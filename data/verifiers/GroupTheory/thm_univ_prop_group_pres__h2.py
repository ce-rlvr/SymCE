import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.free_groups import FreeGroupElement
import itertools
import functools
import math

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

def get_witness_parts(witness):
    if isinstance(witness, dict):
        G = witness.get('G')
        H = witness.get('H')
        f = witness.get('f')
        op = witness.get('op')
        id_H = witness.get('id_H')
    elif isinstance(witness, tuple) and len(witness) == 3:
        G, H, f = witness
        op = None
        id_H = None
    else:
        return None, [], None, None, None

    try:
        H_list = list(H)
    except Exception:
        H_list = []

    if op is None:
        op = lambda a, b: a * b

    if id_H is None and H_list:
        try:
            for e in H_list:
                is_id = True
                for a in H_list:
                    if op(e, a) != a or op(a, e) != a:
                        is_id = False
                        break
                if is_id:
                    id_H = e
                    break
        except Exception:
            pass

    return G, H_list, f, op, id_H

def conditions(witness) -> list[bool]:
    G, H_list, f, op, id_H = get_witness_parts(witness)
    
    # H_1: G is a group defined by the presentation <X | R>
    try:
        h1 = isinstance(G, FpGroup)
    except Exception:
        h1 = False

    # H_2: f: X -> H is a mapping
    try:
        if not h1:
            h2 = False
        else:
            h2 = True
            for gen in G.generators:
                if callable(f):
                    val = f(gen)
                else:
                    if gen not in f:
                        h2 = False
                        break
                    val = f[gen]
                
                in_H = False
                for h in H_list:
                    if val == h:
                        in_H = True
                        break
                if not in_H:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H_3: For every relation w=1 in R, substitution yields the identity element in H
    try:
        if not h1 or not h2:
            h3 = False
        else:
            h3 = True
            for w in G.relators:
                res = id_H
                for gen, power in w.array_form:
                    if callable(f):
                        val = f(gen)
                    else:
                        if gen not in f:
                            h3 = False
                            break
                        val = f[gen]
                    
                    if power == 0:
                        continue
                    elif power > 0:
                        for _ in range(power):
                            res = op(res, val)
                    else:
                        inv_val = None
                        for h in H_list:
                            if op(val, h) == id_H and op(h, val) == id_H:
                                inv_val = h
                                break
                        if inv_val is None:
                            h3 = False
                            break
                        for _ in range(-power):
                            res = op(res, inv_val)
                if not h3:
                    break
                if res != id_H:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # neg_Q: The conclusion fails (H is not a valid group, so a group homomorphism to H cannot exist)
    try:
        if not H_list:
            is_grp = False
        elif id_H is None:
            is_grp = False
        else:
            is_grp = True
            # Check closure
            for a in H_list:
                for b in H_list:
                    try:
                        c = op(a, b)
                        in_H = False
                        for h in H_list:
                            if c == h:
                                in_H = True
                                break
                        if not in_H:
                            is_grp = False
                            break
                    except Exception:
                        is_grp = False
                        break
                if not is_grp: break
            
            # Check associativity
            if is_grp:
                for a in H_list:
                    for b in H_list:
                        for c in H_list:
                            try:
                                if op(op(a, b), c) != op(a, op(b, c)):
                                    is_grp = False
                                    break
                            except Exception:
                                is_grp = False
                                break
                        if not is_grp: break
                    if not is_grp: break
            
            # Check identity
            if is_grp:
                for a in H_list:
                    try:
                        if op(a, id_H) != a or op(id_H, a) != a:
                            is_grp = False
                            break
                    except Exception:
                        is_grp = False
                        break
            
            # Check inverses
            if is_grp:
                for a in H_list:
                    has_inv = False
                    for b in H_list:
                        try:
                            if op(a, b) == id_H and op(b, a) == id_H:
                                has_inv = True
                                break
                        except Exception:
                            pass
                    if not has_inv:
                        is_grp = False
                        break
            
        neg_q = not is_grp
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group defined by the presentation <X | R>",
    "H_2: f is a mapping from X to H",
    "H_3: For every relation w=1 in R, substitution of f(x) yields the identity in H",
    "¬Q: There does not exist a unique group homomorphism phi: G -> H extending f"
]

N_HYP = 3
NEG_Q_INDEX = 3