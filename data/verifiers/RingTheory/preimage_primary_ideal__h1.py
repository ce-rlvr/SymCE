import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

class RingAdapter:
    def __init__(self, ring, prefix=''):
        self.ring = ring
        self.prefix = prefix

    @property
    def elements(self):
        if isinstance(self.ring, dict):
            elems = self.ring.get(f'{self.prefix}elems', self.ring.get('elements', []))
        elif hasattr(self.ring, 'elements'):
            elems = self.ring.elements
        elif hasattr(self.ring, 'elems'):
            elems = self.ring.elems
        else:
            elems = []
        
        try:
            length = len(elems)
        except Exception:
            raise ValueError("Elements must be finite")
        
        if length > 500:
            raise ValueError("Ring too large")
            
        return list(elems)

    def add(self, a, b):
        if isinstance(self.ring, dict):
            op = self.ring.get(f'{self.prefix}add', self.ring.get('add'))
            if isinstance(op, dict): return op[(a, b)]
            return op(a, b)
        if hasattr(self.ring, 'add'):
            return self.ring.add(a, b)
        return a + b

    def mul(self, a, b):
        if isinstance(self.ring, dict):
            op = self.ring.get(f'{self.prefix}mul', self.ring.get('mul'))
            if isinstance(op, dict): return op[(a, b)]
            return op(a, b)
        if hasattr(self.ring, 'mul'):
            return self.ring.mul(a, b)
        return a * b

    @property
    def zero(self):
        if isinstance(self.ring, dict):
            return self.ring.get(f'{self.prefix}zero', self.ring.get('zero'))
        if hasattr(self.ring, 'zero'):
            return self.ring.zero
        elems = self.elements
        return elems[0] if elems else None

    @property
    def one(self):
        if isinstance(self.ring, dict):
            return self.ring.get(f'{self.prefix}one', self.ring.get('one'))
        if hasattr(self.ring, 'one'):
            return self.ring.one
        return None

def parse_witness(witness):
    if isinstance(witness, tuple) and len(witness) == 4:
        R, S, f, Q = witness
        return RingAdapter(R), RingAdapter(S), f, Q
    elif isinstance(witness, dict):
        if 'R' in witness and 'S' in witness:
            return RingAdapter(witness['R']), RingAdapter(witness['S']), witness['f'], witness['Q']
        else:
            return RingAdapter(witness, 'R_'), RingAdapter(witness, 'S_'), witness['f'], witness['Q']
    else:
        return RingAdapter(witness.R), RingAdapter(witness.S), witness.f, witness.Q

def call_f(f, a):
    if isinstance(f, dict):
        return f[a]
    return f(a)

def is_ideal(I, ring):
    I_set = set(I)
    if not I_set:
        return False
    if ring.zero is not None and ring.zero not in I_set:
        return False
    elems = ring.elements
    for a in I_set:
        for b in I_set:
            if ring.add(a, b) not in I_set:
                return False
    for a in I_set:
        for r in elems:
            if ring.mul(r, a) not in I_set:
                return False
            if ring.mul(a, r) not in I_set:
                return False
    return True

def generate_ideal(gens, ring):
    ideal = set(gens)
    if ring.zero is not None:
        ideal.add(ring.zero)
    elems = ring.elements
    
    while True:
        size_before = len(ideal)
        new_elements = set()
        for a in ideal:
            for b in ideal:
                new_elements.add(ring.add(a, b))
            for r in elems:
                new_elements.add(ring.mul(r, a))
                new_elements.add(ring.mul(a, r))
        ideal.update(new_elements)
        if len(ideal) == size_before:
            break
    return ideal

def get_all_ideals(ring):
    elems = ring.elements
    principal_ideals = []
    for x in elems:
        principal_ideals.append(frozenset(generate_ideal([x], ring)))
    
    ideals = set(principal_ideals)
    queue = list(ideals)
    while queue:
        curr = queue.pop(0)
        for p in principal_ideals:
            new_ideal = set()
            for a in curr:
                for b in p:
                    new_ideal.add(ring.add(a, b))
            new_ideal = frozenset(new_ideal)
            if new_ideal not in ideals:
                ideals.add(new_ideal)
                queue.append(new_ideal)
    return list(ideals)

def is_primary_ideal(Q, ring):
    Q_set = frozenset(Q)
    elems = ring.elements
    if len(Q_set) == len(elems):
        return False
    
    ideals = get_all_ideals(ring)
    
    for I in ideals:
        for J in ideals:
            subset = True
            for i in I:
                for j in J:
                    if ring.mul(i, j) not in Q_set:
                        subset = False
                        break
                if not subset:
                    break
            
            if subset:
                if I.issubset(Q_set):
                    continue
                
                J_n = J
                found = False
                for n in range(1, len(elems) + 2):
                    if J_n.issubset(Q_set):
                        found = True
                        break
                    prods = {ring.mul(a, b) for a in J_n for b in J}
                    J_n = frozenset(generate_ideal(prods, ring))
                
                if not found:
                    return False
    return True

def conditions(witness):
    try:
        R, S, f, Q = parse_witness(witness)
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = True
        for a in R.elements:
            fa = call_f(f, a)
            if fa not in S.elements:
                h1 = False
                break
            for b in R.elements:
                if call_f(f, R.add(a, b)) != S.add(fa, call_f(f, b)):
                    h1 = False
                    break
                if call_f(f, R.mul(a, b)) != S.mul(fa, call_f(f, b)):
                    h1 = False
                    break
            if not h1:
                break
    except Exception:
        h1 = False

    try:
        h2 = (call_f(f, R.one) == S.one)
    except Exception:
        h2 = False

    try:
        h3 = is_ideal(Q, S) and is_primary_ideal(Q, S)
    except Exception:
        h3 = False

    try:
        Q_set = set(Q)
        P = [a for a in R.elements if call_f(f, a) in Q_set]
        if not is_ideal(P, R):
            neg_q = True
        else:
            neg_q = not is_primary_ideal(P, R)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S",
    "H_2: f maps the multiplicative identity of R to the multiplicative identity of S",
    "H_3: Q is a primary ideal of S",
    "¬Q: The preimage of Q under f is not a primary ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3