import re

# WORD_FILE = 'data/words_alpha.txt'
# WORD_FILE = 'data/usr_share_dict_words.txt'
COMMON_WORD_FILE = 'data/words_common.txt'
WORD_FILE = 'data/corncob.txt'

with open(WORD_FILE) as f:
    words = [line.strip() for line in f]
    words = [word for word in words if re.search(r"^[a-z]+$", word)]

with open(COMMON_WORD_FILE) as f:
    common_words = [line.strip() for line in f]
    common_words = [word for word in common_words if re.search(r"^[a-z]+$", word)]
