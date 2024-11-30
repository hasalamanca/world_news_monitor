# create_sample_data.py

import pandas as pd

# Create a sample DataFrame with English entries
data = {
    'title': [
        'Breaking News: Market hits all-time high',
        'Sports Update: Local team wins championship',
        'Weather Alert: Heavy rain expected tomorrow',
        'Economy slows down in the last quarter',
        'New Study Reveals Health Benefits of Coffee',
        'Festival Brings Joy to the City',
        'Election Results: New Leader Elected',
        'Tech Giant Releases Innovative Product',
        'Healthcare Advances Lead to Longer Lives',
        'Education Reform Proposed by Government'
    ],
    'description': [
        'Investors are thrilled as stocks reach new heights.',
        'Celebrations erupt as the local team secures the title.',
        'Citizens advised to prepare for potential flooding.',
        'Experts predict further decline in the coming months.',
        'Researchers find that coffee consumption may improve longevity.',
        'People gather to celebrate cultural diversity and unity.',
        'The nation reacts to the election of a new leader.',
        'Consumers excited about the latest groundbreaking technology.',
        'Medical breakthroughs contribute to increased life expectancy.',
        'Proposed changes aim to improve educational outcomes.'
    ]
}

# Create the DataFrame
df_sample = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df_sample.to_csv('sample_data.csv', index=False)

print("Sample DataFrame created and saved as 'sample_data.csv'.")
