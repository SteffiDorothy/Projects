# CS547-IR Scholarly Search

## 📚 Overview
This project is a scholarly search web application developed for the CS547 Information Retrieval course. The application allows users to search academic papers by keywords, similar to services like Google Scholar, arXiv, and IEEE Xplore. It supports user login, keyword search, and displays ranked results based on relevance.

## 🔍 Features
- **Keyword-based Search**: Search papers by title, abstract, or author names.
- **User Authentication**: Login and registration functionality for users.
- **Paper Metadata**: View paper title, authors, abstract, published date, and access links.

## 🛠️ Tech Stack
- **Backend**: Python 3.13.1, Django 5.1.4
- **Frontend**: Django templates (HTML, CSS)
- **Database**: SQLite3 (Preloaded with arXiv papers)

## 🗂️ Dataset Schema
| Field       | Type   | Description                      |
|-------------|--------|----------------------------------|
| id          | INT    | Unique identifier for each paper|
| title       | TEXT   | Title of the paper               |
| abstract    | TEXT   | Abstract of the paper            |
| authors     | TEXT   | List of authors                  |
| published   | DATE   | Publication date                 |
| url         | TEXT   | URL link to paper (arXiv)         |

## 🚀 Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/sisodiajatin/CS547-IR-Scholarly-Search.git
cd CS547-IR-Scholarly-Search
```

2. **Create and activate a virtual environment**
```bash
python3 -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Apply migrations and load initial data**
```bash
python manage.py migrate
python manage.py loaddata arxiv_papers.sql
```

5. **Run the server**
```bash
python manage.py runserver
```

6. **Access the application**
- Open your browser and navigate to: `http://127.0.0.1:8000/`

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
└── requirements.txt         # Required Python packages
```

## 🤝 Contribution
Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License
This project is licensed under the MIT License.

## 📬 Contact
For any queries, please contact [sisodiajatin](https://github.com/sisodiajatin).

---

*Happy Searching!* 🚀
