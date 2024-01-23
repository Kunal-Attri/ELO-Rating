# ELO-Rating

It is an excellent method for calculating relative skill levels of players represented as numeric values.

## Understanding ELO

- Consider a PvP match b/w two players, player A and player B.
- Player A has ELO rating R<sub>a</sub> and player B has ELO rating R<sub>b</sub>.
- ELO ratings of individual players reflect their relative skill levels based on performance in past matches.
- Now, a player defeating a much weaker player is not the same as defeating a much more stronger player. ELO rating takes this into account and is reflected in updated ratings of both players.
- After each match, ELO rating of both players is updated based on a formula.
- Originally, it only considers the outcome of a match.

## Formula to calculate New Rating of a Player

$$
R^{'}_a = R_a + K \times (S_a - E_a)
$$

where,
<br>
$R^{'}_a: \text{New Rating of player A}$
<br>
$R_a: \text{Original Rating of player A}$
<br>
$K\ : \text{Scaling factor}$
<br>
$S_a: \text{Actual score or outcome of the match}$
<br>
$E_a: \text{Expected score or outcome of the match}$

### Scaling Factor: $K$

- It determines how much influence each match can have on the ELO ratings of the players.
- It can be varied according to matches, leagues, competitions, player rating levels, etc.
- Generally, can be set to $32$.

### Actual score: $S_a$

- Represents whether a player won or lost or drawn the match.
- Generally, it takes one of the three values:
  - $1$ for a win
  - $0$ for a loss
  - $0.5$ for a draw
  - i.e. $S_{a} \in [0, 1]$

### Expected score: $E_a$

- This is where magic of ELO ratings happen.
- It represents the probability that the player will win a match.
- It is calculated based on ELO ratings of two players.
- Formula:

$$
E_a = \frac{Q_a}{Q_a + Q_b}
\text{, where}
\begin{cases}
    Q_a = 10 ^ {R_a / c} \\
    Q_b = 10 ^ {R_b / c} \\
    c = 400 \text{ (generally)}
\end{cases}
$$

On solving  by substituting values of $Q_a$ and $Q_b$,

$$
E_a = \frac{1}{1 + 10 ^ {\frac{R_b - R_a}{c}}} \text{, where } c = 400$$

$\therefore E_a \in [0, 1]$


- As $0 \leq S_a \leq 1$ and $0 \leq E_a \leq 1$, maximum change in a player's rating can be $K$.

### Initial ELO Rating

- It is the rating that a new player has when he starts playing the game.
- It must be significantly larger than $K$ factor, to allow a player to play, and lose enough matches before eventually winning matches, so that his ELO rating would finally start rising up.
- Generally, can be 1000.

## Considering Points
