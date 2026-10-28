
# Import the functions we want to test from wordstat.py
from wordstat import clean_words, read_file, main

# Import pytest to use its testing features
import pytest


# Test 1: Check whether words are converted to lowercase
# and punctuation is removed.
def test_clean_words():
    result = clean_words("Python is EASY!")
    assert result == ["python", "is", "easy"]


# Test 2: Check whether empty text returns an empty list.
def test_clean_words_empty_text():
    result = clean_words("")
    assert result == []


# Test 3: Check whether Unicode characters, such as é and ï,
# are preserved while cleaning the text.
def test_clean_words_unicode():
    result = clean_words("Café is nice. naïve person!")
    assert result == ["café", "is", "nice", "naïve", "person"]


# Test 4: Check whether repeated words are preserved
# and converted to lowercase.
def test_clean_words_repeated_words():
    result = clean_words("Python python PYTHON")
    assert result == ["python", "python", "python"]


# Test 5: Check whether text containing only punctuation
# returns an empty list.
def test_clean_words_punctuation_only():
    result = clean_words("!!! , . ?")
    assert result == []


# Test 6: Check whether the function can process a very long line
# containing 10,000 repeated words without losing any words.
def test_clean_words_very_long_line():
    text = "Python " * 10000

    result = clean_words(text)

    # Check the total number of words.
    assert len(result) == 10000

    # Check the first and last words.
    assert result[0] == "python"
    assert result[-1] == "python"


# Test 7: Check whether read_file() correctly reads a valid file.
# tmp_path creates a temporary directory for this test.
def test_read_file(tmp_path):
    file_path = tmp_path / "sample.txt"

    # Create the file and write sample text into it.
    file_path.write_text("Python is easy.", encoding="utf-8")

    # Read the file using the function being tested.
    result = read_file(str(file_path))

    # Check whether the returned text matches the file content.
    assert result == "Python is easy."


# Test 8: Check whether read_file() exits when the file is missing.
def test_read_file_missing_file(tmp_path):
    # Create a path for a file that does not exist.
    file_path = tmp_path / "missing.txt"

    # Check whether the function raises SystemExit
    # when it cannot find the file.
    with pytest.raises(SystemExit):
        read_file(str(file_path))
def test_main_empty_file(tmp_path, capsys):
    # Create an empty text file
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding="utf-8")

    # Run main() with the empty file as its argument
    with pytest.raises(SystemExit) as exc_info:
        main([str(file_path)])

    # Check that the program exits with an error status
    assert exc_info.value.code == 1

    # Check the displayed error message
    captured = capsys.readouterr()
    assert "Error: The file is empty." in captured.out