import csv
import streamlit as st

# --- Fungsi untuk load data ---
def load_news(filename):
    """Baca file news_data.csv ke list of dict"""
    # TODO: buka file CSV (filename) dan baca dengan csv.DictReader
    # kembalikan hasilnya dalam bentuk list
    news_list = []
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            news_list.append(row)
    return news_list

        
def load_comments(filename):
    """Baca file comment_news.csv ke list of dict"""
    # TODO: sama seperti load_news tapi untuk file komentar
    comments_list = []
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            comments_list.append(row)
    return comments_list

# --- Fungsi untuk memproses data ---
def process_data(news_list, comments_list):
    """
    Gabungkan berita dan komentar,
    hitung jumlah komentar & rata-rata rating.
    Hasilnya list of dict.
    """
    # TODO: Buat dictionary untuk kumpulkan komentar per idBerita
    comments_per_news = {}
    for c in comments_list:
        idb = c['idBerita']
        rating = float(c['Rating']) if c['Rating'] else 0
        if idb not in comments_per_news:
            comments_per_news[idb] = {'ratings': [], 'count': 0}
        comments_per_news[idb]['ratings'].append(rating)
        comments_per_news[idb]['count'] += 1

    result = []
    for n in news_list:
        idb = n['idBerita']
        headline = n['Headline']
        if idb in comments_per_news:
            ratings = comments_per_news[idb]['ratings']
            jumlah = comments_per_news[idb]['count']
            rata = sum(ratings) / jumlah if jumlah > 0 else 0
        else:
            rata = 0
            jumlah = 0
        result.append({
            'ID Berita': idb,
            'Headline': headline,
            'Rata-rata Rating': round(rata, 2),
            'Jumlah Komentar': jumlah
        })

    def ambil_rating(item):
        return item['Rata-rata Rating']

    result.sort(key=ambil_rating, reverse=True)
    return result

# --- Fungsi untuk tampilkan di Streamlit ---
def main():
    st.title("Analisis Sentimen & Popularitas Berita")
    st.write("Menampilkan ID, Headline, Rata-rata Rating, dan Jumlah Komentar, diurutkan dari rating tertinggi.")

    # TODO: baca data CSV
    news_data = load_news('news_data.csv')
    comment_data = load_comments('comment_news.csv')
    hasil = process_data(news_data, comment_data)
    st.table(hasil)

if __name__ == '__main__':
    main()
