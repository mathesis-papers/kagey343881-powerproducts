# Correction of OEIS A343881, comment 2, revision 16

Extensions and alternative proofs of related results of Kagey (2015) and
Adenwalla (2025).

Haobo Ma (ChronoAI Pte Ltd, Singapore); Wenlin Zhang (National University of
Singapore; ChronoAI Pte Ltd, Singapore). November 9, 2026.

For the table in [OEIS A343881](https://oeis.org/A343881), comment 2 of revision 16,
the proposed eventual value is false. At k=12, 72 is inadmissible for every n>=2.
The prime-exponent minima are 27, 18, and 54 at primes 2, 3, and 5, and 144 at every
prime p>=7. For general k=r^g with primitive prime-exponent vector for r, the
eventual minimum is kr, with the explicit bound proved in the note.
For A343825's arbitrary-sequence minimum S(p,k), the eventual value is
A071537(k), with an explicit determinant bound. At k=12 the exact value is
20 for p=2 and 18 for every odd prime, reproving Adenwalla's 2025 Appendix,
item 8. The note credits Alekseyev's 2008
rational-permutation proof, Kagey's 2015 square-row results, Hoft and Corneth's
2016 cube formula and proof, Rajesh and Kagey--Rajesh's 2024 strict square
comparison, and Adenwalla's 2025 prime-row permutation theorem.
The two-value rows are injective exactly for prime exponents. For m=AB^2t^3,
with A,B coprime squarefree and t>=1, A299117 consists exactly of those m
with t>1 or A<B. This answers the image, square and squarefree questions in
Kagey's Open problem collection, Problem 16, with 1 explicitly excluded.

## Contents

- `note.tex`: self-contained statements, proofs, coverage table, and references.
- `metadata.json`: bibliographic metadata and the two covered problem identifiers.
- `verify.py`: exact finite tests, using the Python standard library.
- `scientific-checks.json`: expected output of those tests.
- `README.md`: build and checking instructions.

## Build

Use Tectonic 0.17.0:

```sh
tectonic --untrusted note.tex
```

Alternatively, run `pdflatex note.tex` twice. The bibliography is embedded in
`note.tex`; BibTeX and external bibliography files are unnecessary. Required TeX
packages are geometry, amsmath, amssymb, amsthm, booktabs, array, longtable, fontenc, lmodern,
hyperref, and xurl. The source archive contains all document inputs.

## Finite checks

Requires Python 3.8 or later. No third-party Python packages are required.

```sh
python3 verify.py > actual-checks.json
cmp scientific-checks.json actual-checks.json
```

The output has `status: PASS`. Its ranges are finite: 100 table entries, all
prime exponents below 48 at k=12, the m=72 obstruction for 2<=n<=60, 396
corrected-formula cases, six prime-row prefixes, and agreement tests against
integer roots and projective valuation classes. Additional tests cover 600
fixed-prime formula cases, 44 displayed prime-row entries of A343825, 105
exhaustive small multiplicity comparisons, its k=12 column at all 25 primes
below 100, 81 published terms of A071537, six sequence-permutation prefixes,
116 eventual sequence-equality cases, and 100 strict square-comparison cases.
The 116 sequence-equality cases are finite corroboration, not applications
of the explicit bound. Universal statements have complete proofs in the note.
Image tests compare 2000 finite predecessor cases and the 1000 published
terms in https://oeis.org/A299117/b299117.txt against the cube-image criterion.
The source comparison uses the SHA-256 of the compact JSON array of those
1000 values. Every composite exponent through 50 has its explicit row
collision checked. The square and cube assertions are checked for bases 2..100.

## Lean statement

The pinned declaration `result` in
[OeisA343881KageyPowerProducts.lean](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Arith/Factorization/OeisA343881KageyPowerProducts.lean)
proves the negation of A343881's eventual-equality claim. The pinned declaration
`result` in
[OeisA343825KageyPowerSequences.lean](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Arith/Factorization/OeisA343825KageyPowerSequences.lean)
proves A343825's eventual equality with A071537 for k>=1. The explicit bounds,
corrected two-value formula, exact prime columns, row assertions, residue
formula, and first-column identity have the written proofs in `note.tex`.

## License

CC BY 4.0 (`cc-by-4.0`).
https://creativecommons.org/licenses/by/4.0/
