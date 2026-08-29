import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_group(G, op):
    # Closure
    for a in G:
        for b in G:
            try:
                if op(a, b) not in G:
                    return False
            except Exception:
                return False
    # Associativity
    for a in G:
        for b in G:
            for c in G:
                try:
                    if op(op(a, b), c) != op(a, op(b, c)):
                        return False
                except Exception:
                    return False
    # Identity
    identity = None
    for e in G:
        is_id = True
        for a in G:
            try:
                if op(e, a) != a or op(a, e) != a:
                    is_id = False
                    break
            except Exception:
                is_id = False
                break
        if is_id:
            identity = e
            break
    if identity is None:
        return False
    # Inverses
    for a in G:
        has_inv = False
        for b in G:
            try:
                if op(a, b) == identity and op(b, a) == identity:
                    has_inv = True
                    break
            except Exception:
                pass
        if not has_inv:
            return False
    return True

def extract_witness(witness):
    if isinstance(witness, dict):
        return list(witness['N']), list(witness['H']), witness['N_op'], witness['H_op'], witness['phi']
    elif isinstance(witness, tuple):
        if len(witness) == 5:
            return list(witness[0]), list(witness[1]), witness[2], witness[3], witness[4]
        elif len(witness) == 3:
            N_obj, H_obj, phi = witness
            N = list(N_obj.elements) if hasattr(N_obj, 'elements') else list(N_obj)
            H = list(H_obj.elements) if hasattr(H_obj, 'elements') else list(H_obj)
            N_op = N_obj.op if hasattr(N_obj, 'op') else (lambda x, y: x * y)
            H_op = H_obj.op if hasattr(H_obj, 'op') else (lambda x, y: x * y)
            return N, H, N_op, H_op, phi
    else:
        N = list(witness.N)
        H = list(witness.H)
        N_op = witness.N_op
        H_op = witness.H_op
        phi = witness.phi
        return N, H, N_op, H_op, phi

def conditions(witness):
    try:
        N, H, N_op, H_op, phi = extract_witness(witness)
    except Exception:
        return [False, False]
        
    # H1: phi: H -> Aut(N) is a group homomorphism
    h1_ok = False
    try:
        if is_group(H, H_op):
            h1_ok = True
            for h in H:
                mapped = []
                for n in N:
                    mapped.append(phi(h, n))
                
                # Check bijection without requiring hashability
                for m in mapped:
                    if mapped.count(m) != 1:
                        h1_ok = False
                        break
                if not h1_ok: break
                
                for n in N:
                    if n not in mapped:
                        h1_ok = False
                        break
                if not h1_ok: break
                
                # Check homomorphism property of phi(h)
                for n1 in N:
                    for n2 in N:
                        if phi(h, N_op(n1, n2)) != N_op(phi(h, n1), phi(h, n2)):
                            h1_ok = False
                            break
                    if not h1_ok: break
                if not h1_ok: break
                
            # Check if phi is a group homomorphism from H to Aut(N)
            if h1_ok:
                for h1 in H:
                    for h2 in H:
                        h12 = H_op(h1, h2)
                        for n in N:
                            if phi(h12, n) != phi(h1, phi(h2, n)):
                                h1_ok = False
                                break
                        if not h1_ok: break
                    if not h1_ok: break
    except Exception:
        h1_ok = False

    # Conclusion: P iff Q
    # P: N rtimes_phi H is an abelian group
    P = False
    try:
        SD = [(n, h) for n in N for h in H]
        def sd_op(x, y):
            n1, h1 = x
            n2, h2 = y
            return (N_op(n1, phi(h1, n2)), H_op(h1, h2))
            
        P = is_group(SD, sd_op)
        if P:
            # Check commutativity
            for x in SD:
                for y in SD:
                    if sd_op(x, y) != sd_op(y, x):
                        P = False
                        break
                if not P: break
    except Exception:
        P = False
        
    # Q: N is abelian, H is abelian, phi is trivial
    Q = False
    try:
        Q = True
        # N is abelian (commutative)
        for n1 in N:
            for n2 in N:
                if N_op(n1, n2) != N_op(n2, n1):
                    Q = False
                    break
            if not Q: break
            
        # H is abelian (commutative)
        if Q:
            for h1 in H:
                for h2 in H:
                    if H_op(h1, h2) != H_op(h2, h1):
                        Q = False
                        break
                if not Q: break
                
        # phi is trivial
        if Q:
            for h in H:
                for n in N:
                    if phi(h, n) != n:
                        Q = False
                        break
                if not Q: break
    except Exception:
        Q = False
        
    neg_Q_ok = (P != Q)
    
    return [h1_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from H to Aut(N)",
    "¬Q: The semidirect product is an abelian group iff N and H are abelian and phi is trivial FAILS"
]

N_HYP = 1
NEG_Q_INDEX = 1