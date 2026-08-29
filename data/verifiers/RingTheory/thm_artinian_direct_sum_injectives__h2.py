import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

# Standard algebra objects
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

def parse_witness(witness):
    """
    Parses the witness into a tuple (n, m_list) representing the ring R = Z/nZ
    and a list of modules M_i = Z/m_i Z.
    """
    if isinstance(witness, dict):
        n = witness.get('R', witness.get('n', 0))
        m = witness.get('M', witness.get('m', witness.get('M_i', [])))
        if isinstance(n, int) and n > 0:
            if isinstance(m, int):
                return n, [m]
            elif isinstance(m, (list, tuple)):
                return n, [int(x) for x in m if isinstance(x, int)]
    
    ints = []
    def extract(w):
        if isinstance(w, int):
            ints.append(w)
        elif isinstance(w, (list, tuple)):
            for x in w:
                extract(x)
        elif isinstance(w, dict):
            for v in w.values():
                extract(v)
    extract(witness)
    if len(ints) >= 2:
        return ints[0], ints[1:]
    elif len(ints) == 1:
        return ints[0], [ints[0]]
        
    if isinstance(witness, str):
        digits = ''.join(c if c.isdigit() else ' ' for c in witness).split()
        ints = [int(x) for x in digits]
        if len(ints) >= 2:
            return ints[0], ints[1:]
        elif len(ints) == 1:
            return ints[0], [ints[0]]
            
    raise ValueError("Could not parse witness")

def conditions(witness) -> list[bool]:
    try:
        n, m_list = parse_witness(witness)
        
        # H1: R is a right Artinian ring
        # We model R as Z/nZ. It is Artinian if n > 0.
        # We also require M_i to be valid R-modules, meaning m_i divides n.
        h1_ok = (n > 0)
        for m in m_list:
            if m <= 0 or n % m != 0:
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    try:
        if not h1_ok:
            neg_q = False
        else:
            # Conclusion: The direct sum of M_i is an injective right R-module.
            # A direct sum is injective iff each summand is injective.
            # Z/mZ is injective over Z/nZ iff for all primes p dividing m, v_p(m) == v_p(n).
            is_inj = True
            factors_n = factorint(n)
            for m in m_list:
                if m == 1:
                    continue
                factors_m = factorint(m)
                for p, e in factors_m.items():
                    if e != factors_n.get(p, 0):
                        is_inj = False
                        break
                if not is_inj:
                    break
            
            neg_q = not is_inj
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: The direct sum of the modules M_i is not an injective right R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1