from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, timedelta
import database
import scraper

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Main dashboard view"""
    # Get current surplus
    surplus_grains = database.calculate_current_surplus()
    price_per_grain = database.get_latest_rice_price()

    surplus_usd = surplus_grains * price_per_grain if price_per_grain else 0

    # Get recent data
    recent_consumption = database.get_daily_rice(limit=30)
    donations = database.get_donations()
    rice_prices = database.get_rice_prices()

    # Get config
    starting_surplus = database.get_config('starting_surplus_grains', '0')
    starting_date = database.get_config('starting_surplus_date', 'Not set')

    # Calculate total consumed and donated
    all_consumption = database.get_all_daily_rice()
    total_consumed = sum(day['grains'] for day in all_consumption)

    total_donated_usd = sum(d['usd_amount'] for d in donations)
    total_donated_grains = total_donated_usd / price_per_grain if price_per_grain else 0

    # Calculate average daily consumption (last 30 days) and estimate depletion
    avg_daily_consumption = 0
    days_until_depletion = None
    depletion_date = None
    if recent_consumption:
        avg_daily_consumption = sum(day['grains'] for day in recent_consumption) / len(recent_consumption)
        if avg_daily_consumption > 0 and surplus_grains > 0:
            days_until_depletion = int(surplus_grains / avg_daily_consumption)
            depletion_date = datetime.now() + timedelta(days=days_until_depletion)

    return render_template('dashboard.html',
                         surplus_grains=surplus_grains,
                         surplus_usd=surplus_usd,
                         recent_consumption=recent_consumption,
                         donations=donations,
                         rice_prices=rice_prices,
                         starting_surplus=starting_surplus,
                         starting_date=starting_date,
                         total_consumed=total_consumed,
                         total_donated_grains=total_donated_grains,
                         total_donated_usd=total_donated_usd,
                         price_per_grain=price_per_grain,
                         avg_daily_consumption=avg_daily_consumption,
                         days_until_depletion=days_until_depletion,
                         depletion_date=depletion_date)

@app.route('/api/fetch-latest', methods=['POST'])
def fetch_latest():
    """Fetch all missing data up to yesterday"""
    count = scraper.fetch_and_import_missing()
    return jsonify({'success': count > 0, 'count': count})

@app.route('/api/add-donation', methods=['POST'])
def add_donation():
    """Add a new donation"""
    date = request.form.get('date')
    amount = float(request.form.get('amount'))
    donor = request.form.get('donor', '')
    notes = request.form.get('notes', '')

    database.insert_donation(date, amount, donor, notes)
    return redirect(url_for('dashboard'))

@app.route('/api/delete-donation/<int:donation_id>', methods=['POST'])
def delete_donation(donation_id):
    """Delete a donation"""
    database.delete_donation(donation_id)
    return redirect(url_for('dashboard'))

@app.route('/api/add-rice-price', methods=['POST'])
def add_rice_price():
    """Add or update rice price for a year"""
    year = int(request.form.get('year'))
    price = float(request.form.get('price'))
    notes = request.form.get('notes', '')

    database.insert_rice_price(year, price, notes)
    return redirect(url_for('dashboard'))

@app.route('/api/add-manual-rice', methods=['POST'])
def add_manual_rice():
    """Manually add or update a daily rice entry"""
    date = request.form.get('date')
    grains = int(request.form.get('grains'))

    database.insert_daily_rice(date, grains, source='manual')
    return redirect(url_for('dashboard'))

@app.route('/api/chart-data')
def chart_data():
    """Get data for charts"""
    all_consumption = database.get_all_daily_rice()
    donations = database.get_donations()
    starting_surplus = float(database.get_config('starting_surplus_grains', 0))
    price_per_grain = database.get_latest_rice_price()

    # Calculate running surplus over time
    surplus_over_time = []
    current_surplus = starting_surplus

    # Create a dict of donations by date
    donations_by_date = {}
    for d in donations:
        date = d['date']
        grains = d['usd_amount'] / price_per_grain if price_per_grain else 0
        donations_by_date[date] = donations_by_date.get(date, 0) + grains

    # Calculate surplus for each day
    for day in all_consumption:
        date = day['date']

        # Add any donations on this date
        if date in donations_by_date:
            current_surplus += donations_by_date[date]

        # Subtract consumption
        current_surplus -= day['grains']

        surplus_over_time.append({
            'date': date,
            'surplus': int(current_surplus),
            'consumed': day['grains']
        })

    return jsonify(surplus_over_time)

if __name__ == '__main__':
    # Initialize database if needed
    database.init_db()
    app.run(debug=True, port=5000)
