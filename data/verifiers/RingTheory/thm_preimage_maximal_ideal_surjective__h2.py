import sympy
import math

# Top-level setup
Z = sympy.ZZ
Q = sympy.QQ

def parse_ring(r_str):
    if r_str == 'Z' or r_str is sympy.ZZ:
        return ('Z', 0)
    if r_str == 'Q' or r_str is sympy.QQ:
        return ('Q', 0)
    if isinstance(r_str, str):
        if r_str.startswith('Z/') and r_str.endswith('Z'):
            try:
                n = int(r_str[2:-1])
                return ('Zn', n)
            except ValueError:
                pass
    raise ValueError(f"Unknown ring: {r_str}")

def is_comm_ring_with_id(ring):
    rtype, n = ring
    if rtype in ('Z', 'Q'):
        return True
    if rtype == 'Zn' and n > 1:
        return True
    return False

def get_single_gen(ring, gen):
    rtype, n = ring
    
    def to_int(x):
        try:
            return abs(int(x))
        except Exception:
            return 0
            
    if isinstance(gen, (list, tuple, set)):
        if len(gen) == 0:
            return 0
        if rtype == 'Z':
            g = 0
            for x in gen:
                g = math.gcd(g, to_int(x))
            return g
        if rtype == 'Q':
            for x in gen:
                if x != 0:
                    return 1
            return 0
        if rtype == 'Zn':
            g = n
            for x in gen:
                g = math.gcd(g, to_int(x))
            return g
            
    if rtype in ('Z', 'Zn'):
        return to_int(gen)
    return gen

def is_maximal_ideal(ring, gen):
    rtype, n = ring
    if rtype == 'Z':
        return sympy.isprime(gen)
    if rtype == 'Q':
        return gen == 0
    if rtype == 'Zn':
        g = math.gcd(gen, n)
        return sympy.isprime(g)
    return False

def has_homomorphism(R, S):
    rtype, rn = R
    stype, sn = S
    if rtype == 'Z' and stype == 'Q':
        return True
    if rtype == 'Z' and stype == 'Z':
        return True
    if rtype == 'Z' and stype == 'Zn':
        return True
    if rtype == 'Zn' and stype == 'Zn':
        return (rn % sn) == 0
    if rtype == 'Q' and stype == 'Q':
        return True
    return False

def preimage_ideal_gen(R, S, M_gen):
    rtype, rn = R
    stype, sn = S
    if rtype == 'Z' and stype == 'Q':
        if M_gen == 0:
            return 0
        else:
            return 1
    if rtype == 'Z' and stype == 'Z':
        return M_gen
    if rtype == 'Z' and stype == 'Zn':
        return math.gcd(M_gen, sn)
    if rtype == 'Zn' and stype == 'Zn':
        return math.gcd(M_gen, sn)
    if rtype == 'Q' and stype == 'Q':
        return M_gen
    raise ValueError("Unsupported homomorphism")

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, dict):
            return [False, False, False]
            
        R_str = witness.get('R')
        S_str = witness.get('S')
        
        if R_str is None or S_str is None or 'M_gen' not in witness:
            return [False, False, False]
            
        R = parse_ring(R_str)
        S = parse_ring(S_str)
        
        M_gen = get_single_gen(S, witness['M_gen'])
        
        # H1: R and S are commutative rings with identity
        h1 = is_comm_ring_with_id(R) and is_comm_ring_with_id(S)
        
        # H2: M is a maximal ideal of S
        h2 = is_maximal_ideal(S, M_gen)
        
        # Check if canonical homomorphism exists
        if not has_homomorphism(R, S):
            return [False, False, False]
            
        # Conclusion: f^{-1}(M) is a maximal ideal of R
        pre_gen = preimage_ideal_gen(R, S, M_gen)
        q = is_maximal_ideal(R, pre_gen)
        
        return [bool(h1), bool(h2), not bool(q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: M is a maximal ideal of S",
    "¬Q: The preimage f^{-1}(M) is not a maximal ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2