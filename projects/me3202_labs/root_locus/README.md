# Lab 9 study: closed-loop poles and root locus

**Gajendra | 2301ME18 | ME3202, IIT Patna**

The Lab 9 manual starts with `G(s) = 1/(s² + 3s + 2)`. For unity negative feedback with proportional gain `K`, the closed-loop characteristic equation is `s² + 3s + (2 + K) = 0`. This script calculates both poles as `K` changes. It is an analytical study, not an experimental measurement.

```bash
python projects/me3202_labs/root_locus/root_locus_demo.py
python projects/me3202_labs/root_locus/tests/test_root_locus_demo.py
```

Open `results/root_locus.csv` in Excel or MATLAB and plot real versus imaginary pole position. At `K = 0`, the poles are -1 and -2. At `K = 0.25`, they meet at -1.5. For larger positive gain, they form a complex-conjugate pair with real part -1.5.
