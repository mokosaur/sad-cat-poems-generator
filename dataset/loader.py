import os

__location__ = os.path.dirname(os.path.realpath(__file__))


def load_author(author, files=None, keep_empty=False):
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
                        poems[title] = content
                        content = ''
                    title = clean_line[1:].strip()
                else:
                    if keep_empty or clean_line.strip() != '':
                        content += clean_line
    return poems
