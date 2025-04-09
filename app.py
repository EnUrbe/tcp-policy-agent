import os
import openai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import logging

# Import services
from services.openstates_api import search_state_bills
from services.congress_api import search_federal_bills

# Load .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    """
    Serve our simple front-end page.
    """
    return render_template('index.html')

@app.route('/api/state_bills', methods=['GET'])
def api_state_bills():
    state = request.args.get('state')
    keyword = request.args.get('keyword')
    
    # Validate inputs
    if not state or not keyword:
        logging.error("Missing 'state' or 'keyword' parameter")
        return jsonify({"error": "Missing 'state' or 'keyword' parameter"}), 400
    
    try:
        results = search_state_bills(state, keyword)
        return jsonify(results)
    except Exception as e:
        logging.error(f"Error searching state bills: {e}")
        return jsonify({"error": "Failed to retrieve state bills"}), 500

@app.route('/api/federal_bills', methods=['GET'])
def api_federal_bills():
    keyword = request.args.get('keyword')
    
    # Validate inputs
    if not keyword:
        logging.error("Missing 'keyword' parameter")
        return jsonify({"error": "Missing 'keyword' parameter"}), 400
    
    try:
        results = search_federal_bills(keyword)
        return jsonify(results)
    except Exception as e:
        logging.error(f"Error searching federal bills: {e}")
        return jsonify({"error": "Failed to retrieve federal bills"}), 500

@app.route('/api/generate_summary', methods=['POST'])
def generate_summary():
    """
    Generate a policy brief or email script using GPT based on bill data.
    Expects JSON with keys:
    {
      "bills": [ {title, summary} ],
      "mode": "brief" or "email",
      "topic": "Mental Health" (optional)
    }
    """
    data = request.get_json()
    
    # Validate inputs
    if not data or not isinstance(data, dict):
        logging.error("Invalid input data")
        return jsonify({"error": "Invalid input data"}), 400
    
    bills = data.get("bills", [])
    mode = data.get("mode", "brief")
    topic = data.get("topic", "Policy Issue")

    # Build a text block from the bills
    all_bill_info = ""
    for i, bill in enumerate(bills):
        t = bill.get("title", "No Title")
        desc = bill.get("summary", "No summary available.")
        all_bill_info += f"Bill {i+1}: {t}\nSummary: {desc}\n\n"

    prompt = create_prompt(all_bill_info, mode, topic)

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=600,
            temperature=0.7
        )
        generated_text = response["choices"][0]["text"].strip()
        return jsonify({"output": generated_text})
    except Exception as e:
        logging.error(f"Error generating summary: {e}")
        return jsonify({"error": "Failed to generate summary"}), 500

def create_prompt(bill_info, mode, topic):
    """
    Construct a prompt for GPT based on user mode: 'brief' or 'email'.
    """
    if mode == "brief":
        return f"""You are a helpful policy assistant. 
Given these bills about {topic}, create a concise policy brief that includes:
1) Background
2) Key points from the legislation
3) Potential impact on youth or marginalized communities
4) A short conclusion with recommended actions

Here is the relevant info:
{bill_info}

Now generate a policy brief (about 400 words)."""
    elif mode == "email":
        return f"""You are a helpful policy assistant.
Given these bills about {topic}, please write a short, persuasive email script 
to a local legislator. The email should:
1) Introduce the writer as a concerned student or community member
2) Cite 1-2 specifics from the bills
3) Politely but firmly request support or changes
4) Close with a call to action

Here is the relevant info:
{bill_info}

Now generate the email script."""
    else:
        return f"Summarize the following legislation:\n{bill_info}"

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
