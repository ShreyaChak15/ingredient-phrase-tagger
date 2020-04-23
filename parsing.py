import pandas as pd
import numpy as np
import json
import subprocess
import io

df = pd.read_csv('ingr_mod.csv', encoding='latin-1')
# df = df.iloc[0:5000, :]
df_new = df.groupby('recipe_id')['ingredients'].apply(list).reset_index(name='ingredients')
# df_new = df_new.iloc[5000:10000, :]
ingredients = df_new['ingredients'].to_numpy()

parsed_ingr = []
i=0

for ingr in ingredients:
    with io.open('tmp/parser-input.txt', 'w') as f:
        f.write('\n'.join(unicode(ingr)))
    with io.open('tmp/parser-output.txt', 'w') as f:
        bash_cmd = "python bin/parse-ingredients.py tmp/parser-input.txt"
        process = subprocess.check_call(bash_cmd.split(), stdout=f)
    with io.open('tmp/parser-output.json', 'w') as f:
        bash_cmd = "python bin/convert-to-json.py tmp/parser-output.txt"
        process = subprocess.check_call(bash_cmd.split(), stdout=f)
    with io.open('tmp/parser-output.json', 'r') as f:
        pingr = json.dumps(json.load(f))
    parsed_ingr.append(pingr)
    if i%100==0:
        print("%d Iteration done" %i)
    i+=1
        
# np.savetxt('parsed_ingredients.csv', parsed_ingr, delimiter=',', fmt="%s")
pd.Series(parsed_ingr).to_csv("parsed_ingredients.csv")