from datetime import datetime

def generate_complex_password():
        # Implement your password generation logic here
        import random
        import string

        length = random.randint(7, 10)
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))


def apply_coupon_discount(coupon, order_total):
        if coupon.expire_at and coupon.expire_at < datetime.now():
            return 0
              
        if coupon.coupon_types == 'Flat Discount':
            discount_amount = coupon.value
        elif coupon.coupon_types == 'Percentage Discount':
            discount_percent = coupon.value
            discount_amount = (int(order_total) * int(discount_percent)) / 100
            print(discount_amount)
        else:
            discount_amount = 0
        
        return discount_amount
