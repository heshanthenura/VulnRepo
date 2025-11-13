from flask import Flask, request, render_template_string, jsonify
import requests

app = Flask(__name__)

# Internal admin page (only server can access)
@app.route("/admin")
def admin():
    return "Admin Panel: Secret Store Data"

# Homepage: store search
@app.route("/")
def index():
    return """
    <h2>Welcome to FakeStore!</h2>
    <input type="text" id="search-box" placeholder="Search products..." size="40"/>
    <button onclick="search()">Search</button>
    <div id="results"></div>

    <script>
    async function search() {
        const query = document.getElementById('search-box').value;
        // Vulnerable backend API call
        const res = await fetch('/api/search?url=' + encodeURIComponent(query));
        const data = await res.json();
        document.getElementById('results').innerHTML = "<pre>" + data.content + "</pre>";
    }
    </script>
    """

# Vulnerable backend API
@app.route("/api/search")
def api_search():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400
    try:
        # ❌ Vulnerable SSRF: blindly fetches any URL
        r = requests.get(url, timeout=3)
        return jsonify({"url": url, "content": r.text[:500]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
