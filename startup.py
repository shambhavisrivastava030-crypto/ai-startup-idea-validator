

from google import genai
import mysql.connector
import sys

# ==============================
# 🔐 CONFIGURATION
# ==============================

GEMINI_API_KEY = "AIzaSyCjaxakn-46O3QSwuwNDg7AWBZpGvw6Ka4"

# ==============================
# 🤖 GEMINI CLIENT
# ==============================

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    print("❌ Gemini Setup Error:", e)
    sys.exit()

# ==============================
# 🗄️ MYSQL CONNECTION
# ==============================

try:
    db = mysql.connector.MySQLConnection(
        host="localhost",
        user="root",
        password="RadheRadhe12",
        database="startup"
    )
    cursor = db.cursor()
    print("✅ Database Connected Successfully.")
except Exception as e:
    print("❌ MySQL Connection Error:", e)
    sys.exit()


# ==============================
# 🚀 STARTUP VALIDATOR FUNCTION
# ==============================

def run_validator():
    user_idea = input("\n>>> Enter your Startup Idea: ").strip()

    if not user_idea:
        print("⚠ Please enter a valid idea.")
        return

    print("\n🤖 AI is analyzing your idea... Please wait...\n")

    prompt = f"""
You are an AI Startup Idea Validator.

Analyze the following startup idea and provide a structured report with:

1. Problem Statement
2. Target Customers
3. Market Opportunity
4. Competitors
5. Suggested Tech Stack
6. Risk Level (Low/Medium/High)
7. Profitability Score (0-10)

Startup Idea: {user_idea}

Format clearly with headings.
"""

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        ai_report = response.text

        # Save to MySQL
        sql = "INSERT INTO startup_idea (user_input, ai_report) VALUES (%s, %s)"
        cursor.execute(sql, (user_idea, ai_report))
        db.commit()

        print("✅ Report Generated & Saved Successfully!\n")
        print("=" * 60)
        print(ai_report)
        print("=" * 60)

    except Exception as e:
        print("❌ AI Error:", e)


# ==============================
# 📊 DASHBOARD FUNCTION
# ==============================

def show_dashboard():
    print("\n" + "=" * 60)
    print("              🚀 STARTUP DASHBOARD")
    print("=" * 60)

    try:
        cursor.execute(
            "SELECT id, user_input, created_at FROM startup_idea ORDER BY id DESC LIMIT 10"
        )
        rows = cursor.fetchall()

        if not rows:
            print("No startup idea found.")
            return

        for row in rows:
            print(f"ID: {row[0]}")
            print(f"Idea: {row[1]}")
            print(f"Date: {row[2]}")
            print("-" * 60)

    except Exception as e:
        print("❌ Dashboard Error:", e)


# ==============================
# ▶ MAIN PROGRAM
# ==============================

if __name__ == "__main__":
    run_validator()
    show_dashboard()
    input("\nPress Enter to exit...")
