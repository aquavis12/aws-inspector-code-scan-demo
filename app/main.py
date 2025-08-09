#!/usr/bin/env python3
import subprocess
import ldap3
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Vulnerable Demo App</h1>
    <h2>XSS Test</h2>
    <form action="/search" method="get">
        <input type="text" name="q" placeholder="Enter search term">
        <button type="submit">Search</button>
    </form>
    <p>Try: &lt;script&gt;alert('XSS')&lt;/script&gt;</p>
    
    <h2>Command Injection Test</h2>
    <form action="/ping" method="get">
        <input type="text" name="host" placeholder="Enter hostname" value="localhost">
        <button type="submit">Ping</button>
    </form>
    <p>Try: localhost; whoami</p>
    
    <h2>LDAP Injection Test</h2>
    <form action="/ldap" method="get">
        <input type="text" name="username" placeholder="Enter username">
        <button type="submit">LDAP Search</button>
    </form>
    <p>Try: admin)(&(objectClass=*</p>
    '''

# Vulnerable: XSS
@app.route('/search')
def search():
    query = request.args.get('q', '')
    # Vulnerable: Unescaped user input
    template = f"<h1>Search Results for: {query}</h1><p>No results found.</p>"
    return render_template_string(template)

# Vulnerable: Command Injection
@app.route('/ping')
def ping():
    host = request.args.get('host', 'localhost')
    # Vulnerable: Direct command execution without sanitization
    try:
        result = subprocess.run(f"ping -n 1 {host}", shell=True, capture_output=True, text=True, timeout=10)
        return f"<h2>Ping Results:</h2><pre>{result.stdout}</pre><pre>{result.stderr}</pre>"
    except Exception as e:
        return f"<h2>Error:</h2><p>{str(e)}</p>"

# Vulnerable: LDAP Injection
@app.route('/ldap')
def ldap_search():
    username = request.args.get('username', '')
    if not username:
        return "<h2>Please provide a username</h2>"
    
    # Vulnerable: Direct string concatenation in LDAP filter
    ldap_filter = f"(&(objectClass=user)(sAMAccountName={username}))"
    
    try:
        # Mock LDAP search (would normally connect to real LDAP server)
        return f'''
        <h2>LDAP Search Results:</h2>
        <p>Filter used: <code>{ldap_filter}</code></p>
        <p>Searching for user: {username}</p>
        <p><em>Note: This is a mock response. In real scenario, this would query LDAP server.</em></p>
        '''
    except Exception as e:
        return f"<h2>LDAP Error:</h2><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)