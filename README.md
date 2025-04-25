## 📚 Edu-Dashboard
An interactive Education Dashboard built with Streamlit and powered by MongoDB Atlas.

Visualize, explore, and compare student exam results from different years, counties, and nationalities!

# 🚀 Features
📊 Compare top 10 schools across two different Finals years

🌍 Compare average scores between different nationalities

🏫 Search students by School Name or Code

📅 Switch between grades and finals datasets

📈 Display detailed rankings and statistics

🌐 Powered by MongoDB Atlas and Streamlit Cloud

🔐 Secure database connection with Streamlit Secrets Management

# 🛠 Technologies Used
- Python 3.12+

- Streamlit

- Pandas

- Matplotlib

- MongoDB Atlas (Remote cloud database)

- Pymongo

## ⚡ Quickstart Guide
Clone the project:

```bash

git clone https://github.com/<your-username>/edu-dashboard.git
cd edu-dashboard
```

Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
.\venv\Scripts\activate  # on Windows
source venv/bin/activate  # on Linux/Mac
```

Install required packages:

```bash

pip install -r requirements.txt
```
Create .streamlit/secrets.toml (for local testing):

```toml

MONGO_URI = "mongodb+srv://<your-user>:<your-password>@cluster0.k4vh3mz.mongodb.net/edu_dashboard?retryWrites=true&w=majority&appName=Cluster0"
```
Run the app locally:

```bash
streamlit run main.py
```
Deploy to Streamlit Cloud:

- Push to GitHub

- Set up your Streamlit Cloud project

- Add your MONGO_URI in Streamlit Settings → Secrets

- Deploy and enjoy! 🚀

📂 Project Structure
```bash

/edu-dashboard
├── .streamlit/
│   └── secrets.toml (local testing only)
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```
📝 Notes
- MongoDB Atlas is required (no local MongoDB)

- Make sure your Atlas cluster has your IP whitelisted (or 0.0.0.0/0 for public access)

- Handle your database URI securely using Streamlit Secrets!

✨ Screenshots

Dashboard Example	School Comparison	Nationality Comparison
(Add your screenshots if you want!)

📧 Contact
Feel free to contact me if you have questions or ideas!
→ Csipor Antal
