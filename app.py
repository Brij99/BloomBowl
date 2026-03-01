from flask import Flask, render_template, request, flash, redirect, url_for, make_response
from datetime import datetime
import random
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bloombowl-fresh-2026'

# Temporary storage for bulk receipt results (PRG pattern)
BULK_RESULTS = {}

# ─── Menu Data ────────────────────────────────────────────────────────────────

MENU = {
    'sprout_bowls': {
        'title': 'Sprout Bowls',
        'icon': '🌱',
        'description': 'Fresh, nutritious sprouts packed with protein and vitamins',
        'image': 'sprout_bowl.png',
        'products': [
            {'name': 'Sprouts Bowl (With Salad)', 'price': 55, 'popular': True,
             'desc': 'Fresh moong sprouts topped with crunchy salad, onion, tomato & tangy lemon dressing'},
            {'name': 'Sprouts Bowl (Plain)', 'price': 45, 'popular': False,
             'desc': 'Simple and wholesome steamed sprouts with light seasoning'},
            {'name': 'Chana Bowl (With Salad)', 'price': 55, 'popular': True,
             'desc': 'Protein-rich chana (chickpea) sprouts with fresh garden salad'},
            {'name': 'Peanut (Sing) Bowl', 'price': 55, 'popular': False,
             'desc': 'Crunchy boiled peanuts with spices, onion & fresh herbs'},
            {'name': 'Mix Bowl (Sprouts & Chana)', 'price': 55, 'popular': True,
             'desc': 'Best of both worlds — mixed moong sprouts and chana with salad'},
        ]
    },
    'bloom_special': {
        'title': 'Bloom Bowl Special',
        'icon': '⭐',
        'description': 'Our signature creation — the ultimate healthy bowl',
        'image': 'sprout_bowl.png',
        'products': [
            {'name': 'Bloom Bowl Special', 'price': 70, 'popular': True,
             'desc': 'Our signature bowl with sprouts, chana, peanuts, salad, special dressing & toppings'},
            {'name': 'Sweetcorn Salad', 'price': 60, 'popular': True,
             'desc': 'Sweet golden corn kernels tossed with fresh veggies and zesty dressing'},
            {'name': 'Sweetcorn Butter', 'price': 50, 'popular': False,
             'desc': 'Hot buttered sweetcorn with a sprinkle of spices'},
            {'name': 'Sweetcorn Plain', 'price': 40, 'popular': False,
             'desc': 'Simple steamed sweetcorn — pure and natural'},
        ]
    },
    'fruit_bowls': {
        'title': 'Fruit Bowls',
        'icon': '🍓',
        'description': 'Seasonal fruits bursting with natural sweetness',
        'image': 'fruit_bowl.png',
        'products': [
            {'name': 'Small Bowl', 'price': 80, 'popular': False,
             'desc': 'A refreshing mix of seasonal fresh fruits — perfect light snack'},
            {'name': 'Big Bowl', 'price': 100, 'popular': True,
             'desc': 'Generous portion of assorted seasonal fruits — a feast of freshness'},
        ]
    },
    'paneer_bowls': {
        'title': 'Paneer Bowls',
        'icon': '🧀',
        'description': 'Protein-packed bowls with fresh paneer cubes',
        'image': 'paneer_bowl.png',
        'products': [
            {'name': 'Sprout / Chana / Peanut Bowl with Paneer', 'price': 100, 'popular': True,
             'desc': 'Your choice of sprout, chana, or peanut bowl topped with fresh paneer cubes'},
            {'name': 'Mix Bowl Paneer', 'price': 110, 'popular': False,
             'desc': 'Mixed sprouts and chana bowl loaded with paneer cubes & dressing'},
            {'name': 'Bloombowl with Paneer', 'price': 120, 'popular': True,
             'desc': 'Our signature Bloom Bowl elevated with generous paneer — the ultimate bowl'},
        ]
    }
}

# Build flat menu item list for receipt dropdown
ALL_ITEMS = []
for cat in MENU.values():
    for p in cat['products']:
        ALL_ITEMS.append({'name': p['name'], 'price': p['price']})

TESTIMONIALS = [
    {'name': 'Priya S.', 'text': 'The Bloom Bowl Special is my go-to breakfast! Fresh, healthy, and incredibly delicious. Love the quality!', 'rating': 5},
    {'name': 'Rahul M.', 'text': 'Best sprout bowls in town! The mix bowl with paneer is absolutely amazing. Highly recommend!', 'rating': 5},
    {'name': 'Anita K.', 'text': 'Finally a healthy food option that actually tastes great. The fruit bowls are always fresh and generous.', 'rating': 5},
    {'name': 'Vikram P.', 'text': 'Started my fitness journey with BloomBowl. The sweetcorn salad is a game-changer. Keep it up!', 'rating': 4},
]


@app.route('/')
def index():
    return render_template('index.html', menu=MENU, testimonials=TESTIMONIALS)


@app.route('/order', methods=['POST'])
def order():
    name = request.form.get('name', '')
    phone = request.form.get('phone', '')
    items = request.form.get('items', '')
    if name and phone:
        flash(f'Thank you {name}! Your order has been received. We will call you on {phone} to confirm. 🎉', 'success')
    else:
        flash('Please fill in all required fields.', 'error')
    return redirect(url_for('index', _anchor='order'))


@app.route('/receipt', methods=['GET', 'POST'])
def receipt():
    receipt_data = None
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', 'Customer')
        customer_phone = request.form.get('customer_phone', '')
        payment_method = request.form.get('payment_method', 'Cash')

        # Collect line items
        item_names = request.form.getlist('item_name[]')
        item_qtys = request.form.getlist('item_qty[]')
        item_prices = request.form.getlist('item_price[]')

        line_items = []
        subtotal = 0
        for name, qty, price in zip(item_names, item_qtys, item_prices):
            if name and qty and price:
                q = int(qty)
                p = float(price)
                total = q * p
                subtotal += total
                line_items.append({
                    'name': name,
                    'qty': q,
                    'price': p,
                    'total': total
                })

        if line_items:
            receipt_num = f"BB-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
            receipt_data = {
                'receipt_num': receipt_num,
                'date': datetime.now().strftime('%B %d, %Y'),
                'time': datetime.now().strftime('%I:%M %p'),
                'customer_name': customer_name,
                'customer_phone': customer_phone,
                'payment_method': payment_method,
                'line_items': line_items,
                'subtotal': subtotal,
                'total': subtotal,
            }
        else:
            flash('Please add at least one item to generate a receipt.', 'error')

    return render_template('receipt.html', receipt=receipt_data, menu_items=ALL_ITEMS)


@app.route('/bulk-receipt', methods=['GET', 'POST'])
def bulk_receipt():
    receipts = []
    summary = None

    if request.method == 'GET':
        # Check if there are results from a POST redirect
        rid = request.args.get('rid')
        if rid and rid in BULK_RESULTS:
            data = BULK_RESULTS.pop(rid)  # Consume once — old data auto-deleted
            receipts = data['receipts']
            summary = data['summary']
        response = make_response(render_template('bulk_receipt.html', receipts=receipts, summary=summary))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    # POST — process uploaded file or pasted data
    paste_data = request.form.get('paste_data', '').strip()
    file = request.files.get('excel_file')

    try:
        import re
        from collections import defaultdict

        rows_data = []  # list of lists (each row = list of cell values)

        if paste_data:
            # Parse pasted tab-separated data
            lines = paste_data.split('\n')
            for line in lines:
                line = line.strip('\r')
                if not line.strip():
                    continue
                # Split by tab
                cells = line.split('\t')
                rows_data.append(cells)

            if len(rows_data) < 2:
                flash('Please paste at least a header row and one data row.', 'error')
                return redirect(url_for('bulk_receipt'))

        elif file and file.filename:
            if not file.filename.endswith(('.xlsx', '.xls')):
                flash('Please upload a valid Excel file (.xlsx or .xls).', 'error')
                return redirect(url_for('bulk_receipt'))

            import openpyxl
            wb = openpyxl.load_workbook(file, data_only=True)
            ws = wb.active

            for row in ws.iter_rows(values_only=True):
                rows_data.append([cell for cell in row])

            if len(rows_data) < 2:
                flash('Excel file has no data rows.', 'error')
                return redirect(url_for('bulk_receipt'))
        else:
            flash('Please upload an Excel file or paste data.', 'error')
            return redirect(url_for('bulk_receipt'))

        # Parse headers from first row
        raw_headers = rows_data[0]
        headers = []
        for cell in raw_headers:
            if cell is not None and str(cell).strip():
                h = str(cell).strip().lower()
                h = re.sub(r'[^\x20-\x7e]', '', h).strip()
                headers.append(h)
            else:
                headers.append('')

        # Detect column indices with flexible matching
        name_col = None
        item_col = None
        qty_col = None
        price_col = None
        amount_col = None
        phone_col = None
        date_col = None

        for i, h in enumerate(headers):
            if not h:
                continue
            # Customer / Name column
            if name_col is None and h in ('name', 'customer', 'customer name', 'customer_name', 'client', 'buyer'):
                name_col = i
            # Item / Product column
            elif item_col is None and h in ('item', 'product', 'item name', 'item_name', 'order', 'description', 'product name', 'product_name', 'items', 'products'):
                item_col = i
            # Quantity column
            elif qty_col is None and h in ('qty', 'quantity', 'count', 'no', 'nos', 'num'):
                qty_col = i
            # Price column
            elif price_col is None and h in ('price', 'rate', 'unit price', 'unit_price', 'mrp', 'cost', 'unit_cost'):
                price_col = i
            # Amount / Total column
            elif amount_col is None and h in ('amount', 'total', 'total amount', 'total_amount', 'bill', 'value', 'grand total'):
                amount_col = i
            # Phone column
            elif phone_col is None and h in ('phone', 'mobile', 'contact', 'phone number', 'phone_number', 'mob'):
                phone_col = i
            # Date column
            elif date_col is None and h in ('date', 'date of order', 'order date', 'order_date'):
                date_col = i

        # Fallback: try partial/contains matching if exact match failed
        if name_col is None:
            for i, h in enumerate(headers):
                if 'customer' in h or 'name' in h or 'client' in h:
                    name_col = i
                    break

        if item_col is None:
            for i, h in enumerate(headers):
                if i == name_col:
                    continue
                if 'product' in h or 'item' in h or 'order' in h or 'description' in h:
                    item_col = i
                    break

        if price_col is None:
            for i, h in enumerate(headers):
                if 'price' in h or 'rate' in h or 'cost' in h or 'mrp' in h:
                    price_col = i
                    break

        if date_col is None:
            for i, h in enumerate(headers):
                if 'date' in h:
                    date_col = i
                    break

        # Smart fallback: if name_col is still None but we found other columns,
        # use the first unassigned column as the customer name column
        if name_col is None:
            assigned_cols = {item_col, qty_col, price_col, amount_col, phone_col, date_col}
            assigned_cols.discard(None)
            for i in range(len(headers)):
                if i not in assigned_cols:
                    # Check if this column has text data in row 2 (not a number/date)
                    try:
                        row2_val = rows_data[1][i] if len(rows_data) > 1 and i < len(rows_data[1]) else None
                        if row2_val and isinstance(row2_val, str) and not str(row2_val).replace('.','').replace('-','').isdigit():
                            name_col = i
                            break
                    except Exception:
                        pass

            # If still no name_col, just pick the first unassigned column
            if name_col is None:
                for i in range(len(headers)):
                    if i not in assigned_cols:
                        name_col = i
                        break

        if name_col is None:
            flash(f'Could not find a "Name" or "Customer" column. Found headers: {headers}. Please make sure the first row has headers like DATE, Customer, Product, Price.', 'error')
            return redirect(url_for('bulk_receipt'))

        # Read all data rows
        customer_orders = defaultdict(lambda: {'phone': '', 'items': [], 'dates': []})

        for values in rows_data[1:]:
            # Pad row if shorter than headers
            while len(values) < len(headers):
                values.append(None)
            customer_name = str(values[name_col]).strip() if values[name_col] else None
            if not customer_name or customer_name.lower() == 'none':
                continue

            phone = ''
            if phone_col is not None and values[phone_col]:
                phone = str(values[phone_col]).strip()

            date_val = ''
            if date_col is not None and values[date_col]:
                if isinstance(values[date_col], datetime):
                    date_val = values[date_col].strftime('%d %b %y')
                else:
                    date_val = str(values[date_col]).strip()

            item_name = ''
            qty = 1
            price = 0
            amount = 0

            if item_col is not None and values[item_col]:
                item_name = str(values[item_col]).strip()

            if qty_col is not None and values[qty_col]:
                try:
                    qty = int(float(str(values[qty_col])))
                except (ValueError, TypeError):
                    qty = 1

            if price_col is not None and values[price_col]:
                try:
                    price = float(str(values[price_col]))
                except (ValueError, TypeError):
                    price = 0

            if amount_col is not None and values[amount_col]:
                try:
                    amount = float(str(values[amount_col]))
                except (ValueError, TypeError):
                    amount = 0

            # If no item name but has amount, use generic name
            if not item_name and amount > 0:
                item_name = 'Order'
                price = amount
                qty = 1
            elif not item_name and price > 0:
                item_name = 'Order'

            # Calculate total for this line
            if amount > 0 and price == 0:
                price = amount / qty if qty > 0 else amount

            total = qty * price if price > 0 else amount

            if total > 0:
                customer_orders[customer_name]['items'].append({
                    'name': item_name,
                    'qty': qty,
                    'price': price,
                    'total': total,
                    'date': date_val
                })
                if phone:
                    customer_orders[customer_name]['phone'] = phone
                if date_val and date_val not in customer_orders[customer_name]['dates']:
                    customer_orders[customer_name]['dates'].append(date_val)

        # Generate receipts for each unique customer
        total_revenue = 0
        receipt_counter = 1

        for cust_name in sorted(customer_orders.keys()):
            data = customer_orders[cust_name]
            if not data['items']:
                continue

            subtotal = sum(item['total'] for item in data['items'])
            total_revenue += subtotal

            receipt_num = f"BB-{datetime.now().strftime('%Y%m%d')}-{receipt_counter:04d}"
            dates_list = data.get('dates', [])
            if dates_list:
                if len(dates_list) == 1:
                    receipt_date = dates_list[0]
                else:
                    receipt_date = f"{dates_list[0]} — {dates_list[-1]}"
            else:
                receipt_date = datetime.now().strftime('%B %d, %Y')
            receipts.append({
                'receipt_num': receipt_num,
                'date': receipt_date,
                'time': datetime.now().strftime('%I:%M %p'),
                'customer_name': cust_name,
                'customer_phone': data['phone'],
                'payment_method': 'Cash',
                'line_items': data['items'],
                'subtotal': subtotal,
                'total': subtotal,
            })
            receipt_counter += 1

        summary = {
            'total_customers': len(receipts),
            'total_orders': sum(len(r['line_items']) for r in receipts),
            'total_revenue': total_revenue,
        }

        if not receipts:
            flash('No valid data found in the Excel file. Make sure it has Name and Amount/Price columns.', 'error')
            return redirect(url_for('bulk_receipt'))

    except Exception as e:
        flash(f'Error processing Excel file: {str(e)}', 'error')
        return redirect(url_for('bulk_receipt'))

    # Store results and redirect (PRG pattern)
    rid = str(uuid.uuid4())
    BULK_RESULTS[rid] = {'receipts': receipts, 'summary': summary}

    # Cleanup old results (keep max 10)
    if len(BULK_RESULTS) > 10:
        oldest = list(BULK_RESULTS.keys())[0]
        BULK_RESULTS.pop(oldest, None)

    return redirect(url_for('bulk_receipt', rid=rid))


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
