# 📚 Scholarly Search: A Search Engine for Academic Papers

**Course:** CS547 Information Retrieval  

**Institution:** Worcester Polytechnic Institute (WPI)  

**Team:** Jatin Sisodia, Jingxuan Yang, Nandini Priya Sripada, Siddharth Kodwani, Steffi Dorothy

**Instructor:** Prof. Kyumin Lee

**Date:** 12/01/2024

---

## 📖 Overview

Scholarly Search is a web application designed to help researchers, academics, and students search for open-access academic papers. Inspired by platforms like Google Scholar, arXiv, and IEEE Xplore, it enables keyword-based search, relevance-ranked results, and user authentication — all tailored to the needs of scholarly users.

---

## 🔍 Features

- **Keyword Search:** Search by title, abstract, or author name.
- **User Authentication:** Login and registration for personalized access.
- **Paper Metadata:** View titles, authors, abstracts, publication dates, and direct links.
- **Domain-Specific Ranking:** Prioritized academic results.
- **Enhanced Filtering:** Filter results by publication date.
- **User-Centric Design:** Intuitive navigation and personalized experience.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.13.1, Django 5.1.4
- **Frontend:** Django templates (HTML, CSS, Figma for UI design)
- **Database:** SQLite3 + arXiv API integration
- **Libraries:** 
  - Natural Language Toolkit (nltk) for query processing
  - Boolean Retrieval and TF-IDF for ranking
  - Django ORM for simplified database interaction

---

## 🗂️ Dataset & Schema

- **Source:** arXiv API (open-access papers)
- **Schema:**
  | Field      | Type    | Description                     |
  |------------|---------|---------------------------------|
  | id        | INT     | Unique paper identifier        |
  | title     | TEXT    | Paper title                   |
  | abstract  | TEXT    | Paper abstract                |
  | authors   | TEXT    | Author list                  |
  | published | DATE    | Publication date             |
  | url       | TEXT    | Direct paper link (arXiv)    |

---

## 🚀 Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/SteffiDorothy/Scholarly-Search.git
cd CS547-IR-Scholarly-Search
```

2. **Create and activate a virtual environment**
```bash
python3 -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
```

3. **Apply migrations and load initial data**
```bash
python manage.py migrate
python manage.py loaddata arxiv_papers.sql
```

4. **Run the server**
```bash
python manage.py runserver
```

5. **Access the application**
- Open your browser and navigate to: `http://127.0.0.1:8000/`

---

## 📈 Project Structure
```
CS547-IR-Scholarly-Search/
├── manage.py
├── scholarly_search/        # Django project settings
├── search_app/              # Main application with views, models
├── templates/               # HTML templates
├── static/                  # Static files (CSS, JS)
├── db.sqlite3               # Database file
├── arxiv_papers.sql         # Preloaded papers dataset
```

---

## ⚙️ Technical Highlights

- Boolean retrieval + TF-IDF ranking

- Date-based filtering

- NLP preprocessing with nltk

- Responsive UI built from Figma designs

- Evaluation with relevance, ranking quality, and query coverage
  
---

## 📊 Evaluation Metrics

- Relevance

- Ranking quality

- Query coverage
  
---

## 🚀 Future Work

- Integrate advanced NLP techniques for smarter ranking

- Improve user interface based on feedback

- Extend to include additional academic repositories
  
---

## 💬 Challenges

- Developing robust ranking algorithms

- Designing intuitive filters and search options

- Optimizing performance for large datasets

- Ensuring scalability and usability

---

## 🎥 Demo

[Click here to watch the demo](https://docs.google.com/file/d/1ZipurEkW6BBZqqNFFvlhPA5LvHzJGGwi/preview)

---

## 📚 References

- [arXiv API](https://info.arxiv.org/help/api/index.html)
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/)
- [Springer Article](https://link.springer.com/article/10.1007/s11192-018-2958-5)
- [CORE Journals](https://ital.corejournals.org/index.php/ital/article/view/9718)

---

## 🤝 Contribution
Contributions are welcome! Feel free to open an issue or submit a pull request.

---

## 💬 Contact

For questions or collaboration opportunities, please reach out via GitHub or [LinkedIn](https://www.linkedin.com/in/steffi-dorothy-9938a21a3/)!

---

## 📄 License
This project is licensed under the MIT License.

---

*Happy Searching!* 🚀
