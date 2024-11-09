class DiscountModule:
    def __init__(self, item_names, item_prices, campaigns):
        self.item_names = item_names
        self.item_prices = item_prices
        self.campaigns = campaigns

    def apply_discounts(self):
        total = sum(self.item_prices)
        total = self.coupon(total)
        total = self.on_top(total)
        total = self.seasonal(total)

        if total <=0 :
            return 0

        return total
    
    def coupon(self, price):
        if price <=0 :
            return 0
        coupon_campaigns = [campaign for campaign in self.campaigns if campaign['type'] in ['fixed_amount', 'percentage']]
    
        if len(coupon_campaigns) > 1:
            raise ValueError("Only one coupon discount can be applied. Multiple coupon discounts found.")
    
        if coupon_campaigns:
            campaign = coupon_campaigns[0]
            if campaign['type'] == 'fixed_amount':
                price -= campaign['amount']
            elif campaign['type'] == 'percentage':
                price *= (1 - campaign['percentage'] / 100)
    
        return price
    
    def on_top(self, price):
        if price <=0 :
            return 0
        on_top_campaigns = [campaign for campaign in self.campaigns if campaign['type'] in ['percentage_by_category', 'points']]
    
        if len(on_top_campaigns) > 1:
            raise ValueError("Only one On Top discount can be applied. Multiple On Top discounts found.")
    
        if on_top_campaigns:
            campaign = on_top_campaigns[0]
            if campaign['type'] == 'percentage_by_category':
                category_total = sum(
                    price for name, price in zip(self.item_names, self.item_prices) if name[1] in campaign.get('category', [])
                )
                price -= category_total * (campaign['percentage'] / 100)
            elif campaign['type'] == 'points':
                max_discount = 0.2 * price
                discount = min(campaign['points'], max_discount)
                price -= discount
        return price
    
    def seasonal(self, price):
        if price <=0 :
            return 0
        seasonal_campaigns = [campaign for campaign in self.campaigns if campaign['type'] == 'seasonal']
    
        if seasonal_campaigns:
            campaign = seasonal_campaigns[0]
            x = campaign['x']
            y = campaign['y']
            discount_count = price // x
            price -= discount_count * y
    
        return price