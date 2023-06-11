import os
import pandas as pd

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

# path of the database
root_path = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(root_path, 'sites.db')

# get the domains from the parquet file
domains = pd.read_parquet('list of company websites.snappy.parquet', engine='fastparquet')
domains.insert(0, 'id', range(1, len(domains) + 1))
domains.insert(2, 'success', False)

# tranformers Hugging Face configuration
tokenizer = AutoTokenizer.from_pretrained('dslim/bert-base-NER')
model = AutoModelForTokenClassification.from_pretrained('dslim/bert-base-NER')
nlp = pipeline("ner", model=model, tokenizer=tokenizer)