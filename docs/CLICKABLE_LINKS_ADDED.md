# Clickable Source Links Added! 🔗

## What's New

All source citations and references now have clickable links that open the full policy documents!

## Features Added

### 1. Citation Links in Answers

- Each citation now has a clickable title
- Opens the full policy document in a new tab
- Shows an external link icon for clarity

### 2. Recent Sources Sidebar

- Source links in the sidebar are now clickable
- Opens the corresponding policy document
- Includes external link icon

### 3. New API Endpoint

- `/policy/<filename>` - Serves policy documents
- Secure: Only serves files from the `policies/` directory
- Supports markdown files

## How It Works

### Backend Changes

1. **New Route in `app.py`:**

   ```python
   @app.route('/policy/<path:filename>')
   def serve_policy(filename):
       # Serves policy files securely
   ```

2. **Enhanced Citations in `src/rag.py`:**
   - Added `filename` field
   - Added `url` field pointing to `/policy/{filename}`

### Frontend Changes

1. **Updated `static/app.js`:**
   - Citations now render as clickable links
   - Recent sources are clickable
   - External link icons added

2. **Updated `static/style.css`:**
   - Styled citation links with hover effects
   - Added external link icon styling

## Example URLs

When the app is running, you can access:

- http://localhost:5000/policy/employee-handbook.md
- http://localhost:5000/policy/pto-policy.md
- http://localhost:5000/policy/remote-work-policy.md
- http://localhost:5000/policy/expense-policy.md
- http://localhost:5000/policy/security-policy.md

## User Experience

### Before:

```
Sources:
  Pto Policy
  "Paid Time Off (PTO) Policy Overview..."
  From: policies\pto-policy.md
```

### After:

```
Sources:
  Pto Policy 🔗  (clickable!)
  "Paid Time Off (PTO) Policy Overview..."
  From: pto-policy.md
```

## Security

- Only files from the `policies/` directory can be accessed
- Path traversal attacks are prevented
- Files are served with proper content types

## Testing

Run the test to verify all links work:

```bash
python test_links.py
```

## Start the App

```bash
python app.py
```

Then try asking:

- "How many vacation days do I get?"
- Click on the "Pto Policy" link in the sources
- The full policy document will open in a new tab!

## Benefits

1. ✅ Users can verify information by reading the full document
2. ✅ Better transparency and trust
3. ✅ Easy access to complete policy details
4. ✅ Professional user experience
5. ✅ Meets citation requirements for academic/professional use

Enjoy the enhanced citation experience! 🎉
