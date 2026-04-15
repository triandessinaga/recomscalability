import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load data
df = pd.read_csv("data/products.csv")

# Encode fitur kategorikal → numerik
df_encoded = pd.get_dummies(df.drop(columns=["product"])).astype(int)

# Hitung cosine similarity antar produk
similarity = cosine_similarity(df_encoded)

# Cache sederhana untuk menyimpan hasil rekomendasi
_cache = {}


def recommend(keyword: str, top_n: int = 3) -> list:
    keyword = keyword.strip()
    if keyword in _cache:
        return _cache[keyword]

    matches = df[df["product"].str.contains(keyword, case=False, na=False)]
    if matches.empty:
        return []

    idx = matches.index[0]
    scores = sorted(enumerate(similarity[idx]), key=lambda x: x[1], reverse=True)
    result = [df.iloc[i]["product"] for i, _ in scores[1:top_n + 1]]

    _cache[keyword] = result
    return result


def search_products(keyword: str) -> list:
    keyword = keyword.strip()
    matches = df[df["product"].str.contains(keyword, case=False, na=False)]
    return matches["product"].tolist()
