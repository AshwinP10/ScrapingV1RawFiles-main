import pandas as pd
import nltk
nltk.download('punkt')  # Download the sentence tokenizer

from nltk.tokenize import sent_tokenize

# Load the massive list CSV file
massive_list = pd.read_csv("msrandmrs_list.csv")

# Keep only the columns of interest
narrowed_list = massive_list[["Document Title", "Authors", "Publication Year", "PDF Link", "Abstract"]]

# Add a new column "Implementation?" with values "YES" or "NO" based on the presence of "github" in the abstract
narrowed_list["Implementation?"] = narrowed_list["Abstract"].str.contains("github", case=False, na=False).replace({True: "YES", False: "NO"})

# Function to summarize the abstract
def summarize_abstract(abstract):
    sentences = sent_tokenize(abstract)
    sentence_scores = {sentence: len(sentence.split()) for sentence in sentences}
    num_sentences_in_summary = 2
    summary_sentences = [sentence for sentence, score in sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences_in_summary]]
    summary = ' '.join(summary_sentences)
    return summary

# Apply the summarize_abstract function to create the "Abstract Summary" column
narrowed_list["Abstract Summary"] = narrowed_list["Abstract"].apply(summarize_abstract)

# Remove the original "Abstract" column
narrowed_list = narrowed_list[["Document Title", "Authors", "Publication Year", "PDF Link", "Implementation?", "Abstract Summary"]]

# Save the simplified list with the abstract summary to a new CSV file
narrowed_list.to_csv("msr.csv", index=False)
