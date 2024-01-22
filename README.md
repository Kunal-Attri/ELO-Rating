# ELO-Rating

In this repo, I created a library which can be re-used to directly implement ELO Rating system in any game.

## Formula to calculate New Rating of a Player

$$
New\ Rating,\ R^{'}_{a} = R_{a} + K * (S_{a} - E_{a})
\\
Expected\ score,\ E_{a} = \frac{1}{1 + 10 ^ \frac{R_{b} - R_{a}}{c}}
$$
