# CleanCity Email Classifier Evaluation Report

## 1. Overview

This report compares classifier predictions with the ground-truth labels.

## 2. Dataset Summary

- Dataset: `emails_labeled.csv`
- Emails evaluated: 220
- Runtime/API exceptions: 142
- Fallback (`I don't know`) predictions: 142
- Categories shown (including fallback): 5

## 3. Overall Performance

- **Accuracy:** 35.45%
- **Macro precision:** 80.00%
- **Macro recall:** 28.36%
- **Macro F1-score:** 41.87%
- **Weighted precision:** 100.00%
- **Weighted recall:** 35.45%
- **Weighted F1-score:** 52.34%

## 4. Per-Category Metrics

| Category | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Missed Pickup | 100.00% | 36.36% | 53.33% | 55 |
| Schedule Change | 100.00% | 34.55% | 51.35% | 55 |
| Complaint | 100.00% | 36.36% | 53.33% | 55 |
| Other | 100.00% | 34.55% | 51.35% | 55 |
| I don't know | 0.00% | 0.00% | 0.00% | 0 |

## 5. Confusion Matrix

Rows represent actual labels; columns represent predicted labels.

![Confusion Matrix](confusion_matrix.png)

## 6. Prediction Results

Detailed predictions and error details are saved in `evaluation_predictions.csv`.

## 7. Error Analysis

The evaluation script encountered runtime/API exceptions for 142 email(s). Those rows were assigned `I don't know`. Review the `evaluation_error` column in the predictions CSV.

Fallback predictions may indicate uncertainty or invalid model output. They are counted as incorrect unless the ground-truth label matches the fallback.

## 8. Conclusion

Overall accuracy on this dataset was 35.45%. Use the per-category metrics and prediction CSV to investigate errors. Results on this dataset do not guarantee performance on new emails.
