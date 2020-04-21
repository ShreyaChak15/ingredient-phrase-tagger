import pandas as pd
import numpy as np
import json
import subprocess

df = pd.read_csv('ingr.csv', encoding='latin-1')

df_new = df.groupby('recipe_id')['ingredients'].apply(list).reset_index(name='ingredients')
ingredients = df_new['ingredients'].to_numpy()

parsed_ingr = []
for ingr in ingredients:
    with open('tmp/parser-input.txt', 'w') as f:
        f.write('\n'.join(ingr))
    with open('tmp/parser-output.txt', 'w') as f:
        bash_cmd = "python bin/parse-ingredients.py tmp/parser-input.txt"
        process = subprocess.check_call(bash_cmd.split(), stdout=f)
    with open('tmp/parser-output.json', 'w') as f:
        bash_cmd = "python bin/convert-to-json.py tmp/parser-output.txt"
        process = subprocess.check_call(bash_cmd.split(), stdout=f)
    with open('tmp/parser-output.json', 'r') as f:
        pingr = json.load(f)
    parsed_ingr.append(pingr)
        
np.savetxt('parsed_ingredients', parsed_ingr, delimiter=',')