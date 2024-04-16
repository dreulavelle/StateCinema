from statecinema import Movie


def test_movie_init():
    movie = Movie(title="Example Movie")
    assert isinstance(movie, Movie)
