import joblib, pandas as pd, argparse
from sklearn.metrics import classification_report, confusion_matrix

def main(args):
    vect = joblib.load(args.vectorizer)
    clf = joblib.load(args.model)
    sample = pd.read_csv(args.sample)
    X = sample['message'].values
    X_t = vect.transform(X)
    preds = clf.predict(X_t)
    print(classification_report(sample['label'].values, preds))
    print("Confusion matrix:")
    print(confusion_matrix(sample['label'].values, preds))

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--vectorizer', default='model/artifacts/vectorizer.joblib')
    p.add_argument('--model', default='model/artifacts/model.joblib')
    p.add_argument('--sample', default='model/artifacts/eval_sample.csv')
    args = p.parse_args()
    main(args)
