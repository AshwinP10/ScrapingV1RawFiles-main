import os.path
import csv
from scholarly import scholarly
from nltk import sent_tokenize, word_tokenize
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize.treebank import TreebankWordDetokenizer
import heapq
import time

# CSV file name
csv_file = 'gscholar.csv'

def summarize_text(text, num_sentences=2):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

    # Calculate word frequency
    freq_dist = FreqDist(words)

    # Calculate sentence scores based on word frequency
    sentence_scores = {}
    for sentence in sentences:
        for word, freq in freq_dist.items():
            if word in sentence.lower():
                if sentence in sentence_scores:
                    sentence_scores[sentence] += freq
                else:
                    sentence_scores[sentence] = freq

    # Get the summary by selecting the top sentences
    summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary = TreebankWordDetokenizer().detokenize(summary_sentences)

    return summary

def retrieve_google_scholar_data(keywords, conferences, num_results=10, summary_sentences=2):
    search_query = scholarly.search_pubs(' '.join(keywords))
    for i, result in enumerate(search_query):
        if i >= num_results:
            break
        try:
            document_title = result.bib.get('title', '')
            authors = ', '.join(result.bib.get('author', []))
            publication_year = result.bib.get('year', '')
            pdf_link = result.bib.get('url', '')
            conference = result.bib.get('journal', '')
            abstract = result.bib.get('abstract', '')

            # Add your implementation check logic
            implementation_check = 'GitHub Link' if 'github' in abstract.lower() else ''

            # Summarize the abstract
            summarized_abstract = summarize_text(abstract, num_sentences=summary_sentences)

            # Create a dictionary with the data
            result_data = {
                'Document Title': document_title,
                'Authors': authors,
                'Publication Year': publication_year,
                'PDF Link': pdf_link,
                'Implementation?': implementation_check,
                'Abstract Summary': summarized_abstract
            }

            # Check if the paper meets your criteria (e.g., conference)
            if conference.lower() in conferences:
                # Print the data to the terminal
                print("=" * 50)
                print("Document Title: ", document_title)
                print("Authors: ", authors)
                print("Publication Year: ", publication_year)
                print("PDF Link: ", pdf_link)
                print("Implementation?: ", implementation_check)
                print("Abstract Summary: ", summarized_abstract)
        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage:
keywords = ['multi-agent', 'social navigation', 'dynamic environments', 'crowds']
conferences = ['IROS', 'AAAI', 'ICRA']

# Adjust the number of results and summary sentences as needed
retrieve_google_scholar_data(keywords, conferences, num_results=5, summary_sentences=2)
