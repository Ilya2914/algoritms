import random
import pandas as pd
from datetime import datetime, timedelta, time

WORKSTART = 9
WORKEND = 18
WORKDAYS = set(range(0,5))

banks = ["Сбербанк","Т-Банк","ВТБ","Альфа-Банк"]
schemes = ["Visa","MasterCard","МИР"]

print("Введите вероятности банков (Сбербанк, Т-Банк, ВТБ, Альфа-Банк) через пробел, сумма = 1:")
bank_probs = list(map(float, input().split()))
if len(bank_probs) != 4 or sum(bank_probs) > 1 or sum(bank_probs) == 0:
    raise ValueError("Сумма вероятностей банков должна быть <= 1 и > 0 и должно быть 4 числа!")

print("Введите вероятности платежных систем (Visa, MasterCard, МИР) через пробел, сумма = 1:")
scheme_probs = list(map(float, input().split()))
if len(scheme_probs) != 3 or sum(scheme_probs) > 1 or sum(scheme_probs) == 0:
    raise ValueError("Сумма вероятностей платежных систем должна быть <= 1 и > 0 и должно быть 3 числа!")

surnames_man = ["Иванов","Петров","Сидоров","Смирнов","Кузнецов","Попов","Соколов",
                 "Лебедев","Козлов","Новиков","Морозов","Волков","Медведев","Федоров",
                 "Соловьев","Васильев","Михайлов","Григорьев","Егоров","Андреев",
                 "Белов","Кириллов","Никитин","Савельев","Кондратьев","Тарасов",
                 "Богданов","Данилов","Елисеев","Зайцев","Игнатьев","Капустин"]
surnames_women = [s + "а" for s in surnames_man]

first_names_man = ["Иван","Пётр","Сергей","Алексей","Дмитрий","Михаил","Андрей","Николай",
                    "Владимир","Юрий","Олег","Роман","Кирилл","Максим","Василий","Станислав"]
first_names_women = ["Юлия","Анна","Екатерина","Мария","Ольга","Наталья","Ирина","Елена",
                      "Татьяна","Светлана","Александра","Виктория","Дарья","Ксения","Алиса"]

patronymics_man = ["Иванович","Петрович","Сергеевич","Алексеевич","Дмитриевич","Михайлович",
                    "Андреевич","Николаевич","Владимирович","Юрьевич","Олегович","Романович"]
patronymics_women = [p[:-2]+"евна" if p.endswith("ич") else p+"на" for p in patronymics_man]

base_symptom_to_doctors = {
    "боль в горле": ["лор","терапевт"],
    "насморк": ["лор","терапевт"],
    "кашель": ["лор","пульмонолог","терапевт"],
    "повышенная температура": ["терапевт","инфекционист"],
    "головная боль": ["невролог","терапевт"],
    "боль в животе": ["гастроэнтеролог","терапевт"],
    "тошнота": ["гастроэнтеролог","терапевт"],
    "понос": ["гастроэнтеролог","терапевт"],
    "сыпь": ["дерматолог"],
    "зуд кожи": ["дерматолог","аллерголог"],
    "аллергическая реакция": ["аллерголог","дерматолог"],
    "затруднённое дыхание": ["пульмонолог","терапевт","кардиолог"],
    "одышка": ["пульмонолог","кардиолог"],
    "боль в груди": ["кардиолог","терапевт"],
    "аритмия": ["кардиолог"],
    "снижение зрения": ["офтальмолог"],
    "шум в ушах": ["оториноларинголог","невролог"],
    "потеря сознания": ["невролог","реаниматолог"],
    "травма": ["хирург","травматолог"],
    "боль в спине": ["невролог","травматолог","ортопед"],
    "депрессия": ["психиатр","психолог"],
    "бессонница": ["невролог","психиатр"],
    "злоупотребление алкоголем": ["нарколог"],
    "нарушение памяти": ["невролог","психиатр"],
    "нарушение координации": ["невролог"],
    "проблемы с мочеиспусканием": ["уролог","нефролог"],
    "нарушение менструального цикла": ["гинеколог"],
    "беременность": ["гинеколог"]
}

test_prices = {
    "мазок на ковид": 500,
    "общий анализ крови": 400,
    "биохимия крови": 1200,
    "анализ мочи общий": 300,
    "ПЦР (инфекция)": 800,
    "антигенный тест": 600,
    "микроскопия": 450,
    "посев": 700,
    "гормональный профиль": 1500,
    "антибиотикограмма": 900,
    "онкомаркеры": 2000,
    "УЗИ": 1200,
    "рентген": 1500,
    "МРТ": 5000,
    "КТ": 4000,
    "ЭКГ": 700,
    "спирометрия": 600,
    "анализ кала": 350,
    "иммунологический тест": 1800,
    "анализ на сахар": 450,
    "анализ на холестерин": 500,
    "тест на аллергию": 700,
    "тест на витамины": 600,
    "тест на гормоны": 800,
    "анализ на витамины": 600,
    "не требуются": 0
}

symptom_to_tests = {
    "боль в горле": ["мазок на ковид","антигенный тест"],
    "насморк": ["мазок на ковид","антигенный тест"],
    "кашель": ["спирометрия","мазок на ковид"],
    "повышенная температура": ["общий анализ крови","биохимия крови"],
    "головная боль": ["биохимия крови","анализ на сахар","анализ на холестерин"],
    "боль в животе": ["анализ мочи общий","биохимия крови"],
    "тошнота": ["анализ на витамины","биохимия крови"],
    "понос": ["анализ кала","анализ мочи общий"],
    "сыпь": ["тест на аллергию"],
    "зуд кожи": ["тест на аллергию"],
    "аллергическая реакция": ["тест на аллергию"],
    "затруднённое дыхание": ["спирометрия","ЭКГ"],
    "одышка": ["спирометрия","ЭКГ"],
    "боль в груди": ["ЭКГ","спирометрия"],
    "аритмия": ["ЭКГ"],
    "снижение зрения": [],
    "шум в ушах": [],
    "потеря сознания": ["ЭКГ","анализ на сахар"],
    "травма": ["рентген","КТ","МРТ"],
    "боль в спине": ["МРТ","рентген"],
    "депрессия": [],
    "бессонница": [],
    "злоупотребление алкоголем": ["анализ на витамины"],
    "нарушение памяти": ["анализ на витамины"],
    "нарушение координации": ["анализ на витамины"],
    "проблемы с мочеиспусканием": ["анализ мочи общий"],
    "нарушение менструального цикла": ["гормональный профиль"],
    "беременность": ["гормональный профиль"]
}

bank_card_bins = {
    "Сбербанк": {
        "Visa": ["427402", "427411"],
        "MasterCard": ["510510", "555555"],
        "МИР": ["220000", "220001"]
    },
    "Т-Банк": {
        "Visa": ["427500", "427510"],
        "MasterCard": ["510520", "555560"],
        "МИР": ["220010", "220011"]
    },
    "ВТБ": {
        "Visa": ["427520", "427530"],
        "MasterCard": ["510530", "555570"],
        "МИР": ["220020", "220021"]
    },
    "Альфа-Банк": {
        "Visa": ["427714", "427715"],
        "MasterCard": ["510540", "555580"],
        "МИР": ["220030", "220031"]
    }
}


def gen_russian_passport(existing_set):
    while True:
        series = random.randint(1000,9999)
        number = random.randint(100000,999999)
        p = f"RU {series:04d} {number:06d}"
        if p not in existing_set:
            existing_set.add(p)
            return p

def gen_kazakh_passport(existing_set):
    while True:
        series = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        number = random.randint(10000000, 99999999)
        p = f"KZ {series} {number:08d}"
        if p not in existing_set:
            existing_set.add(p)
            return p

def gen_belarus_passport(existing_set):
    while True:
        series = "".join(random.choices("ABCEHKMOPT", k=2))
        number = random.randint(1000000,9999999)
        p = f"BY {series} {number:07d}"
        if p not in existing_set:
            existing_set.add(p)
            return p

def gen_snils(existing_set):
    while True:
        snils = f"{random.randint(100,999):03d}-{random.randint(100,999):03d}-{random.randint(100,999):03d} {random.randint(10,99):02d}"
        if snils not in existing_set:
            existing_set.add(snils)
            return snils

def random_work_datetime(start_date,end_date):
    days=(end_date-start_date).days
    for _ in range(1000):
        d = start_date + timedelta(days=random.randint(0, days))
        hour = random.randint(WORKSTART, WORKEND-1)
        minute = random.choice([0,15,30,45])
        dt = datetime.combine(d.date(), time(hour, minute))
        if dt.weekday() in WORKDAYS:
            return dt
    return datetime.combine(start_date,time(WORKSTART,0))

used_cards_global = set()

def choose_card(bank_probs, scheme_probs, bank_card_bins):
    while True:
        bank = random.choices(banks, weights=bank_probs)[0]
        scheme = random.choices(schemes, weights=scheme_probs)[0]
        bin_prefix = random.choice(bank_card_bins[bank][scheme])
        remaining_length = 16 - len(bin_prefix)
        number = bin_prefix + "".join(str(random.randint(0,9)) for _ in range(remaining_length-1))
        number += str(random.randint(0,9))
        if number not in used_cards_global:
            used_cards_global.add(number)
            return bank, scheme, number

def generate_dataset(rows=50000,out_xlsx="dataset.xlsx"):

    used_passports=set()
    used_snils=set()
    passport_generators = [gen_russian_passport, gen_kazakh_passport, gen_belarus_passport]

    clients_dict = {}
    clients=[]
    for _ in range(rows//2):
        sex = random.choice(["мужской","женский"])
        if sex=="мужской":
            fio = f"{random.choice(surnames_man)} {random.choice(first_names_man)} {random.choice(patronymics_man)}"
        else:
            fio = f"{random.choice(surnames_women)} {random.choice(first_names_women)} {random.choice(patronymics_women)}"
        if fio in clients_dict:
            passport = clients_dict[fio]["passport"]
            snils = clients_dict[fio]["snils"]
        else:
            passport = random.choice(passport_generators)(used_passports)
            snils = gen_snils(used_snils)
            clients_dict[fio] = {"passport": passport, "snils": snils}
        clients.append({"fio":fio,"sex":sex,"passport":passport,"snils":snils})

    cards=[]
    data=[]
    symptom_list=list(base_symptom_to_doctors.keys())

    for _ in range(rows):
        client=random.choice(clients)
        sex = client["sex"]
        if sex=="мужской":
            possible_symptoms = [s for s in symptom_list if s not in ["беременность","нарушение менструального цикла"]]
        else:
            possible_symptoms = symptom_list
        symptoms=random.sample(possible_symptoms,k=random.randint(1,5))

        doctor_candidates=[]
        for s in symptoms:
            doctor_candidates.extend(base_symptom_to_doctors[s])
        doctor=random.choice(doctor_candidates)

        visit_date=random_work_datetime(datetime(2020,1,1),datetime(2025,1,1))

        def random_analysis_datetime(visit_date):
            for _ in range(1000):
                delta_hours = random.randint(24, 72)
                dt = visit_date + timedelta(hours=delta_hours)
                dt = dt.replace(hour=random.randint(WORKSTART, WORKEND - 1),
                                minute=random.choice([0, 15, 30, 45]))
                if dt.weekday() in WORKDAYS:
                    return dt
            dt = visit_date + timedelta(hours=24)
            dt = dt.replace(hour=WORKSTART, minute=0)
            return dt

        analysis_date = random_analysis_datetime(visit_date)

        # Анализы
        tests_candidates=[]
        test_choice=[]
        for s in symptoms:
            tests_candidates.extend(symptom_to_tests.get(s,[]))
        tests_selected=random.sample(tests_candidates,k=min(len(tests_candidates), random.randint(1,5)))
        for i in range (len(tests_selected)):
            if tests_selected[i] not in test_choice:
                test_choice.append(tests_selected[i])
        if len(test_choice) == 0:
            test_choice.append("не требуются")
        price=sum([test_prices[t] for t in test_choice])

        available_cards = [c for c in cards if
                           (c["assigned_to"] is None or c["assigned_to"] == client["passport"]) and c["uses_left"] > 0]
        if not available_cards:
            bank, scheme, number = choose_card(bank_probs, scheme_probs, bank_card_bins)
            card = {"bank": bank, "scheme": scheme, "number": number, "uses_left": 5, "assigned_to": client["passport"]}
            cards.append(card)
        else:
            weights = []
            for c in available_cards:
                bank_index = banks.index(c["bank"])
                scheme_index = schemes.index(c["scheme"])
                weights.append(bank_probs[bank_index] * scheme_probs[scheme_index])
            card = random.choices(available_cards, weights=weights)[0]

        card["uses_left"] -= 1
        card["assigned_to"] = client["passport"]

        data.append({
            "ФИО":client["fio"],
            "Пол": sex,
            "Паспорт":client["passport"],
            "СНИЛС":client["snils"],
            "Симптомы":", ".join(symptoms),
            "Врач":doctor,
            "Дата посещения":visit_date.isoformat(),
            "Анализы":", ".join(test_choice),
            "Дата получения анализов": analysis_date.isoformat(),
            "Стоимость анализов":f"{price} руб.",
            "Банк":card["bank"],
            "Номер карты":card["number"]
        })

    df=pd.DataFrame(data)
    df.to_excel(out_xlsx,index=False)
    print(f"Датасет сгенерирован: {out_xlsx}, строк: {len(df)}")
    return df

if __name__=="__main__":
    generate_dataset(rows=50000,out_xlsx="dataset.xlsx")
