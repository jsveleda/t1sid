import random
import string

class DataGenerator:

    def __init__(self):
        self.data = []
    
    def generate_data(self, length):
        for i in range(length):
            key = f'key_{i}'
            value = f'value_{self.generate_string()}'
            self.data.append((key, value))

    def generate_string(self):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(16))