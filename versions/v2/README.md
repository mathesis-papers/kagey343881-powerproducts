# Correction of OEIS A343881, comment 2, revision 16: extensions of Kagey (2015) and Adenwalla (2025)

**Authors:** Haobo Ma, Wenlin Zhang

We correct the conjecture in comment 2 of Peter Kagey's OEIS A343881, revision 16 (June 14, 2021), and extend results of Kagey (2015) and Adenwalla (2025): the proposed value 72 at k=12 is inadmissible for every exponent n>=2. The exact prime-exponent minima are 27, 18, and 54 at p=2,3,5, respectively, and 144 at every prime p>=7. More generally, writing k=r^g with the prime-exponent vector of r having greatest common divisor 1, we prove that T(p,k)=r^(g+1) for all sufficiently large primes, with an explicit threshold. This gives the precise range in which the proposed formula k rad(k) is correct. We also prove the entry's distinct-prime-row assertion and first-column formula using the same valuation description. For the cross-referenced sequence minimum in A343825, we prove eventual equality with A071537 by an explicit determinant bound and reprove Adenwalla's k=12 prime column: 20 at p=2 and 18 at every odd prime. The valuation classes also answer the image questions in Kagey's Open problem collection, Problem 16: they characterize the cube-row image and show that the two-value rows are injective exactly at prime exponents.

- PDF: [frozen public file](paper.pdf)
- License: CC-BY-4.0
- Version: 2
- Mathesis record: [kagey343881-powerproducts](https://mathesis-omega-research.apps.chrono-ai.fun/papers/kagey343881-powerproducts?version=2)

## How to cite

Haobo Ma, Wenlin Zhang (2026). Correction of OEIS A343881, comment 2, revision 16: extensions of Kagey (2015) and Adenwalla (2025). Mathesis, version 2. https://mathesis-omega-research.apps.chrono-ai.fun/papers/kagey343881-powerproducts?version=2

## Statement progress

| Statement | Formalization status | Source | Verification basis |
|---|---|---|---|
| Proposition (s1) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Arith/Factorization/OeisA343881KageyPowerProducts.lean) | No public receipt |
| Corollary (s10) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Arith/Factorization/OeisA343881KageyPowerProducts.lean) | No public receipt |
| Corollary (s11) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Arith/Factorization/OeisA343881KageyPowerProducts.lean) | No public receipt |
| Proposition (s12) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Arith/Factorization/OeisA343881KageyPowerProducts.lean) | No public receipt |
| Theorem (s13) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Arith/Factorization/OeisA343881KageyPowerProducts.lean) | No public receipt |
| Corollary (s14) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Arith/Factorization/OeisA343881KageyPowerProducts.lean) | No public receipt |
| Theorem (s2) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Arith/Factorization/OeisA343881KageyPowerProducts.lean) | No public receipt |
| Corollary (s3) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Arith/Factorization/OeisA343881KageyPowerProducts.lean) | No public receipt |
| Proposition (s4) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Arith/Factorization/OeisA343881KageyPowerProducts.lean) | No public receipt |
| Corollary (s5) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Arith/Factorization/OeisA343881KageyPowerProducts.lean) | No public receipt |
| Corollary (s6) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Arith/Factorization/OeisA343881KageyPowerProducts.lean) | No public receipt |
| Proposition (s7) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Arith/Factorization/OeisA343881KageyPowerProducts.lean) | No public receipt |
| Corollary (s8) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Arith/Factorization/OeisA343881KageyPowerProducts.lean) | No public receipt |
| Corollary (s9) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Arith/Factorization/OeisA343881KageyPowerProducts.lean) | No public receipt |

## Contributions

Original authors are listed above. Formalization contributors and attribution are retained in `formalization/nodes.json`; repository pull requests do not confer verification or credit. Submit formalization attempts through the Mathesis attempt path described in [CONTRIBUTING.md](CONTRIBUTING.md).
