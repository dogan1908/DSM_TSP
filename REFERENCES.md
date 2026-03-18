# References

All references cited in the DSM paper, with context for how each relates to this work.

---

## Core TSP Literature

**[1] Applegate, D. L., Bixby, R. E., Chvátal, V., & Cook, W. J. (2006).**
*The Traveling Salesman Problem: A Computational Study.*
Princeton University Press.
— The definitive computational reference for TSP. Provides context for why TSP heuristics matter and how they are evaluated.

**[2] Karp, R. M. (1972).**
Reducibility among combinatorial problems.
In R. E. Miller & J. W. Thatcher (Eds.), *Complexity of Computer Computations* (pp. 85–103). Plenum Press.
— Proved NP-hardness of the Hamiltonian cycle problem, implying NP-hardness of TSP. Motivates the need for heuristics.

---

## TSP Algorithms Compared in This Paper

**[3] Christofides, N. (1976).**
Worst-case analysis of a new heuristic for the travelling salesman problem.
Technical Report 388, Graduate School of Industrial Administration, Carnegie Mellon University.
— The classical 3/2-approximation algorithm. Uses minimum spanning tree + minimum-weight perfect matching. Requires full O(N²) distance matrix with sqrt. DSM comparison: both use matching, but Christofides matches globally (odd-degree vertices) while DSM matches locally (antiparallel doors).

**[4] Serdyukov, A. I. (1978).**
On some extremal walks in graphs (in Russian).
*Upravlyaemye Sistemy*, 17, 76–79.
— Independent discovery of the Christofides algorithm in the USSR. Submitted January 1976, published 1978.

**[5] Lin, S., & Kernighan, B. W. (1973).**
An effective heuristic algorithm for the traveling-salesman problem.
*Operations Research*, 21(2), 498–516.
— The Lin-Kernighan heuristic, basis for the LKH solver. Produces near-optimal tours but requires full distance computation. Potential hybrid partner for DSM (DSM matching as warm start for LK optimization).

**[6] Croes, G. A. (1958).**
A method for solving traveling-salesman problems.
*Operations Research*, 6(6), 791–812.
— Introduced the 2-opt local search improvement. Used in DSM's final tour optimization phase. One of the oldest and most robust TSP improvement methods.

**[7] Held, M., & Karp, R. M. (1962).**
A dynamic programming approach to sequencing problems.
*Journal of the Society for Industrial and Applied Mathematics*, 10(1), 196–210.
— The Held-Karp algorithm for exact TSP solution via dynamic programming. O(N² · 2^N) time. Used in our benchmarks as the ground-truth optimal solution for N ≤ 20.

---

## Directional and Sparse TSP Methods

**[8] Gillett, B. E., & Miller, L. R. (1974).**
A heuristic algorithm for the vehicle-dispatch problem.
*Operations Research*, 22(2), 340–349.
— The Sweep algorithm for vehicle routing. Groups cities by polar angle (arctan) relative to a central depot. Conceptually related to DSM's lighthouse concept: both use a reference point for global context. Key difference: Sweep computes arctan; DSM uses Compass16 (integer-only).

**[9] Gao, L., Chen, M., Chen, Q., Luo, G., Zhu, N., & Liu, Z. (2023).**
ELG: An efficient local-global framework for the traveling salesman problem.
In *Proceedings of IJCAI 2023*.
— Uses polar coordinate features in k-nearest-neighbor graphs for neural TSP solving. Shares DSM's philosophy of local, directional, sparse representations. Key differences: ELG requires trigonometric features, GPU inference, and millions of training samples. DSM is deterministic, training-free, and integer-only.

**[10] Hudson, B., Li, Q., Malencia, M., & Prorok, A. (2022).**
Graph neural network guided local search for the traveling salesperson problem.
*arXiv preprint arXiv:2110.05291*.
— Constructs sparse k-NN TSP graphs to reduce GNN input size. DSM follows the same sparsification principle (k=3 edges per city) but adds antiparallel matching and lighthouse filtering as novel mechanisms.

---

## Hardware Reference

**[11] Microchip Technology (2021).**
*AVR Instruction Set Manual.*
Document DS40002198.
— Reference for cycle counts on ATmega328 and similar 8-bit AVR microcontrollers. Used to estimate DSM vs NN wall-clock performance on integer-only hardware. Key data points: integer multiply = 1–2 cycles, software sqrt (Newton, 8 iterations) ≈ 50–100 cycles.

---

## Additional Context (Not Cited in Paper)

**Stanĕk, R., Greistorfer, P., Ladner, K., & Pferschy, U. (2019).**
Geometric and LP-based heuristics for angular travelling salesman problems in the plane.
*Computers & Operations Research*, 108, 15–32.
— Angular TSP: minimizes total turning angle rather than distance. Different problem formulation but uses geometric/angular reasoning. Not directly comparable to DSM.

**Gutin, G., & Punnen, A. P. (Eds.) (2007).**
*The Traveling Salesman Problem and Its Variations.*
Springer.
— Comprehensive reference covering TSP variants, heuristics, and exact methods. General background.

**Karlin, A., Klein, N., & Oveis Gharan, S. (2021).**
A (slightly) improved approximation algorithm for metric TSP.
In *Proceedings of the 53rd Annual ACM Symposium on Theory of Computing (STOC)*.
— Improved Christofides' ratio from 3/2 to 3/2 − 10⁻³⁶. Theoretical breakthrough but not practically relevant for embedded systems.
