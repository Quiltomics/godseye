import os

MIN_SIZE = 4  # the minimum size for a token
FIGSIZE=(5, 3)  # Figure size

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME_DIR = os.path.expanduser("~")

KEYWORDS = (
    "coronary artery",
    "congestive heart",
    "congenital heart",
    "hypertension",
    "cardiomyopathy",
    "stroke",
    "myocardial infarction",
    "angina",
    "arrhythmia",
)

FILE_TYPE_KEY = {
    "pubmed": ("PubmedArticleSet", "PubmedArticle"),
    "medline": "MedlineCitationSet"
}