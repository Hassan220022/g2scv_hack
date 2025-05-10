# 🧠 Arabic Text Classification Transformer

This repository explores **Arabic text classification** using various deep learning models. Over multiple trials, we've tested different architectures, tuning techniques, and preprocessing methods to determine what works best. Spoiler: sometimes, **keeping it simple is the secret!** 😉

---

## 🚀 Best Results  

Here are the top-performing models along with their evaluation results:  

### **1️⃣ Model 3 (Best Performance)**  
📌 **Optimized BiLSTM + AraVec Validation**  

![Model 3](https://github.com/user-attachments/assets/e4b161d0-178f-4434-b42c-41d46adc5d58)  

### **2️⃣ Model 4 (Very Strong Performance)**  
📌 **Fine-tuned embeddings + additional dropout**  

![Model 4](https://github.com/user-attachments/assets/37761dde-3923-4ef4-96f8-f7b75e351720)  

### **3️⃣ Model 2 (Balanced but Slower)**  
📌 **Experimented with GRU & GlobalMaxPooling1D**  

![Model 2](https://github.com/user-attachments/assets/71088259-5d0d-4222-b9bd-3afc3da06375)  

### **4️⃣ Model 1 (The Baseline Model)**  
📌 **Simple BiLSTM with basic preprocessing**  

![Model 1](https://github.com/user-attachments/assets/5c59f0dc-28e9-441f-b3ae-a50506b1fc44)  

---

## 🏗️ Project Structure  

1. **Bidirectional LSTM-based Models**  
2. **Logical AraVec Validation (Word Similarity + Vector Math)**  
3. **Shows Raw & Cleaned Data**  
4. **90-10 Train-Test Split**  
5. **Preprocessing, Tokenization & Padding**  
6. **Confusion Matrix + Classification Report**  
7. **Train & Validation Loss Curve**  
8. **Testing on New Arabic Sentences**  
9. **Final Summary & Insights**  

---

## 🔄 Evolution of the Models  

After a lot of trial and error (and a few existential crises), here’s how our models evolved:  

1. **Baseline Model**:  
   - Simple **BiLSTM (128 & 64 units)** + dropout  
   - Balanced architecture with no excessive complexity  

2. **First Modification**:  
   - Switched to **GRU**, added **GlobalMaxPooling1D**, **Dense(64)**  
   - Introduced **recurrent dropout**  

3. **Second Modification**:  
   - Enabled **mixed precision training**  
   - Used **learning rate scheduler**  
   - Downside: **Too heavy and slow** for our dataset  

4. **Final Adjustment**:  
   - **Reduced epochs from 10 to 6**  
   - **Implemented cross-validation** for better generalization  

**Lesson Learned:** More layers ≠ better performance. The simplest model (BiLSTM with proper tuning) turned out to be the best! 😅  

---

## 🔮 Future Improvements  

- **Try Transformer-based models** (if feasible for Arabic text tasks).  
- **Use more extensive Arabic datasets** for better generalization.  
- **Explore data augmentation techniques** to handle rare words better.  

🤖 *Remember: Sometimes, AI isn't about adding more—it's about optimizing what you already have!*  

---

**Contributions & Feedback**: Feel free to fork, improve, or share ideas! Let's keep making **Arabic NLP** better. 🚀
