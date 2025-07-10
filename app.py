from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import io
import csv
from collections import defaultdict

app = Flask(__name__)

# Store expenses in a JSON file
EXPENSES_FILE = 'expenses.json'

def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(EXPENSES_FILE, 'w') as f:
        json.dump(expenses, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    expenses = load_expenses()
    return jsonify(expenses)

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.json
    expenses = load_expenses()
    
    expense = {
        'id': len(expenses) + 1,
        'date': data['date'],
        'amount': float(data['amount']),
        'category': data['category'],
        'place': data['place'],
        'description': data['description'],
        'timestamp': datetime.now().isoformat()
    }
    
    expenses.append(expense)
    save_expenses(expenses)
    
    return jsonify({'success': True, 'expense': expense})

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expenses = load_expenses()
    expenses = [e for e in expenses if e['id'] != expense_id]
    save_expenses(expenses)
    return jsonify({'success': True})

@app.route('/api/charts')
def get_charts():
    expenses = load_expenses()
    
    if not expenses:
        return jsonify({'category_chart': None, 'daily_chart': None})
    
    # Category chart
    category_totals = defaultdict(float)
    for expense in expenses:
        category_totals[expense['category']] += expense['amount']
    
    category_fig = go.Figure(data=[go.Pie(
        labels=list(category_totals.keys()),
        values=list(category_totals.values()),
        title='Spending by Category'
    )])
    category_fig.update_layout(height=400)
    
    # Daily chart
    daily_totals = defaultdict(float)
    for expense in expenses:
        daily_totals[expense['date']] += expense['amount']
    
    sorted_dates = sorted(daily_totals.keys())
    daily_amounts = [daily_totals[date] for date in sorted_dates]
    
    daily_fig = go.Figure(data=[go.Scatter(
        x=sorted_dates,
        y=daily_amounts,
        mode='lines+markers',
        name='Daily Spending',
        line=dict(color='#4facfe', width=3),
        marker=dict(size=8)
    )])
    daily_fig.update_layout(
        title='Daily Spending Trend',
        height=400,
        xaxis_title='Date',
        yaxis_title='Amount ($)'
    )
    
    return jsonify({
        'category_chart': json.dumps(category_fig, cls=PlotlyJSONEncoder),
        'daily_chart': json.dumps(daily_fig, cls=PlotlyJSONEncoder)
    })

@app.route('/api/stats')
def get_stats():
    expenses = load_expenses()
    
    if not expenses:
        return jsonify({
            'total_spent': 0,
            'daily_average': 0,
            'total_expenses': 0,
            'top_category': '-'
        })
    
    total = sum(expense['amount'] for expense in expenses)
    unique_dates = list(set(expense['date'] for expense in expenses))
    daily_average = total / len(unique_dates) if unique_dates else 0
    
    category_totals = {}
    for expense in expenses:
        category = expense['category']
        category_totals[category] = category_totals.get(category, 0) + expense['amount']
    
    top_category = max(category_totals, key=category_totals.get) if category_totals else '-'
    
    return jsonify({
        'total_spent': round(total, 2),
        'daily_average': round(daily_average, 2),
        'total_expenses': len(expenses),
        'top_category': top_category
    })

@app.route('/api/export')
def export_data():
    expenses = load_expenses()
    
    if not expenses:
        return jsonify({'error': 'No expenses to export'})
    
    output = io.StringIO()
    fieldnames = ['id', 'date', 'amount', 'category', 'place', 'description', 'timestamp']
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    writer.writeheader()
    for expense in expenses:
        writer.writerow(expense)
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='family-trip-expenses.csv'
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)