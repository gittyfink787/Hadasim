import random
import pandas as pd

random.seed(42)
num_people=400
people=[]

def generate_name(gender):
    male_names = [
        "David", "Michael", "Joshua", "Aaron", "Isaac", "Eli", "Solomon", "Samuel", "Daniel", "Benjamin",
        "Moses", "Jacob", "Ezra", "Levi", "Asher", "Reuben", "Gad", "Simeon", "Judah", "Naphtali",
        "Zachariah", "Ezekiel", "Elijah", "Caleb", "Nathan", "Saul", "Isaiah", "Jeremiah", "Amos", "Hosea",
        "Eliezer", "Abraham", "Jonah", "Jesse", "Baruch", "Shlomo", "Hanan", "Yonatan", "Lior", "Oren",
        "Ariel", "Uri", "Tuvia", "Shimon", "Yaakov", "Reuven", "Matan", "Nadav", "Noam", "Yitzhak"
    ]

    female_names = [
        "Sarah", "Rebecca", "Leah", "Rachel", "Miriam", "Esther", "Hannah", "Ruth", "Tamar", "Deborah",
        "Naomi", "Shulamit", "Dina", "Yocheved", "Malkah", "Zippora", "Batya", "Hadas", "Yaara", "Tova",
        "Avigail", "Chana", "Liya", "Esther", "Raizel", "Tehila", "Malka", "Rivka", "Michal", "Sivan",
        "Shira", "Bat-Chen", "Ahuva", "Yona", "Gila", "Hila", "Nava", "Tali", "Chavi", "Meira", "Ayelet",
        "Bracha", "Shoshana", "Noa", "Yaara", "Rinat", "Dvorah", "Ariel", "Yaara", "Chagit", "Liat"
    ]

    family_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
        "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Young",
        "King", "Scott", "Green", "Baker", "Adams", "Nelson", "Hall", "Rivera", "Campbell", "Mitchell",
        "Roberts", "Carter", "Phillips", "Evans", "Turner", "Torres", "Parker", "Collins", "Edwards", "Stewart"
    ]

    return (random.choice(male_names if gender=='Male' else female_names),random.choice(family_names))

def generate_people():
    for person_id in range(1,num_people+1):
        gender=random.choice(['Male','Female'])
        personal_name,family_name,=generate_name(gender)
        people.append({
            'person_id':person_id,
            'personal_name':personal_name,
            'family_name':family_name,
            'gender':gender,
            'father_id':None,
            'mother_id':None,
            'spouse_id':None
        })


def generate_couples():
    males=[p for p in people if p['gender']=='Male']
    females=[p for p in people if p['gender']=='Female']
    min_len=min(len(males),len(females))

    couples=[]
    for i in range(min_len):
        husband=males[i]
        wife=females[i]
        prob_1=random.random()
        prob_2 = random.random()
        if prob_1< 0.8:
            husband['spouse_id']=wife['person_id']
        if prob_2 < 0.8:
            wife['spouse_id']=husband['person_id']
        if prob_1 or prob_2:
            couples.append((husband['person_id'],wife['person_id']))

    return couples

def generate_children(couples):
    if not couples:
        return
    for p in people:
        i=len(couples)-random.randint(1,5)

        while i>0:
            fath_can, moth_can = couples[i]
            if fath_can<p['person_id'] and moth_can<p['person_id']:
                p['father_id']=fath_can
                p['mother_id']=moth_can
                break
            else:
                i=i//2


def generate_SQL():
    with open("inset_to_person.txt",'w',encoding="utf-8") as file:
        for p in people:
            sql_query=f"""
            INSERT INTO person (person_id,personal_name,family_name,gender,father_id,mother_id,spouse_id)
            VALUES ({p['person_id']},'{p['personal_name']}','{p['family_name']}','{p['gender']}',
            {'NULL' if p['father_id'] is None else p['father_id']} ,
            {'NULL' if p['mother_id'] is None else p['mother_id']},
            {'NULL' if p['spouse_id'] is None else p['spouse_id']});
            """
            file.write(sql_query)

generate_people()
couples=generate_couples()
generate_children(couples)
generate_SQL()











