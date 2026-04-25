import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download necessary NLTK data safely
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def download_nltk_data():
    required_packages = ['punkt', 'stopwords', 'wordnet', 'omw-1.4', 'punkt_tab']
    for package in required_packages:
        try:
            nltk.data.find(f'tokenizers/{package}') if 'punkt' in package else nltk.data.find(f'corpora/{package}')
        except LookupError:
            print(f"Downloading NLTK package: {package}...")
            try:
                nltk.download(package, quiet=True)
            except Exception as e:
                print(f"Failed to download {package}: {e}")

download_nltk_data()

class TextPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
    
    def clean_text(self, text):
        """
        Apply full preprocessing pipeline:
        1. Lowercase
        2. Remove HTML tags and special characters
        3. Tokenize
        4. Remove stopwords
        5. Lemmatize
        """
        if not isinstance(text, str):
            return ""
            
        # 1. Lowercase
        text = text.lower()
        
        # 2. Remove HTML tags (e.g., <br />)
        text = re.sub(r'<.*?>', ' ', text)
        
        # Remove non-alphabit characters (keep spaces)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # 3. Tokenize
        tokens = word_tokenize(text)
        
        # 4 & 5. Stopword removal and Lemmatization
        clean_tokens = [
            self.lemmatizer.lemmatize(token) 
            for token in tokens 
            if token not in self.stop_words and len(token) > 2
        ]
        
        return " ".join(clean_tokens)

if __name__ == "__main__":
    # Test
    tp = TextPreprocessor()
    sample = "This is a <b>SAMPLE</b> text! It's running nicely."
    print("Original:", sample)
    print("Cleaned:", tp.clean_text(sample))
