import argparse
import pandas as pd
import re
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
import os

def clean_text(s):
    s = str(s)
    s = s.replace('\n',' ').replace('\r',' ')
    s = re.sub(r'http\S+',' <URL> ', s)
    s = re.sub(r'[^\w\s<>&]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip().lower()
    return s

def main(args):
    df = pd.read_csv(args.input)
    df = df.drop_duplicates(subset=['Message']).dropna(subset=['Message'])
    df['cleaned_message'] = df['Message'].apply(clean_text)
    # Map categories to lowercase standard names
    df['category'] = df['Category'].str.strip().str.lower().map({
        'spam': 'spam',
        'transactional': 'transactional',
        'promotional': 'promotional',
        'promo': 'promotional'
    }).fillna('spam')
    X = df['cleaned_message'].values
    y = df['category'].values
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,stratify=y,random_state=42)
    vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=200000)
    clf = SGDClassifier(loss='log_loss', max_iter=1000, tol=1e-3)
    pipeline = Pipeline([('vect', vectorizer), ('clf', clf)])
    print("Training on", len(X_train), "samples...")
    pipeline.fit(X_train, y_train)
    print("Evaluating...")
    preds = pipeline.predict(X_test)
    print(classification_report(y_test, preds))
    cm = confusion_matrix(y_test, preds)
    print("confusion_matrix:\n", cm)
    os.makedirs(args.out, exist_ok=True)
    joblib.dump(pipeline.named_steps['vect'], os.path.join(args.out,'vectorizer.joblib'))
    joblib.dump(pipeline.named_steps['clf'], os.path.join(args.out,'model.joblib'))
    # Save a small sample of test for quick smoke tests
    sample = pd.DataFrame({'message': X_test[:200], 'label': y_test[:200]})
    sample.to_csv(os.path.join(args.out,'eval_sample.csv'), index=False)
    print("Saved artifacts to", args.out)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input', default='data/message_dataset.csv')
    p.add_argument('--out', default='model/artifacts')
    args = p.parse_args()
    main(args)
