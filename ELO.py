class ELO:
    """
    Class intended for ELO Rating use in multiple scenarios
    """

    def __init__(self, k_factor: int = 32, c_value: int = 400):
        """
        Constructor for ELO rating
        :param k_factor: K factor, default 32
        :param c_value: c factor, default 400
        """
        self.__K_FACTOR = k_factor
        self.__C_VALUE = c_value

    def elo(self,
            rating_a: float,
            rating_b: float,
            score_a: float,
            score_b: float) -> tuple[float, float]:
        """
        This function updates the rating of two players based on points scored by them in a PvP match
        :param rating_a: current rating of player A
        :param rating_b: current rating of player B
        :param score_a: points scored by player A
        :param score_b: points scored by player B
        :return: new ratings of the two players
        """

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
