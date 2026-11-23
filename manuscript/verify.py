import hashlib
import json
from functools import lru_cache
from fractions import Fraction
from itertools import product
from math import gcd, prod


@lru_cache(maxsize=20000)
def factor(number):
    assert number >= 1
    factors = []
    divisor = 2
    while divisor * divisor <= number:
        multiplicity = 0
        while number % divisor == 0:
            number //= divisor
            multiplicity += 1
        if multiplicity:
            factors.append((divisor, multiplicity))
        divisor += 1
    if number > 1:
        factors.append((number, 1))
    return tuple(factors)


def is_prime(number):
    return number > 1 and factor(number) == ((number, 1),)


def valuation_witness(exponent, left, right):
    left_factors = dict(factor(left))
    right_factors = dict(factor(right))
    coordinates = tuple(
        (left_factors.get(prime, 0), right_factors.get(prime, 0))
        for prime in left_factors.keys() | right_factors.keys()
    )
    for first in range(1, exponent):
        for second in range(1, exponent):
            if all((first * source + second * target) % exponent == 0
                   for source, target in coordinates):
                root = prod(
                    prime ** ((first * left_factors.get(prime, 0)
                               + second * right_factors.get(prime, 0)) // exponent)
                    for prime in left_factors.keys() | right_factors.keys()
                )
                assert left ** first * right ** second == root ** exponent
                return first, second, root
    return None


def minimum(exponent, start, bound):
    for candidate in range(start + 1, bound + 1):
        witness = valuation_witness(exponent, start, candidate)
        if witness is not None:
            return candidate, witness
    raise AssertionError((exponent, start, bound))


def signature(prime, number):
    residues = tuple((base, multiplicity % prime)
                     for base, multiplicity in factor(number)
                     if multiplicity % prime)
    if not residues:
        return ()
    inverse = pow(residues[0][1], -1, prime)
    return tuple((base, residue * inverse % prime) for base, residue in residues)


def prime_minimum(prime, start, bound):
    target = signature(prime, start)
    for candidate in range(start + 1, bound + 1):
        if signature(prime, candidate) == target:
            return candidate
    raise AssertionError((prime, start, bound))


def corrected(number):
    exponents = [multiplicity for _, multiplicity in factor(number)]
    common = 0
    for multiplicity in exponents:
        common = gcd(common, multiplicity)
    primitive = prod(base ** (multiplicity // common)
                     for base, multiplicity in factor(number))
    return number * primitive, common, max(exponents)


def exact_root(number, exponent):
    lower = 1
    upper = 1 << ((number.bit_length() + exponent - 1) // exponent)
    while lower <= upper:
        middle = (lower + upper) // 2
        power = middle ** exponent
        if power == number:
            return middle
        if power < number:
            lower = middle + 1
        else:
            upper = middle - 1
    return None


def direct_witness(exponent, left, right):
    for first in range(1, exponent):
        for second in range(1, exponent):
            root = exact_root(left ** first * right ** second, exponent)
            if root is not None:
                return first, second, root
    return None


def floor_root(number, exponent):
    lower = 0
    upper = 1 << ((number.bit_length() + exponent - 1) // exponent)
    while lower < upper:
        middle = (lower + upper + 1) // 2
        if middle ** exponent <= number:
            lower = middle
        else:
            upper = middle - 1
    return lower


def residue_formula(prime, start):
    candidates = []
    for scalar in range(1, prime):
        representative = prod(base ** (scalar * multiplicity % prime)
                              for base, multiplicity in factor(start))
        multiplier = floor_root(start // representative, prime) + 1
        candidates.append(representative * multiplier ** prime)
    return min(candidates)


def least_class_member(prime, number):
    return min(prod(base ** (scalar * multiplicity % prime)
                    for base, multiplicity in factor(number))
               for scalar in range(1, prime))


def cube_image(number):
    first = prod(base for base, multiplicity in factor(number) if multiplicity % 3 == 1)
    second = prod(base for base, multiplicity in factor(number) if multiplicity % 3 == 2)
    cube_part = prod(base ** (multiplicity // 3) for base, multiplicity in factor(number))
    return cube_part > 1 or first < second


def reduce_vector(vector, basis, prime):
    if prime:
        remaining = {base: value % prime for base, value in vector.items() if value % prime}
    else:
        remaining = {base: Fraction(value) for base, value in vector.items() if value}
    while remaining:
        pivot = min(remaining)
        if pivot not in basis:
            break
        scalar = remaining[pivot]
        for base, value in basis[pivot].items():
            updated = remaining.get(base, 0) - scalar * value
            if prime:
                updated %= prime
            if updated:
                remaining[base] = updated
            else:
                remaining.pop(base, None)
    return remaining


def sequence_minimum(prime, start, bound):
    if start in (0, 1):
        return start
    target = dict(factor(start))
    basis = {}
    if not reduce_vector(target, basis, prime):
        return start
    for endpoint in range(start + 1, bound + 1):
        remaining = reduce_vector(dict(factor(endpoint)), basis, prime)
        if remaining:
            pivot = min(remaining)
            inverse = pow(remaining[pivot], -1, prime) if prime else 1 / remaining[pivot]
            basis[pivot] = {base: (value * inverse % prime if prime else value * inverse)
                            for base, value in remaining.items()}
        if not reduce_vector(target, basis, prime):
            return endpoint
    return None


def direct_sequence(exponent, start, endpoint):
    for first in range(1, exponent):
        for multiplicities in product(range(exponent), repeat=endpoint - start):
            value = start ** first
            for number, multiplicity in zip(range(start + 1, endpoint + 1), multiplicities):
                value *= number ** multiplicity
            if exact_root(value, exponent) is not None:
                return True
    return False


def main():
    expected_table = {
        2: [4, 8, 12, 9, 20, 24, 28, 18, 16, 40],
        3: [8, 4, 9, 16, 25, 36, 49, 27, 24, 80],
        4: [4, 4, 9, 8, 20, 24, 28, 18, 12, 40],
        5: [32, 4, 9, 8, 25, 36, 49, 16, 27, 100],
        6: [4, 4, 9, 8, 20, 24, 28, 9, 16, 40],
        7: [128, 4, 9, 8, 25, 36, 49, 16, 27, 100],
        8: [4, 4, 9, 8, 20, 24, 28, 16, 12, 40],
        9: [8, 4, 9, 8, 25, 36, 49, 16, 24, 80],
        10: [4, 4, 9, 8, 20, 24, 28, 16, 16, 40],
        11: [2048, 4, 9, 8, 25, 36, 49, 16, 27, 100],
    }
    for exponent, row in expected_table.items():
        assert [minimum(exponent, start, max(row))[0]
                for start in range(1, 11)] == row

    prime_column = []
    for prime in range(2, 48):
        if is_prime(prime):
            value, witness = minimum(prime, 12, 144)
            expected = {2: 27, 3: 18, 5: 54}.get(prime, 144)
            assert value == expected
            assert value == prime_minimum(prime, 12, 144)
            prime_column.append({"prime": prime, "minimum": value,
                                 "x": witness[0], "y": witness[1], "c": witness[2]})

    obstruction = [exponent for exponent in range(2, 61)
                   if valuation_witness(exponent, 12, 72) is not None]
    assert obstruction == []

    direct_cases = 0
    for exponent in range(2, 8):
        for candidate in range(13, 145):
            direct = direct_witness(exponent, 12, candidate)
            modular = valuation_witness(exponent, 12, candidate)
            assert (direct is not None) == (modular is not None)
            direct_cases += 1

    agreement_cases = 0
    for prime in [2, 3, 5, 7]:
        for start in range(1, 21):
            for candidate in range(start + 1, 61):
                assert (signature(prime, start) == signature(prime, candidate)) == (
                    valuation_witness(prime, start, candidate) is not None)
                agreement_cases += 1

    formula_cases = 0
    formula_threshold_cases = 0
    differences = []
    for start in range(2, 101):
        value, common, largest = corrected(start)
        radical_value = start * prod(base for base, _ in factor(start))
        assert (value == radical_value) == (len({entry[1] for entry in factor(start)}) == 1)
        if value != radical_value:
            differences.append(start)
        for prime in [31, 37, 41, 43]:
            logarithm_bound = value.bit_length() - 1
            if prime > max(common + 1, largest * logarithm_bound):
                formula_threshold_cases += 1
            assert prime_minimum(prime, start, value) == value
            formula_cases += 1
    assert differences[0] == 12

    distinct_rows = []
    for prime in [2, 3, 5, 7, 11, 13]:
        values = [2 ** prime]
        for start in range(2, 101):
            values.append(prime_minimum(prime, start, start * 2 ** prime))
        assert len(set(values)) == len(values)
        distinct_rows.append(prime)

    closed_formula_cases = 0
    for prime in distinct_rows:
        for start in range(1, 101):
            value = residue_formula(prime, start)
            assert value == prime_minimum(prime, start, value)
            closed_formula_cases += 1

    expected_sequence_rows = {
        2: [0, 1, 6, 8, 4, 10, 12, 14, 15, 9, 18],
        3: [0, 1, 4, 6, 9, 10, 12, 14, 8, 16, 15],
        5: [0, 1, 4, 6, 8, 10, 9, 14, 12, 15, 16],
        7: [0, 1, 4, 6, 8, 10, 9, 14, 12, 15, 16],
    }
    for prime, row in expected_sequence_rows.items():
        assert [sequence_minimum(prime, start, max(row))
                for start in range(11)] == row

    exhaustive_cases = 0
    for prime in [2, 3, 5]:
        for start in range(2, 9):
            for endpoint in range(start, start + 5):
                assert (sequence_minimum(prime, start, endpoint) is not None) == (
                    direct_sequence(prime, start, endpoint))
                exhaustive_cases += 1

    expected_rational = [
        1, 4, 6, 8, 10, 9, 14, 12, 15, 16, 22, 18, 26, 21, 20, 24, 34, 25,
        38, 27, 28, 33, 46, 30, 32, 39, 35, 36, 58, 40, 62, 42, 44, 51, 45,
        48, 74, 57, 52, 49, 82, 50, 86, 55, 54, 69, 94, 56, 60, 63, 68, 65,
        106, 64, 66, 70, 76, 87, 118, 72, 122, 93, 75, 77, 78, 80, 134, 85,
        92, 84, 142, 81, 146, 111, 88, 95, 90, 91, 158, 96, 98,
    ]
    rational_values = [sequence_minimum(None, start, start * start)
                       for start in range(1, 101)]
    assert rational_values[:len(expected_rational)] == expected_rational
    assert all(value is not None for value in rational_values)
    assert len(set(rational_values)) == len(rational_values)
    for prime in distinct_rows:
        values = [sequence_minimum(prime, start, max(64, start * start))
                  for start in range(101)]
        assert all(value is not None for value in values)
        assert len(set(values)) == len(values)
        assert {value for value in values if value <= 100} == {
            value for value in range(101) if not is_prime(value)}

    sequence_column = []
    for prime in range(2, 100):
        if is_prime(prime):
            value = sequence_minimum(prime, 12, 20)
            assert value == (20 if prime == 2 else 18)
            sequence_column.append({'prime': prime, 'minimum': value})
    assert rational_values[11] == 18
    assert 12 ** 8 == 16 ** 3 * 18 ** 4
    assert 12 * 15 * 20 == 60 ** 2

    eventual_sequence_cases = 0
    for start in range(2, 31):
        for prime in [101, 103, 107, 109]:
            assert sequence_minimum(prime, start, rational_values[start - 1]) == (
                rational_values[start - 1])
            eventual_sequence_cases += 1

    strict_cases = 0
    for start in range(1, 101):
        assert sequence_minimum(2, start, max(64, start * start)) < residue_formula(2, start)
        strict_cases += 1

    image_cases = 0
    for prime in [2, 3, 5, 7]:
        seen = set()
        for number in range(1, 501):
            normalized = signature(prime, number)
            assert (normalized in seen) == (number > least_class_member(prime, number))
            if all(multiplicity == 1 for base, multiplicity in factor(number)):
                assert normalized not in seen
            seen.add(normalized)
            image_cases += 1

    cube_image_values = [number for number in range(1, 5185) if cube_image(number)]
    assert len(cube_image_values) == 1000
    for number in range(1, 5185):
        assert cube_image(number) == (number > least_class_member(3, number))
    cube_digest = hashlib.sha256(json.dumps(cube_image_values, separators=(',', ':')).encode()).hexdigest()
    assert cube_digest == '88930276b20976452d0f052c73cfa4f6211855f71231b00bfd8726324f4a91c7'
    assert residue_formula(3, 11) == 88
    assert not cube_image(1)
    for number in range(2, 101):
        assert cube_image(number ** 2) and cube_image(number ** 3)

    composite_collisions = []
    for exponent in range(4, 51):
        if not is_prime(exponent):
            smallest = factor(exponent)[0][0]
            start = 2 ** (smallest - 1)
            endpoint = 2 ** smallest
            assert minimum(exponent, 1, endpoint)[0] == endpoint
            assert minimum(exponent, start, endpoint)[0] == endpoint
            composite_collisions.append({'exponent': exponent, 'start': start, 'common_minimum': endpoint})

    result = {
        "status": "PASS",
        "method": "exact integer factorization and valuation congruences; independent integer-root comparison",
        "table": {"n_min": 2, "n_max": 11, "k_min": 1, "k_max": 10,
                  "entries": 100, "matched": True},
        "k12_prime_column": prime_column,
        "k12_m72": {"n_min": 2, "n_max": 60, "admissible_exponents": obstruction},
        "integer_root_comparison": {"n_min": 2, "n_max": 7, "k": 12,
                                    "m_min": 13, "m_max": 144, "cases": direct_cases},
        "prime_signature_comparison": {"primes": [2, 3, 5, 7], "k_min": 1,
                                       "k_max": 20, "m_max": 60, "cases": agreement_cases},
        "corrected_formula": {"k_min": 2, "k_max": 100, "primes": [31, 37, 41, 43],
                              "cases": formula_cases,
                              "cases_above_sufficient_threshold": formula_threshold_cases,
                              "different_from_k_radical": differences},
        "distinct_row_prefixes": {"primes": distinct_rows, "k_min": 1, "k_max": 100},
        "fixed_prime_formula": {"primes": distinct_rows, "k_min": 1, "k_max": 100,
                                "cases": closed_formula_cases},
        "sequence_source_table": {"primes": list(expected_sequence_rows),
                                  "k_min": 0, "k_max": 10, "entries": 44},
        "sequence_integer_root_comparison": {"primes": [2, 3, 5], "k_min": 2,
                                             "k_max": 8, "endpoint_offsets": [0, 1, 2, 3, 4],
                                             "cases": exhaustive_cases},
        "rational_relation_minimum": {"k_min": 1, "k_max": 100,
                                      "source_terms_compared": len(expected_rational),
                                      "values": rational_values},
        "sequence_bijection_prefix": {"primes": distinct_rows, "k_min": 0, "k_max": 100,
                                       "all_nonprime_images_through": 100},
        "sequence_k12_prime_column": sequence_column,
        "sequence_eventual_equality": {"k_min": 2, "k_max": 30,
                                       "primes": [101, 103, 107, 109],
                                       "cases": eventual_sequence_cases},
        "strict_square_comparison": {"k_min": 1, "k_max": 100, "cases": strict_cases},
        "prime_image_criterion": {"primes": [2, 3, 5, 7], "m_min": 1, "m_max": 500,
                                  "predecessor_comparisons": image_cases},
        "cube_image": {"source_url": "https://oeis.org/A299117/b299117.txt",
                       "source_terms_compared": 1000, "last_source_value": 5184,
                       "values_json_sha256": cube_digest, "criterion_cases": 5184,
                       "square_and_cube_bases": [2, 100], "prime_11_minimum": 88},
        "composite_row_collisions": composite_collisions,
        "scope": "Finite checks corroborate the written proofs; the all-input statements are proved in note.tex."
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
