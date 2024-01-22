
class ELO:
    """
    Class intended for ELO Rating use in multiple scenarios
    """

    def __init__(self, k: int = 32, c: int = 400):
        self.__K = k
        self.__c = c

    def update_rating(self,
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
        new_rating_a = rating_a + self.__K * (score_a - expected_score_a)
        new_rating_b = rating_b + self.__K * (score_b - expected_score_b)
        new_ratings = (new_rating_a, new_rating_b)

        return new_ratings

    def __get_expected_scores(self,
                              rating_a: float,
                              rating_b: float) -> tuple[float, float]:
        """
        This function returns the expected scores of individual players based on their ratings
        :param rating_a: current rating of player A
        :param rating_b: current rating of player B
        :return: expected scores of the two players
        """
        expected_score_a = 1 / (1 + 10 ** ((rating_b - rating_a) / self.__c))
        expected_score_b = 1 / (1 + 10 ** ((rating_a - rating_b) / self.__c))
        expected_scores = (expected_score_a, expected_score_b)

        return expected_scores
