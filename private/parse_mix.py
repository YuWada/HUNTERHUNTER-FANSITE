from bs4 import BeautifulSoup
import re

with open('mix.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

characters = []
# On huntermix, names are usually in <b> inside <td> or something similar.
# Let's see the structure first
