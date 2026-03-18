# Directional Sparse Matching (DSM)

**A Trigonometry-Free TSP Heuristic for Embedded Systems**

*Dogan Balban — March 2026*

---

## What is DSM?

DSM is a heuristic for the Travelling Salesman Problem (TSP) that uses **exclusively integer arithmetic** — no square root, no arctan, no sin/cos, no floating-point operations at any stage.

Each city stores 3 nearest-neighbor squared distances and discrete 16-point compass directions, plus lighthouse reference signatures. Neighbors are discovered via an *antiparallel matching rule*: equal squared distance + opposite compass direction = candidate pair.

## Why?

Classical TSP heuristics (Nearest Neighbor, Christofides, Lin-Kernighan) require `sqrt()` for every distance evaluation. On a modern CPU this costs nanoseconds. But on hardware **without floating-point units** — 8-bit microcontrollers, FPGAs, sensor nodes, low-power drones — a single `sqrt()` costs 50–100 CPU cycles via software emulation.

DSM eliminates all such calls. The entire pipeline runs in integer addition, subtraction, multiplication by two fixed constants, and comparison.

## Honest Assessment

| Claim | Status |
|---|---|
| No trigonometry or sqrt | **True** — at any stage |
| Faster than Nearest Neighbor | **True on integer-only hardware** (4–5× fewer cycles per edge). No advantage on CPUs with FPU. |
| Better tour quality | **False** — tours are 1–7% longer than NN |
| Fewer comparisons | **False** — Phase 1 (k-NN search) is O(N²), same as NN |
| Novel matching principle | **True** — antiparallel compass matching with lighthouse filtering is not described in prior TSP literature |

## Key Results

| N | DSM vs Optimum | DSM vs NN | MCU Speedup |
|---|---|---|---|
| 10–20 | +1–7% (Held-Karp) | +1–7% | 4.4× |
| 100 | est. +7–12% | +7.2% | 4.4× |
| 300 | est. +5–10% | +4.4% | 4.4× |

Matching precision: 97–100% up to N=500 with 2 lighthouses.

## The Core Idea

```
For each city:
  → Find 3 nearest neighbors using d² (no sqrt needed)
  → Classify direction to each neighbor via Compass16:
      if |Δx| < |Δy| × 0.199  →  N or S
      if |Δx| < |Δy| × 0.668  →  NNE/NNW/SSE/SSW
      else                      →  NE/NW/SE/SW
      (symmetric for horizontal case)
  → Store: 3 × (d², compass direction) + 2 × lighthouse signature
  → Total: 10 integer values per city

Matching:
  → Two cities are neighbors if their doors have:
      equal d² (±2%) AND opposite compass direction (NE ↔ SW)
  → Lighthouse filter: both cities must see each reference point
      from similar direction and distance

Tour:
  → Build chains from matches → merge chains → 2-opt
```

## Target Hardware

- **8/16-bit MCUs** (ATmega328, MSP430, PIC) — no FPU available
- **FPGAs/ASICs** — Compass16 is a combinational circuit (~200 LUTs)
- **Low-power drones** — battery-constrained, every cycle costs energy
- **Sensor networks** — each node knows only local neighbors

## Repository Contents

```
├── README.md              This file
├── LICENSE                MIT License
├── paper/
│   ├── DSM_Balban2026.pdf   The paper (LaTeX compiled)
│   └── DSM_Balban2026.tex   LaTeX source
├── src/
│   └── dsm.py             Reference implementation (Python)
├── benchmarks/
│   └── run_benchmarks.py  Reproduce all paper results
└── REFERENCES.md          Full reference list
```

## Quick Start

```python
python src/dsm.py --cities 100 --seed 42
```

## DOI

[![DOI](https://zenodo.org/badge/DOI/YOUR_DOI_HERE.svg)](https://doi.org/YOUR_DOI_HERE)

> Replace `YOUR_DOI_HERE` with the actual DOI after Zenodo upload.

## Citation

If you use DSM in your research, please cite:

```
Balban, D. (2026). Trigonometry-Free TSP Heuristics for Embedded Systems:
A Compass-Based Matching Approach. Working Paper. DOI: YOUR_DOI_HERE
```

BibTeX:
```bibtex
@techreport{Balban2026DSM,
  author    = {Balban, Dogan},
  title     = {Trigonometry-Free {TSP} Heuristics for Embedded Systems:
               A Compass-Based Matching Approach},
  year      = {2026},
  month     = {March},
  type      = {Working Paper},
  doi       = {10.5281/zenodo.19096781}
}
```

## Contributing

DSM is a working paper. Known areas for improvement:

- Tour quality gap (currently 1–7% below NN)
- Phase 1 acceleration (grid hashing, kd-trees)
- 32-point compass for higher precision at large N
- Hybrid approaches (DSM matching + Lin-Kernighan optimization)
- Hardware implementation (FPGA prototype, MCU benchmark)

Pull requests and discussions welcome.

## License

MIT License — see [LICENSE](LICENSE)
