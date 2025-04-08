# TCP Policy Agent

**An AI-powered civic tech tool that helps youth organizers turn real-time legislation into action.**  
Built by [TheCHANGEproject](https://thechangeproject.org), this open-source agent fetches live state and federal policy language and transforms it into student-friendly briefs, outreach scripts, and organizing tools.

---

## What It Does

TCP Policy Agent empowers students and community organizers by:

- 🔍 Fetching live bills from **Congress** and **state legislatures**
- 📝 Generating **policy briefs** from raw legislation
- 📬 Writing **email and phone scripts** to contact lawmakers
- 🧾 Drafting **resolutions** and campaign talking points
- 🧭 Providing week-by-week **organizing roadmaps**

It’s civic power—made accessible.

---

## Tech Stack

- **Flask** for backend API
- **OpenStates API** for state bills
- **GovTrack API** for federal bills
- **OpenAI GPT-4o (coming soon)** for summaries + campaign tools
- **React.js** frontend (planned)

---

## Getting Started

### 🔧 Requirements

- Python 3.10+
- Flask
- OpenStates API Key

### Install & Run

```bash
git clone https://github.com/YOUR_USERNAME/tcp-policy-agent.git
cd tcp-policy-agent
pip install -r requirements.txt
