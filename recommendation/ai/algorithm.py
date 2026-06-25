from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommendation.models import Department

def recommend_department(user_symptoms):
    """
    Core AI Recommendation Algorithm.
    
    Uses TF-IDF (Term Frequency-Inverse Document Frequency) to convert the text of 
    the symptoms into mathematical vectors. It then uses Cosine Similarity to find
    the "angle" between the user's symptom vector and the database's department 
    keyword vectors to find the closest match.
    """
    departments = Department.objects.all()
    if not departments:
        return None

    # Step 1: Gather the "corpus" (collection of documents)
    # The documents are the keywords belonging to each department in the system.
    dept_keywords = [dept.keywords for dept in departments]

    # We append the user's typed symptoms as the FINAL document in our corpus.
    corpus = dept_keywords + [user_symptoms]

    # Step 2: Vectorization (TF-IDF)
    # The vectorizer mathematically evaluates how important a word is. 
    # If "pain" appears everywhere, it gets a low score. If "wheezing" is rare 
    # but appears in Pulmonology, it gets a high score.
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Step 3: Isolate Vectors
    # The last vector in the matrix is our user's symptoms.
    user_vector = tfidf_matrix[-1]
    
    # The rest are the department keyword vectors.
    dept_vectors = tfidf_matrix[:-1]

    # Step 4: Calculate Cosine Similarity
    # This checks the physical distance/angle between the user vector and all department vectors.
    # Returns an array of scores from 0.0 (no match) to 1.0 (perfect match).
    similarity_scores = cosine_similarity(user_vector, dept_vectors).flatten()

    # Step 5: Find the Best Match
    # argmax() gets the index of the highest score.
    best_match_index = similarity_scores.argmax()
    
    # If the score is higher than 0, we found a match. If it's 0, they typed gibberish.
    if similarity_scores[best_match_index] > 0:
        return departments[int(best_match_index)]
    
    return None
