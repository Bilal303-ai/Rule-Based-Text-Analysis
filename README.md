# About

This program is designed to provide comprehensive insights into any given text by performing detailed analysis across several key metrics. By processing the text, the program outputs valuable information including:

**Word Count:** Total number of words in the text.

**Sentence Count:** Total number of sentences in the text.

**Average Sentence Length:** The average number of words per sentence.

**Complex Word Count:** Number of complex words (words with two or more syllables).

**Percentage of Complex Words:** The percentage of words in the text that are complex.

**Average Word Length:** The average number of characters per word.

**Positive Score:** A measure of the positivity of the text.

**Negative Score:** A measure of the negativity of the text.

**Subjectivity Score:** A measure of how subjective or objective the text is.

**Fog Index:** An index that estimates the readability of the text, indicating the years of education needed to understand the text on the first reading.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/Bilal303-ai/Rule-Based-Text-Analysis
   cd Ink2Pixel
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. **Access the App:** After running the app, you will see a message similar to:
   ```bash
   Running on local URL: http://127.0.0.1:7860
   ``` 
Copy the provided URL and paste it into your web browser to access the app.

## Note:
Number of words and sentences are computed after removing the stopwords from the text.
