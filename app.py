from flask import Flask, render_template, request
from discount_module import DiscountModule

app = Flask(__name__)

MOCK_ITEMS = [
    {"name": "T-Shirt", "price": 350.0, "category": "Clothing"},
    {"name": "Hat", "price": 250.0, "category": "Accessories"},
    {"name": "Hoodie", "price": 700.0, "category": "Clothing"},
    {"name": "Watch", "price": 850.0, "category": "Accessories"},
    {"name": "Sneakers", "price": 1200.0, "category": "Footwear"},
    {"name": "Jeans", "price": 500.0, "category": "Clothing"},
    {"name": "Sunglasses", "price": 600.0, "category": "Accessories"},
    {"name": "Backpack", "price": 950.0, "category": "Accessories"},
    {"name": "Headphones", "price": 1300.0, "category": "Electronics"},
    {"name": "Smartphone Case", "price": 150.0, "category": "Electronics"}
]

@app.route('/', methods=['GET', 'POST'])
def index():
    final_price = None  
    
    if request.method == 'POST':
        selected_item_names = request.form.getlist('selected_items')
        
        selected_items = [item for item in MOCK_ITEMS if item['name'] in selected_item_names]
        
        item_names = []
        item_prices = []
        for item in selected_items:
            item_name = item['name']
            item_price = item['price']
            item_category= item['category']
            quantity = int(request.form.get(f'quantity_{item_name}', 1))
            total_price_for_item = item_price * quantity
            
            item_names.append([item_name,item_category])
            item_prices.append(total_price_for_item)
        campaigns = []
        error = None  

        if request.form.get('fixed_amount'):
            fixed_amount = float(request.form['fixed_amount'])
            if fixed_amount < 0:
                error = "Fixed amount discount cannot be negative."
            elif fixed_amount > 0:
                campaigns.append({
                    'type': 'fixed_amount',
                    'amount': fixed_amount
                })

        if request.form.get('percentage'):
            percentage = float(request.form['percentage'])
            if percentage < 0:
                error = "Percentage discount cannot be negative."
            elif percentage > 100:
                error = "Percentage discount cannot be more than 100."
            elif percentage > 0:
                campaigns.append({
                    'type': 'percentage',
                    'percentage': percentage
                })

        if request.form.get('category') and request.form.get('category_percentage'):
            category_percentage = float(request.form['category_percentage'])
            if category_percentage < 0:
                error = "Category percentage discount cannot be negative."
            elif category_percentage > 0:
                campaigns.append({
                    'type': 'percentage_by_category',
                    'category': request.form['category'].split(','),
                    'percentage': category_percentage
                })

        if request.form.get('points'):
            points = int(request.form['points'])
            if points < 0:
                error = "Points discount cannot be negative."
            elif points > 0:
                campaigns.append({
                    'type': 'points',
                    'points': points
                })

        if request.form.get('seasonal_every_x') and request.form.get('seasonal_discount_y'):
            every_x_thb = float(request.form['seasonal_every_x'])
            discount_y_thb = float(request.form['seasonal_discount_y'])
            if every_x_thb < 0 or discount_y_thb < 0:
                error = "Seasonal discount values cannot be negative."
            elif every_x_thb<= discount_y_thb:
                error =  "Discount cannot be more than or equal to seasonal discount."
            elif every_x_thb > 0 and discount_y_thb > 0:
                campaigns.append({
                    'type': 'seasonal',
                    'every_x_thb': every_x_thb,
                    'discount_y_thb': discount_y_thb
                })

        if error:
            return render_template('index.html', error=error, final_price=None, items=MOCK_ITEMS)

        discount_module = DiscountModule(item_names, item_prices, campaigns)
        try:
            final_price = discount_module.apply_discounts()
        except ValueError as e:
            return render_template('index.html', error=str(e), final_price=None, items=MOCK_ITEMS)
        
    return render_template('index.html', final_price=final_price, items=MOCK_ITEMS)

if __name__ == '__main__':
    app.run(debug=True)