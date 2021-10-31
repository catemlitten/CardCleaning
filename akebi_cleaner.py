import pandas
import re

'''
Akebi is handy for adding quickly adding words to Anki on mobile
but the default cards leave something to be desired for me.
Basic cleanup script taking in a deck exported to CSV and returning a CSV
with kanji + furigana split out, romaji + akebi link removed, and tags updated
An additional column for recordings is added but that is not (yet?) automated
'''

filename = input('Enter the name of the CSV containing the exported cards:\n')
filename = f'{filename}.csv'
df = pandas.read_csv(filename)

def push_furigana(kwf):
    # kwf =~ 水筒[すいとう]
    # Extract the furigana from between brackets
    split_kwf = kwf.split('[') # break at first bracket
    furigana = split_kwf[1][0:-1] # remove ending bracket
    return furigana

def clean_kanji(kwf):
    # kwf =~ 水筒[すいとう]
    # Extract the kanji without the furigana
    split_kwf = kwf.split('[') # break at first bracket
    kanji = split_kwf[0]
    return kanji


df = df.drop(['akebilink'], axis=1)
df.insert(6,'recording', '')
df['tags'] = df['tags'].replace('Akebi', 'akebifixed') # distinguish between fixed and unfixed cards quickly
df['romaji'] = df['kanjiwithfurigana'].apply(push_furigana)
df['kanjiwithfurigana'] = df['kanjiwithfurigana'].apply(clean_kanji)


df.to_csv('akebi_cards.csv', index=False)  
