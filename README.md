# Football Statistics – Football Project (Data Ingestion)

This repository contains the application responsible for **football match statistics data ingestion**, as part of the **Football Performance & Financial Control** project.

The application was developed to replace manual spreadsheet updates, ensuring standardized, reliable, and structured data collection.

---

## Project Objective

Provide a simple and reliable interface for registering individual and overall football statistics, including number of wins, goals scored, goals conceded, attendance, and other metrics, aiming to eliminate the use of spreadsheets, increase data reliability, and facilitate information updates and maintenance.

This repository focuses **exclusively on football statistical data ingestion**, and does not include visualizations or analytical business rules.

---

## Features

- Data entry form built with **Streamlit**
- Structured selection of:
  - Player
  - Team
  - Match
- Registration of:
  - Goals scored
  - Goals conceded
- Direct write to **PostgreSQL database (Supabase)**
- Reduced manual errors and spreadsheet dependency

---

## Technologies Used

- Python
- Streamlit
- PostgreSQL
- Supabase
- SQL

---

## Repository Structure

Estatisticas_Pelada/
│── app.py
│── requirements.txt
│── runtime.txt
│── .streamlit/
│   └── config.toml

---

## Data Flow

1. User submits match statistics via Streamlit form  
2. Data is validated and standardized  
3. Records are stored directly in PostgreSQL  
4. Data becomes available for Power BI analysis  

---

## Related Project

This repository is part of the larger project:

**Football Performance & Financial Control – End-to-End Data Project**

The main portfolio repository provides an overview of the full solution and related modules.

---

##  Notes

This project was designed to allow non-technical users to register statistical data without direct interaction with databases or spreadsheets.

