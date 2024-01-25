/**
 * Class intended for ELO Rating use in multiple scenarios
 */
public class ELO {
    private final int K_FACTOR;
    private static final int DEFAULT_K_FACTOR = 32;
    private final int C_VALUE;
    private static final int DEFAULT_C_VALUE = 400;
    private final int L_FACTOR;
    private static final int DEFAULT_L_FACTOR = 16;
    private static final int DEFAULT_METHOD = 2;
    
    // Outcomes
    public static final int DRAW = 0;
    public static final int PLAYER_A_WON = 1;
    public static final int PLAYER_B_WON = 2;

    /**
     * Constructor with all default values
     */
    public ELO() {
        this(DEFAULT_K_FACTOR, DEFAULT_C_VALUE, DEFAULT_L_FACTOR);
    }

    /**
     * @param k_factor K-factor
     */
    public ELO(int k_factor) {
        this(k_factor, DEFAULT_C_VALUE, DEFAULT_L_FACTOR);
    }

    /**
     * @param k_factor K-factor
     * @param c_value c-factor
     */
    public ELO(int k_factor, int c_value) {
        this(k_factor, c_value, DEFAULT_L_FACTOR);
    }

    /**
     * @param k_factor K-factor
     * @param c_value c-factor
     * @param l_factor L-factor
     */
    public ELO(int k_factor, int c_value, int l_factor) {
        K_FACTOR = k_factor;
        C_VALUE = c_value;
        L_FACTOR = l_factor;
    }

    /**
     * @param rating_a Current rating of player A
     * @param rating_b Current rating of player B
     * @param outcome Outcome of the match
     * @return New ratings of the two players
     */
    public double[] elo(double rating_a, double rating_b, int outcome) {
        if (outcome == ELO.DRAW) {
            return this.elo_scores(rating_a, rating_b, 0.5, 0.5);
        } else if (outcome == ELO.DRAW) {
            return this.elo_scores(rating_a, rating_b, 1, 0);
        } else if (outcome == ELO.DRAW) {
            return this.elo_scores(rating_a, rating_b, 0, 1);
        } else {
            // Invalid Outcome given
            System.out.println("Invalid outcome given. Refer deocumentation on github for more details.");
            return new double[] {rating_a, rating_b};
        }
    }

    /**
     * @param rating_a Current rating of player A
     * @param rating_b Current rating of player B
     * @param score_a Outcome of game for player A
     * @param score_b Outcome of game for player B
     * @return New ratings of the two players
     */
    private double[] elo_scores(double rating_a, double rating_b, double score_a, double score_b) {

        // Check if scores and valid
        if  (!valid_scores(score_a, score_b)) {
            System.out.println("Scores not valid");
            return new double[]{rating_a, rating_b};
        }

        // Expected scores of the players
        double[] expected_scores = this.get_expected_scores(rating_a, rating_b);
        double expected_score_a = expected_scores[0];
        double expected_score_b = expected_scores[1];

        // New ratings of the players
        double new_rating_a = this.update(rating_a, score_a, expected_score_a);
        double new_rating_b = this.update(rating_b, score_b, expected_score_b);

        return new double[] {new_rating_a, new_rating_b};
    }

    /**
     * @param rating_a Current rating of player A
     * @param rating_b Current rating of player B
     * @param points_a Points scored by player A
     * @param points_b Points scored by player B
     * @param method Whether to rationalize points or use L factor
     * @return New ratings of the two players
     */
    public double[] elo_with_points(double rating_a, double rating_b, double points_a, double points_b, int method) {
        if (method == 0) {
            return this.elo_outcome_points(rating_a, rating_b, points_a, points_b);
        } else if (method == 1) {
            return this.elo_rationalize_points(rating_a, rating_b, points_a, points_b);
        } else if (method == 2) {
            return this.elo_with_l_factor(rating_a, rating_b, points_a, points_b);
        } else {
            // Invalid method given
            System.out.println("Invalid method given");
            return new double[] {rating_a, rating_b};
        }
    }

    private double[] elo_outcome_points(double rating_a, double rating_b, double points_a, double points_b) {
        double[] scores = this.get_scores(points_a, points_b);
        return this.elo_scores(rating_a, rating_b, scores[0], scores[1]);
    }

    /**
     * @param rating_a Current rating of player A
     * @param rating_b Current rating of player B
     * @param points_a Points scored by player A
     * @param points_b Points scored by player B
     * @return New ratings of the two players
     */
    private double[] elo_rationalize_points (double rating_a, double rating_b, double points_a, double points_b) {
        double score_a, score_b;

        if (points_a == points_b && points_b == 0){
            // Both players got zero points
            score_a = 0.5;
            score_b = 0.5;
        } else {
            // Not zero points
            score_a = points_a / (points_a + points_b);
            score_b = points_b / (points_a + points_b);
        }

        return this.elo_scores(rating_a, rating_b, score_a, score_b);
    }

    /**
     * @param rating_a Current rating of player A
     * @param rating_b Current rating of player B
     * @param points_a Points scored by player A
     * @param points_b Points scored by player B
     * @return New ratings of the two players
     */
    private double[] elo_with_l_factor (double rating_a, double rating_b, double points_a, double points_b) {
        // Get actual scores
        double[] scores = this.get_scores(points_a, points_b);
        double score_a = scores[0];
        double score_b = scores[1];

        // Get expected scores
        double[] expected_scores = this.get_expected_scores(rating_a, rating_b);
        double expected_a = expected_scores[0];
        double expected_b = expected_scores[1];

        // Calculating new ratings based on outcome
        double[] new_ratings = this.elo_scores(rating_a, rating_b, score_a, score_b);
        double new_rating_a = new_ratings[0];
        double new_rating_b = new_ratings[1];

        // Calculating p value
        double p_a = this.p(score_a, expected_a);
        double p_b = this.p(score_b, expected_b);

        // Adding L factor calculation for extra points
        new_rating_a += p_a * this.L_FACTOR * this.points_fraction(points_a, points_b);
        new_rating_b += p_b * this.L_FACTOR * this.points_fraction(points_b, points_a);

        return new double[] {new_rating_a, new_rating_b};
    }

    /**
     * @param score_a Outcome of match for player A
     * @param score_b Outcome of match for player B
     * @return whether the scores are valid
     */
    private boolean valid_scores(double score_a, double score_b) {
        return (0.0 <= score_a && score_a <= 1.0 &&
                0.0 <= score_b && score_b <= 1.0 &&
                score_a + score_b < 1.1);
    }

    /**
     * @param rating_a Current rating of player A
     * @param rating_b Current rating of player B
     * @return Expected outcome for both players
     */
    private double[] get_expected_scores(double rating_a, double rating_b) {
        double expected_score_a = this.expect(rating_a, rating_b);
        double expected_score_b = this.expect(rating_b, rating_a);

        return new double[] {expected_score_a, expected_score_b};
    }

    /**
     * @param rating_a Current rating of player A
     * @param rating_b Current rating of player A
     * @return Expected outcome for player A
     */
    private double expect(double rating_a, double rating_b) {
        return 1.0 / (1 + Math.pow(10, ((rating_b - rating_a) / this.C_VALUE)));
    }

    /**
     * @param rating Current rating of the player
     * @param score Actual outcome of the game
     * @param expected_score Expected outcome of the game
     * @return New rating of the player
     */
    private double update(double rating, double score, double expected_score) {
        return rating + this.K_FACTOR * (score - expected_score);
    }

    /**
     * @param score Actual outcome of the game
     * @param expected Expected outcome of the game
     * @return Either -1 or 0 or 1
     */
    private double p (double score, double expected) {
        if (score == expected) {
            return 0;
        }
        return (score - expected) / Math.abs(score - expected);
    }

    /**
     * @param points_a points scored by player A
     * @param points_b points scored by player B
     * @return fraction of points
     */
    private double points_fraction (double points_a, double points_b) {
        if (points_a == points_b && points_a == 0) {
            return 0;
        }
        return points_a / (points_a + points_b);
    }

    private double[] get_scores(double points_a, double points_b) {
        if (points_a == points_b) {
            return new double[] {0.5, 0.5};
        } else if (points_a > points_b) {
            return new double[] {1, 0};
        } else {
            return new double[] {0, 1};
        }
    }

    // Overloading functions
    public double[] elo(long rating_a, long rating_b, int outcome) {
        return elo((double) rating_a, (double) rating_b, outcome);
    }

    // ratings double
    public double[] elo_with_points(double rating_a, double rating_b, double points_a, double points_b) {
        return elo_with_points(rating_a, rating_b, points_a, points_b, DEFAULT_METHOD);
    }

    public double[] elo_with_points(double rating_a, double rating_b, long points_a, long points_b, int method) {
        return elo_with_points(rating_a, rating_b, (double) points_a, (double) points_b, method);
    }

    public double[] elo_with_points(double rating_a, double rating_b, long points_a, long points_b) {
        return elo_with_points(rating_a, rating_b, points_a, points_b, DEFAULT_METHOD);
    }

    // ratings long
    public double[] elo_with_points(long rating_a, long rating_b, long points_a, long points_b, int method) {
        return elo_with_points((double) rating_a, (double) rating_b, (double) points_a, (double) points_b, method);
    }

    public double[] elo_with_points(long rating_a, long rating_b, long points_a, long points_b) {
        return elo_with_points(rating_a, rating_b, points_a, points_b, DEFAULT_METHOD);
    }

    public double[] elo_with_points(long rating_a, long rating_b, double points_a, double points_b, int method) {
        return elo_with_points((double) rating_a, (double) rating_b, points_a, points_b, method);
    }

    public double[] elo_with_points(long rating_a, long rating_b, double points_a, double points_b) {
        return elo_with_points(rating_a, rating_b, points_a, points_b, DEFAULT_METHOD);
    }
}