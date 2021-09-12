from botok import Text
from tqdm import tqdm

tibetan_tokens = []

t = Text(text)
tokens = t.tokenize_words_raw_text

for token in tqdm(tokens.split(' ')):

    token = token.replace('_', ' ')
    tibetan_tokens.append(token)