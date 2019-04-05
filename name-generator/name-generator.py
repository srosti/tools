import urllib.request
import random

# Two ways to get a list of words

# First way - get list from freebsd site - there are others on the web
word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
response = urllib.request.urlopen(word_url)
long_txt = response.read().decode()
words = long_txt.splitlines()

# Second way - get the list locally - TODO: need to check if this exists on raspberry pi
words2 = None
with open('/usr/share/dict/words') as f:
    words2 = f.read().splitlines()

upper_words = [word for word in words if word[0].isupper()]
name_words  = [word for word in upper_words if not word.isupper()]
rand_name   = ' '.join([name_words[random.randint(0, len(name_words))] for i in range(2)])
print(rand_name)

upper_words = [word for word in words2 if word[0].isupper()]
name_words  = [word for word in upper_words if not word.isupper()]
rand_name   = ' '.join([name_words[random.randint(0, len(name_words))] for i in range(2)])
print(rand_name)