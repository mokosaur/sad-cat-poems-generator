import os

__location__ = os.path.dirname(os.path.realpath(__file__))


def load_author(author, files=None, keep_empty=False, clean=True, only_polish=True):
    """Loads poems written by the given author.

    :param author: Author of the poems
    :param files: List of filenames from which you want to import poems; if None, all the files will be loaded
    :param keep_empty: Set to True if you want to keep empty lines in poems
    :return: Dictionary in which keys are titles of poems, and values are their content
    """
    if not files:
        files = os.listdir(os.path.join(__location__, author))
    else:
        files = [f if f[-4:] == '.txt' else f + '.txt' for f in files]
    poems = {}
    for f in files:
        title = ''
        content = ''
        with open(os.path.join(__location__, author, f), 'r', encoding='utf8') as file:
            for line in file:
                clean_line = line.replace('\ufeff', '')
                if clean_line.startswith("#"):
                    if len(content):
                        if clean:
                            content = clean_data(content)
                            title = clean_data(title)
                        if not only_polish or polish_title(title):
                            poems[title] = content
                        content = ''
                    title = clean_line[1:].strip()
                else:
                    if keep_empty or clean_line.strip() != '':
                        content += clean_line
    return poems


def clean_data(text):
    corrections = {
        'Ã³': 'ó',
        'Å¼': 'ż',
        'Ä™': 'ę',
        'Å‚': 'ł',
        'Å›': 'ś',
        'Ä‡': 'ć',
        'Ä…': 'ą',
        'Å„': 'ń',
        'Åº': 'ź'
    }
    for k, v in corrections.items():
        text = text.replace(k, v)
    return text


def polish_title(title):
    return "english" not in title and "esperanto" not in title and "[en]" not in title
