from faker import Faker

fake = Faker()

def generate_checkout_details():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "postal_code": fake.postcode()
    }