import z3
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

CONDITION_LABELS = [
    "H_1: phi is an automorphism of G",
    "H_2: phi(phi(x)) = x for all x in G",
    "H_3: phi(x) = x implies x = e",
    "¬Q: G is not abelian or phi(x) != x^-1 for some x"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    # Check for z3 model
    if isinstance(witness, tuple) and len(witness) >= 6 and isinstance(witness[0], z3.ModelRef):
        try:
            model = witness[0]
            G_sort = witness[1]
            op = witness[2]
            phi = witness[3]
            e = witness[4]
            inv = witness[5]
            
            x, y = z3.Consts('x y', G_sort)
            
            homo = z3.ForAll([x, y], phi(op(x, y)) == op(phi(x), phi(y)))
            inj = z3.ForAll([x, y], z3.Implies(phi(x) == phi(y), x == y))
            surj = z3.ForAll([y], z3.Exists([x], phi(x) == y))
            
            h1 = bool(model.eval(homo, model_completion=True)) and \
                 bool(model.eval(inj, model_completion=True)) and \
                 bool(model.eval(surj, model_completion=True))
                 
            h2_expr = z3.ForAll([x], phi(phi(x)) == x)
            h2 = bool(model.eval(h2_expr, model_completion=True))
            
            h3_expr = z3.ForAll([x], z3.Implies(phi(x) == x, x == e))
            h3 = bool(model.eval(h3_expr, model_completion=True))
            
            abelian = z3.ForAll([x, y], op(x, y) == op(y, x))
            inversion = z3.ForAll([x], phi(x) == inv(x))
            q_expr = z3.And(abelian, inversion)
            neg_q = not bool(model.eval(q_expr, model_completion=True))
            
            return [h1, h2, h3, neg_q]
        except Exception:
            return [False, False, False, False]

    # Standard Python object / Iterable
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, phi = witness
                e_provided = getattr(G, 'identity', getattr(G, 'e', None))
                op_provided = getattr(G, 'op', lambda x, y: x * y)
                inv_provided = getattr(G, 'inv', None)
            elif len(witness) == 3:
                G, phi, e_provided = witness
                op_provided = getattr(G, 'op', lambda x, y: x * y)
                inv_provided = getattr(G, 'inv', None)
            elif len(witness) == 5:
                G, phi, e_provided, op_provided, inv_provided = witness
            else:
                G = witness[0]
                phi = witness[1]
                e_provided = witness[2]
                op_provided = witness[3]
                inv_provided = witness[4]
        else:
            G = witness
            phi = G.phi
            op_provided = getattr(G, 'op', lambda x, y: x * y)
            inv_provided = getattr(G, 'inv', None)
            e_provided = getattr(G, 'e', getattr(G, 'identity', None))

        if hasattr(G, 'test_elements'):
            elements = list(G.test_elements)
        elif hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)

        op = op_provided

        e = e_provided
        if e is None:
            for x in elements:
                is_id = True
                for y in elements:
                    if op(x, y) != y or op(y, x) != y:
                        is_id = False
                        break
                if is_id:
                    e = x
                    break

        if inv_provided is not None:
            inv = inv_provided
        else:
            def inv(x):
                try:
                    res = x**-1
                    if op(x, res) == e and op(res, x) == e:
                        return res
                except Exception:
                    pass
                try:
                    res = -x
                    if op(x, res) == e and op(res, x) == e:
                        return res
                except Exception:
                    pass
                for y in elements:
                    if op(x, y) == e and op(y, x) == e:
                        return y
                raise ValueError("Inverse not found")
    except Exception:
        return [False, False, False, False]

    # H1: phi is an automorphism
    h1 = True
    try:
        mapped = []
        for x in elements:
            px = phi(x)
            mapped.append(px)
            for y in elements:
                if phi(op(x, y)) != op(px, phi(y)):
                    h1 = False
                    break
            if not h1:
                break
        if h1:
            is_inj = True
            for i in range(len(mapped)):
                for j in range(i + 1, len(mapped)):
                    if mapped[i] == mapped[j]:
                        is_inj = False
                        break
                if not is_inj:
                    break
            if not is_inj:
                h1 = False
                
        if h1:
            for x in elements:
                found = False
                for m in mapped:
                    if x == m:
                        found = True
                        break
                if not found:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: phi(phi(x)) = x
    h2 = True
    try:
        for x in elements:
            if phi(phi(x)) != x:
                h2 = False
                break
    except Exception:
        h2 = False

    # H3: phi(x) = x implies x = e
    h3 = True
    try:
        for x in elements:
            if phi(x) == x:
                if x != e:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # neg_Q
    neg_q = False
    try:
        is_abelian = True
        for x in elements:
            for y in elements:
                if op(x, y) != op(y, x):
                    is_abelian = False
                    break
            if not is_abelian:
                break
        
        if not is_abelian:
            neg_q = True
        else:
            is_inversion = True
            for x in elements:
                if phi(x) != inv(x):
                    is_inversion = False
                    break
            neg_q = not is_inversion
    except Exception:
        pass

    return [h1, h2, h3, neg_q]