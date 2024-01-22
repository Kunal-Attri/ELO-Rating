# ELO-Rating

In this repo, I created a library which can be re-used to directly implement ELO Rating system in any game.

## Formula to calculate New Rating of a Player

$R^{'}_a = R_a + K * (S_a - E_a)$

$E_a = \frac{1}{1 + 10^{\frac{R_b - R_a}{c}}}$