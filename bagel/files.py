def files_using_word(filenames, word):
    files_with_word = []
    for filename in filenames:
        if word_in_file(word, filename):
            files_with_word.append(filename)
    return files_with_word


def word_in_file(word, filename):
    with open(filename) as f:
        contents = f.read().lower()
        return (word in contents)
