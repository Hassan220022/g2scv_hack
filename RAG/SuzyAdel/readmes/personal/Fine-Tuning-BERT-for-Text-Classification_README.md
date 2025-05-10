# Fine-Tuning-BERT-for-Text-Classification
This project involves fine-tuning a pre-trained BERT (Bidirectional Encoder Representations from Transformers) model for a text classification task on a given dataset. The goal is to adapt BERT to classify Arabic text inputs into predefined categories by training it on a labeled dataset(Positive, Negative,Mixed) .


## Key Features of This Implementation:
- Proper Arabic Handling: Uses asafaya/bert-base-arabic specifically for Arabic text

- Exact Symbol Removal: Only removes the specified symbols while preserving Arabic text structure

- Optimal max_len: Calculates the exact needed length without truncation

- Batch Size Optimization: Starts with 8 and allows you to increase if GPU memory permits

- Gradient Accumulation: Properly implemented with steps=8

- Stratified Splitting: Maintains class balance in train/test sets

- Full Evaluation: Includes confusion matrix and custom sentence testing

- Reproducibility: All random seeds set
![image](https://github.com/user-attachments/assets/7a5ccc85-ea82-42e9-908c-e790972804d4)
