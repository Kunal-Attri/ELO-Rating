class ELO:
    """
    Class intended for ELO Rating use in multiple scenarios
    """

    def __init__(self, k_factor: int = 32, c_value: int = 400, l_factor: int = 16):
        """
        Constructor for ELO rating
        :param k_factor: K factor, default 32
        :param c_value: c factor, default 400
        :param l_factor: L factor, default 16
        """
        self.__K_FACTOR = k_factor
        self.__C_VALUE = c_value
        self.__L_FACTOR = l_factor

    def elo(self,
            rating_a: float,
            rating_b: float,
            score_a: float,
            score_b: float) -> tuple[float, float]:
        """
        This function updates the rating of two players based on outcome of a PvP match
        :param rating_a: current rating of player A
        :param rating_b: current rating of player B
        :param score_a: points scored by player A
        :param score_b: points scored by player B
        :return: new ratings of the two players
        """

        # Check if scores and valid
        if not self.__valid_scores(score_a, score_b):
            print("Scores not valid")
            return rating_a, rating_b

        # Expected scores of the players
        expected_scores = self.__get_expected_scores(rating_a, rating_b)
        expected_score_a, expected_score_b = expected_scores

        # New ratings of the players
        new_rating_a = self.__update(rating_a, score_a, expected_score_a)
        new_rating_b = self.__update(rating_b, score_b, expected_score_b)

        new_ratings = (new_rating_a, new_rating_b)
        return new_ratings

    def __update(self,
                 rating: float,
                 score: float,
                 expected_score: float) -> float:
        """
        Function for actual update formula implementation for updating rating of a player
        :param rating: current rating of the player
        :param score: actual score of the player
        :param expected_score: expected score of the player
        :return: new rating of the player
        """
        return rating + self.__K_FACTOR * (score - expected_score)

    def __get_expected_scores(self,
                              rating_a: float,
                              rating_b: float) -> tuple[float, float]:
        """
        This function returns the expected scores of individual players based on their ratings
        :param rating_a: current rating of player A
        :param rating_b: current rating of player B
        :return: expected scores of the two players
        """
        expected_score_a = self.__expect(rating_a, rating_b)
        expected_score_b = self.__expect(rating_b, rating_a)

        expected_scores = (expected_score_a, expected_score_b)
        return expected_scores

    def __expect(self,
                 rating_a: float,
                 rating_b: float) -> float:
        """
        Function for formula implementation for expected score of player A
        :param rating_a: current rating of player A
        :param rating_b: current rating of player B
        :return: expected score of player A
        """
        return 1.0 / (1 + 10 ** ((rating_b - rating_a) / self.__C_VALUE))

    def elo_with_points(self,
                        rating_a: float,
                        rating_b: float,
                        points_a: float,
                        points_b: float,
                        use_l_factor: bool = True) -> tuple[float, float]:
        """
        Function to calculate new ratings of two players based on points scored by them in a PvP match
        :param rating_a: current rating of player A
        :param rating_b: current rating of player B
        :param points_a: points scored by player A
        :param points_b: points scored by player B
        :param use_l_factor: Whether to rationalize points or use L factor
        :return: new ratings of the two players
        """
        if not use_l_factor:
            return self.__elo_rationalize_points(rating_a, rating_b, points_a, points_b)
        else:
            return self.__elo_with_l_factor(rating_a, rating_b, points_a, points_b)

    def __elo_rationalize_points(self,
                                 rating_a: float,
                                 rating_b: float,
                                 points_a: float,
                                 points_b: float
                                 ) -> tuple[float, float]:
        """
        Function to calculate new ELO ratings by rationalizing points for score
        :param rating_a: current rating of player A
        :param rating_b: current rating of player B
        :param points_a: points scored by player A
        :param points_b: points scored by player B
        :return: new ratings of the two players
        """
        if points_a == points_b and points_b == 0:
            # Both players got zero points
            score_a = 0.5
            score_b = 0.5
        else:
            # Not zero points
            score_a = points_a / (points_a + points_b)
            score_b = points_b / (points_a + points_b)

        return self.elo(rating_a, rating_b, score_a, score_b)

    def __elo_with_l_factor(self,
                            rating_a: float,
                            rating_b: float,
                            points_a: float,
                            points_b: float
                            ) -> tuple[float, float]:
        """
        Function to calculate ELO ratings by using L factor for points scored
        :param rating_a: current rating of player A
        :param rating_b: current rating of player B
        :param points_a: points scored by player A
        :param points_b: points scored by player B
        :return: new ratings of the two players
        """
        if points_a == points_b:
            # Draw match
            score_a = 0.5
            score_b = 0.5
        elif points_a > points_b:
            # Player A won
            score_a = 1
            score_b = 0
        else:
            #  Player B won
            score_a = 0
            score_b = 1

        # Calculating new ratings based on outcome
        new_ratings = self.elo(rating_a, rating_b, score_a, score_b)
        new_rating_a, new_rating_b = new_ratings

        # Get expected scores
        expected_scores = self.__get_expected_scores(rating_a, rating_b)
        expected_a, expected_b = expected_scores

        # Calculating p value
        p_a = self.__p(score_a, expected_a)
        p_b = self.__p(score_b, expected_b)

        # Adding L factor calculation for extra points
        new_rating_a += p_a * self.__L_FACTOR * self.__points_fraction(points_a, points_b)
        new_rating_b += p_b * self.__L_FACTOR * self.__points_fraction(points_b, points_a)

        new_ratings = (new_rating_a, new_rating_b)
        return new_ratings

    def __p(self, score, expected):
        """
        Returns 1 or 0 or -1
        :param score: actual outcome of match
        :param expected: expected outcome of match
        :return: Either 1 or -1 or 0
        """
        if score == expected:
            return 0
        return (score - expected) / abs(score - expected)

    def __points_fraction(self, points_a, points_b):
        """
        Returns the fraction of points scored by a player w.r.t. total points scored.
        :param points_a: points scored by player A
        :param points_b: points scored by player B
        :return: fraction of points
        """
        if points_a == points_b:
            return 0
        return points_a / (points_a + points_b)

    def __valid_scores(self, score_a, score_b):
        return 0 <= score_a <= 1 and 0 <= score_b <= 1 and score_a + score_b <= 1.1