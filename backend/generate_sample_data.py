"""
Script to generate sample real estate data for testing
Run this to create a sample Excel file if you don't have the original dataset
"""
import pandas as pd
import random
from datetime import datetime

# Pune localities
localities = [
    'Wakad', 'Aundh', 'Kharadi', 'Hinjewadi', 'Baner', 
    'Viman Nagar', 'Koregaon Park', 'Kalyani Nagar', 'Magarpatta',
    'Ambegaon Budruk', 'Akurdi', 'Pimple Saudagar', 'Hadapsar',
    'Kothrud', 'Deccan Gymkhana', 'Shivaji Nagar', 'Pimpri',
    'Chinchwad', 'Undri', 'Wagholi'
]

# Generate data
data = []
for year in range(2018, 2025):
    for locality in localities:
        # Base price with year-over-year growth
        base_price = random.randint(3000, 8000)
        price_per_sqft = base_price + (year - 2018) * random.randint(200, 500)
        
        # Generate multiple records per year
        for _ in range(random.randint(3, 8)):
            size = random.choice([600, 800, 1000, 1200, 1500, 1800, 2000, 2500])
            price = price_per_sqft * size
            
            # Add some variance
            price = price * random.uniform(0.9, 1.1)
            
            record = {
                'Year': year,
                'Area': locality,
                'Price': round(price, 2),
                'Demand': random.randint(5, 50),
                'Size': size,
                'Type': random.choice(['2BHK', '3BHK', '4BHK', '1BHK']),
                'Month': random.randint(1, 12)
            }
            data.append(record)

# Create DataFrame
df = pd.DataFrame(data)

# Sort by Year and Area
df = df.sort_values(['Year', 'Area']).reset_index(drop=True)

# Save to Excel
output_file = 'real_estate_data.xlsx'
df.to_excel(output_file, index=False)

print(f"✅ Sample data generated successfully!")
print(f"📁 File: {output_file}")
print(f"📊 Records: {len(df)}")
print(f"📍 Localities: {len(localities)}")
print(f"📅 Years: 2018-2024")
print(f"\nSample data:")
print(df.head(10))
print(f"\nStatistics:")
print(df.describe())
