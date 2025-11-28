import pandas as pd
import random
def generate_data(n=100):
    age_range = (30, 86)
    blood_types = ['B-', 'A+', 'A-', 'O+', 'AB+']
    medical_conditions = ['Cancer', 'Obesity', 'Diabetes', 'Arthritis', 'Hypertension']
    data = []
    
    for i in range(1, n + 1):
        age = random.randint(age_range[0], age_range[1])
        medical_condition = random.choice(medical_conditions)
        if medical_condition == 'Cancer':
            admission_type = 'Emergency'
        elif age >= 65:
            admission_type = 'Emergency'
        elif medical_condition in ['Hypertension', 'Diabetes'] and age >= 40:
            admission_type = 'Urgent'
        else:
            admission_type = 'Elective'
       
        if medical_condition == 'Cancer':
            medication = random.choice(['Lipitor', 'Aspirin'])
        elif medical_condition == 'Obesity':
            medication = random.choice(['Paracetamol', 'Ibuprofen'])
        elif medical_condition == 'Diabetes':
            medication = random.choice(['Penicillin', 'Ibuprofen'])
        elif medical_condition == 'Hypertension':
            medication = random.choice(['Aspirin', 'Lipitor'])
        elif medical_condition == 'Arthritis':
            medication = random.choice(['Ibuprofen', 'Paracetamol'])
        
        if age <= 40 and medical_condition not in ['Cancer', 'Diabetes']:
            test_result = 'Normal'
        elif age >= 60 or medical_condition in ['Cancer', 'Diabetes']:
            test_result = 'Abnormal'
        else:
            test_result = 'Inconclusive'
        user_data = {
            'Name': f'User{i}',
            'Age': age,
            'Blood Type': random.choice(blood_types),
            'Medical Condition': medical_condition,
            'Admission Type': admission_type,
            'Medication': medication,
            'Test Results': test_result,
        }
        data.append(user_data)
    
    df = pd.DataFrame(data)
    df.to_csv('user_health_data.csv', index=False)
    return df

df = generate_data(100)

