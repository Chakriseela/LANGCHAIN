# =========================
# 1. INSTALL DEPENDENCIES
# =========================
# !pip install -q langchain langchain-community langchain-text-splitters
# !pip install -q faiss-cpu pypdf pandas matplotlib seaborn
# !pip install -q google-genai reportlab


# =========================
# 2. IMPORTS
# =========================
import os
from dotenv import load_dotenv
load_dotenv()
from google import genai

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


# =========================
# 3. GEMINI CLIENT
# =========================
client = genai.Client(api_key= os.getenv("GOOGLE_API_KEY"))


# =========================
# 4. LOAD PDFs
# =========================
japi_path = "/content/visualization_RAG/JAPI2015_TablesGraphs_Rev.pdf"
expense_path = "/content/visualization_RAG/Chakravarthi_Expense_Report.pdf"

docs = PyPDFLoader(japi_path).load() + PyPDFLoader(expense_path).load()


# =========================
# 5. CHUNKING
# =========================
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)
chunks = splitter.split_documents(docs)


# =========================
# 6. VECTOR DB (FAISS)
# =========================
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.from_documents(chunks, embeddings)
retriever = db.as_retriever(search_kwargs={"k": 5})


# =========================
# 7. PROMPT ENGINE (TRAINED DATA FORMAT)
# =========================
def build_prompt(context, question):
    return f"""
You are an AI financial analyst.

Return structured output:
1. TABLE REPORT
2. ANALYSIS
3. INSIGHTS
4. VISUALIZATION PLAN

Context:
{context}

Question:
{question}
"""


# =========================
# 8. RAG FUNCTION
# =========================
def ask_rag(question):
    docs = retriever.invoke(question)
    context = "\n".join([d.page_content for d in docs])

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=build_prompt(context, question)
    )

    return response.text


# =========================
# 9. DATA EXTRACTION (SAFE VERSION)
# =========================
def extract_data(text):
    words = re.findall(r"[A-Za-z]+", text)
    nums = re.findall(r"\d+", text)

    if len(nums) == 0:
        nums = ["1"] * len(words)

    df = pd.DataFrame({
        "category": words[:len(nums)],
        "value": list(map(int, nums[:len(words)]))
    })

    return df


# =========================
# 10. AI EXPLANATION
# =========================
def explain_chart(title, data):
    prompt = f"""
Explain this chart in 2 lines professionally.

Chart: {title}
Data: {data}
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text


# =========================
# 11. VISUALIZATION ENGINE (FIXED)
# =========================
report_items = []

def generate_charts(df):

    grouped = df.groupby("category")["value"].sum()

    # ---------------- BAR ----------------
    plt.figure(figsize=(8,5))
    grouped.plot(kind="bar")
    plt.title("Figure 1: Bar Chart - Expense Distribution")
    plt.tight_layout()

    bar_path = "/content/bar.png"
    plt.savefig(bar_path)
    plt.show()

    exp = explain_chart("Bar Chart", grouped.to_dict())
    print("\n🧠 Explanation:\n", exp)

    report_items.append((bar_path, "Figure 1: Bar Chart", exp))


    print("\n" + "="*80 + "\n")


    # ---------------- PIE ----------------
    plt.figure(figsize=(6,6))
    grouped.plot(kind="pie", autopct="%1.1f%%")
    plt.title("Figure 2: Pie Chart - Expense Share")
    plt.ylabel("")
    plt.tight_layout()

    pie_path = "/content/pie.png"
    plt.savefig(pie_path)
    plt.show()

    exp = explain_chart("Pie Chart", grouped.to_dict())
    print("\n🧠 Explanation:\n", exp)

    report_items.append((pie_path, "Figure 2: Pie Chart", exp))


    print("\n" + "="*80 + "\n")


    # ---------------- LINE ----------------
    plt.figure(figsize=(8,5))
    df["value"].plot(kind="line", marker="o")
    plt.title("Figure 3: Line Chart - Trend")
    plt.tight_layout()

    line_path = "/content/line.png"
    plt.savefig(line_path)
    plt.show()

    exp = explain_chart("Line Chart", df["value"].tolist())
    print("\n🧠 Explanation:\n", exp)

    report_items.append((line_path, "Figure 3: Line Chart", exp))


# =========================
# 12. PDF REPORT GENERATION
# =========================
def create_pdf(items, output="AI_Report.pdf"):

    doc = SimpleDocTemplate(output)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("AI Generated Financial Report", styles["Title"]))
    content.append(Spacer(1, 12))

    for img, title, exp in items:
        content.append(Paragraph(title, styles["Heading2"]))
        content.append(Image(img, width=400, height=250))
        content.append(Spacer(1, 8))
        content.append(Paragraph(exp, styles["Normal"]))
        content.append(Spacer(1, 20))

    doc.build(content)
    return output


# =========================
# 13. RUN PIPELINE
# =========================
query = "Analyze expense report and generate structured insights"

print("\n===== RAG OUTPUT =====\n")
print(ask_rag(query))


expense_text = "\n".join([d.page_content for d in PyPDFLoader(expense_path).load()])
df = extract_data(expense_text)

generate_charts(df)

pdf_file = create_pdf(report_items)

print("\n✅ PDF GENERATED:", pdf_file)