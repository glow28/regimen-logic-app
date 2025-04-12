# Regimen Logic Visualiser

**Version 4.0** | Built with **Python, Streamlit, and Graphviz**

---

## 🧠 What is this?
This app visualises complex treatment regimens by converting logical strings like:
```
AND or OR OR or AND OR or AND
```
into clean, structured diagrams with logic blocks ("all" vs "exactly-one") and coloured highlights:

- 🔹 **AND + or** nests (deep red)
- 🔹 Flat `or or` = yellow blocks
- 🔹 Single `or` = pink blocks
- 🔹 `OR` = separates regimens (blue blocks)

Each logic token represents how medications are selected:
- `and` = flat combination (non-exclusive)
- `or` = flat alternatives
- `AND` and `or` = nested logic (e.g. combo + choice)
- `OR` = completely separate regimen paths

---

## ⚙️ How it works
- **Streamlit** provides the interactive UI.
- **Graphviz** generates the visual logic diagrams.
- Input is parsed and broken into logic segments using custom rules.
- Component nodes (labelled A-Z) are placed according to logic structure.

---

## 🌐 Deploy / Run Locally
### 1. Clone this repo:
```bash
git clone https://github.com/YOUR_USERNAME/regimen-logic-app
cd regimen-logic-app
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run app
```bash
streamlit run app.py
```

---

## 📄 Files
| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit app |
| `requirements.txt` | Python dependencies |
| `README.md` | You're here |
| `LICENSE` | MIT License (default) |
| `logic_diagram.png` | Generated dynamically |

---

## ✍️ Author
**Created by:** Dr Gloria Esegbona 
Health data scientist & clinical logic tinkerer  


---

## 📅 License
This project is licensed under the **MIT License**. See `LICENSE` for details.

---

## 🔧 TODO / Ideas
- Add download button (PNG / PDF)
- Add logic explainer string (e.g. "Drug A and one of [Drug B or C]")
- Allow user-defined labels (instead of A-Z)
- Export Mermaid syntax or KG JSON
- Add sharing link

---

