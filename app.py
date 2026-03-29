import os
import json
import gspread
from flask import Flask, render_template, request
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets API scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from Render Environment Variable
creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open your Google Sheet
sheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1R6E_iztm2hbWsBd3b1TXrVAPDfZfva6aAROqXnz1o_4/edit"
).sheet1


@app.route("/", methods=["GET", "POST"])
def index():
    data = sheet.get_all_records()
    message = ""

    # Get unique villages for dropdown
    villages = sorted(list(set(row["Owner Village"] for row in data)))

    if request.method == "POST":
        selected_village = request.form["village"]
        tag_id = request.form["tag_id"]

        # Check if tag exists for selected village
        for row in data:
            if row["Owner Village"] == selected_village and str(row["Tag ID"]) == tag_id:
                message = "✅ Tag Found!"
                break
        else:
            message = "❌ Tag Not Found!"

    return render_template("index.html", villages=villages, message=message)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)