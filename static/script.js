const searchBtn = document.getElementById('searchBtn');
const generateBtn = document.getElementById('generateBtn');
const searchType = document.getElementById('searchType');
const searchInput = document.getElementById('searchInput');
const billResultsDiv = document.getElementById('billResults');
const outputArea = document.getElementById('outputArea');
const modeSelect = document.getElementById('mode');

let foundBills = [];

searchBtn.addEventListener('click', async () => {
  billResultsDiv.innerHTML = 'Loading...';
  foundBills = [];

  const type = searchType.value; // 'state' or 'federal'
  const keyword = encodeURIComponent(searchInput.value.trim());

  let url = '';
  if (type === 'state') {
    // For state, user might input "Colorado"
    // or "New York" or "Texas"
    url = `/api/state_bills?state=${keyword}&keyword=${keyword}`;
  } else {
    // Federal
    url = `/api/federal_bills?keyword=${keyword}`;
  }

  try {
    const res = await fetch(url);
    const data = await res.json();

    if (data.error) {
      billResultsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
      return;
    }

    foundBills = data; // store globally
    renderBills(data);

  } catch (err) {
    console.error(err);
    billResultsDiv.innerHTML = `<p>Error fetching bills</p>`;
  }
});

function renderBills(bills) {
  if (!Array.isArray(bills) || bills.length === 0) {
    billResultsDiv.innerHTML = '<p>No bills found.</p>';
    return;
  }
  let html = '<ul>';
  bills.forEach((bill, i) => {
    // For OpenStates data, we might have "title" or "displayName"
    // For GovTrack, we might have "title" or "short_title"
    const title = bill.title || bill.displayName || 'No Title';
    const summary = bill.summary || bill.description || 'No summary available.';
    html += `<li><strong>${title}</strong><br><em>${summary}</em></li><br>`;
  });
  html += '</ul>';
  billResultsDiv.innerHTML = html;
}

generateBtn.addEventListener('click', async () => {
  if (foundBills.length === 0) {
    outputArea.innerHTML = '<p>No bills to summarize. Please search first.</p>';
    return;
  }

  outputArea.innerHTML = 'Generating...';

  // We'll pass the array of found bills, with some normalized shape
  // In a real project, you'd parse out relevant fields or do more data cleaning
  const billsForGPT = foundBills.map(b => {
    return {
      title: b.title || b.displayName || 'No Title',
      summary: b.summary || b.description || 'No summary found.'
    };
  });

  const mode = modeSelect.value;

  const body = {
    bills: billsForGPT,
    mode: mode,
    topic: searchInput.value || 'Policy Issue'
  };

  try {
    const res = await fetch('/api/generate_summary', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(body)
    });
    const data = await res.json();
    outputArea.innerHTML = `<pre>${data.output}</pre>`;
  } catch (err) {
    console.error(err);
    outputArea.innerHTML = `<p>AI generation error</p>`;
  }
});

