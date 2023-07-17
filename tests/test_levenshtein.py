from youtube_bz.utils.levenshtein_distance import levenshtein_distance


def test_levenshtein_distance():
    assert levenshtein_distance("test", "test") == 0
    assert levenshtein_distance("cats", "dogs") == 3
    assert levenshtein_distance("cats", "") == 4
    assert levenshtein_distance("", "cats") == 4
