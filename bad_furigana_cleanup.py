import pandas
import re

'''
Some cards from premade decks have horrible formatting. 
An example sentence looks like so:
真面目[まじめ;h]に やろう[,やる;h] よ
I would like these to instead look like this:
真面目にやろうよ
They also have extra fields I don't care about so those will be removed.
'''

filename = input('Enter the name of the CSV containing the exported cards:\n')
filename = f'{filename}.csv'
df = pandas.read_csv(filename, index_col=False, usecols=['word','image','audio','frontaudio','target','notes'])

def remove_furigana_and_spaces(expression):
    # expression =~ 真面目[まじめ;h]に やろう[,やる;h] よ
    # Remove spaces and everything between brackets
    # remove everything between braces 
    expression = re.sub("[\(\[].*?[\)\]]", "", expression)
    # remove &ensp; 
    expression = re.sub("&ensp;", "", expression)
    # smush it all together
    expression = "".join(expression.split())
    
    return expression

df['word'] = df['word'].apply(remove_furigana_and_spaces)
df = df.drop(['frontaudio'], axis=1)
df = df.drop(['target'], axis=1)
df.insert(4,'tags', 'defurred')

df.to_csv('defurred_cards.csv', index=False)