import streamlit as st
from googletrans import Translator

translator = Translator()

# Define the list of supported languages

languages = {
    'bn': 'bengali',
    'en': 'english',
    'gu': 'gujarati',
    'hi': 'hindi',
    'kn': 'kannada',
    'ml': 'malayalam',
    'ne': 'nepali',
    'or': 'odia',
    'pa': 'punjabi',
    'sd': 'sindhi',
    'ta': 'tamil',
    'te': 'telugu',
    'ur': 'urdu'
}

# Create a selectbox for language selection
language = st.selectbox('Select language', list(languages.values()))

# Get the language code from the selected language
language_code = [code for code, lang in languages.items() if lang == language][0]

# Create a text input for the text to be translated
text = st.text_input('Enter text')

# Translate the text
if text:
    translation = translator.translate(text, dest=language_code)
    st.write(translation.text)