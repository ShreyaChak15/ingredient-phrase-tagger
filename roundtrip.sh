#!/bin/sh
COUNT_TRAIN=130000
COUNT_TEST=20000

echo "generating training data..."
bin/generate_data --data-path=nyt-ingredients-snapshot-2015.csv --count=$COUNT_TRAIN --offset=0 > tmp/train_file || exit 1

echo "training..."
crf_learn template_file tmp/train_file tmp/model_file || exit 1

echo "generating test data..."
bin/generate_data --data-path=input.txt --count=6 --offset=0 > tmp/test_file || exit 1

echo "testing..."
crf_test -m tmp/model_file tmp/test_file > tmp/test_output || exit 1

echo "generating test data..."
python bin/parse-ingredients.py inputs.txt > results.txt

python bin/convert-to-json.py results.txt > parsed_r.json
