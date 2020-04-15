from ask_jc.tokenizer.simple_regex_tokenizer import SimpleRegexTokenizer


def test_tokenize():
    text = 'I\'m one two-three 4 5 678 nine10, fiancée.'
    expected = ['I\'m', 'one', 'two-three', '4', '5', '678', 'nine10', ',', 'fiancée', '.']
    tokenizer = SimpleRegexTokenizer()
    actual = tokenizer.tokenize(text)
    assert expected == actual
