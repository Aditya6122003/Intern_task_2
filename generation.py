import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
from fpdf import FPDF # type: ignore
import os

# Step 1: Load the Data
data_file = os.path.join(os.path.dirname(__file__), "C:/Users/admin/Documents/Internship/Task-2/data/Tweets.csv")
data_file = os.path.abspath(data_file)  # Convert to absolute path

try:
    df = pd.read_csv(data_file)
except FileNotFoundError:
    print(f"Error: The file {data_file} was not found. Please check the path.")
    exit()

# Step 2: Data Analysis
total_tweets = len(df)
df["text"] = df["text"].fillna("")  # Replace NaN with empty string
average_tweet_length = df["text"].apply(len).mean()
sentiment_counts = df["sentiment"].value_counts()

# Step 3: Generate a Sentiment Distribution Chart
plt.figure(figsize=(6,4))
sentiment_counts.plot(kind="bar", color=["green", "red", "blue"])
plt.title("Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Tweet Count")
plt.xticks(rotation=0)
chart_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "C:/Users/admin/Documents/Internship/Task-2/output/sentiment_chart.png"))
plt.savefig(chart_path, bbox_inches="tight")

# Step 4: Create a PDF Report
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(200, 10, "Twitter Sentiment Analysis Report", ln=True, align="C")
        self.ln(10)

# Initialize PDF
pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Add Summary
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, f"Total Tweets Analyzed: {total_tweets}", ln=True)
pdf.cell(200, 10, f"Average Tweet Length: {average_tweet_length:.2f} characters", ln=True)
pdf.cell(200, 10, "Sentiment Breakdown:", ln=True)

# Add Table (Sentiment Counts)
pdf.set_font("Arial", size=10)
for sentiment, count in sentiment_counts.items():
    pdf.cell(200, 10, f"{sentiment}: {count} tweets", ln=True)

# Insert Chart
pdf.image(chart_path, x=50, w=100)

# Save PDF
pdf_output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "C:/Users/admin/Documents/Internship/Task-2/output/report.pdf"))
pdf.output(pdf_output_path)

print(f"✅ Report generated successfully! Check: {pdf_output_path}")
