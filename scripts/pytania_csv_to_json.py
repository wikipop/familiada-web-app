import json
import random
import pandas as pd

df = pd.read_csv("../data/familiada_pytania.csv")

def generate_variable_points():
    """
    Generuje listę 8 punktów, których suma wynosi od 95 do 100,
    a wartości maleją w różnym tempie.
    """
    total_points = random.randint(95, 100)

    # Tworzymy malejące proporcje, np. [0.3, 0.2, ..., 0.01] i normalizujemy
    weights = sorted([random.uniform(0.5, 5.0) for _ in range(8)], reverse=True)
    weight_sum = sum(weights)
    normalized = [w / weight_sum for w in weights]

    # Przekształcamy w punkty i zaokrąglamy do całkowitych
    raw_points = [round(p * total_points) for p in normalized]

    # Korekta sumy, aby uzyskać dokładnie total_points
    diff = total_points - sum(raw_points)
    for i in range(abs(diff)):
        index = i % 8
        raw_points[index] += 1 if diff > 0 else -1

    return raw_points


def convert_to_structured_json_variable_points(df):
    structured_data = []

    for _, row in df.iterrows():
        question = row['Pytanie']
        points_list = generate_variable_points()

        answers = []
        for i in range(1, 9):
            answer_text = row[str(i)]
            answers.append({
                "odpowiedź": answer_text,
                "punkty": points_list[i - 1]
            })

        structured_data.append({
            "pytanie": question,
            "odpowiedzi": answers
        })

    return structured_data


# Nowa konwersja z bardziej realistycznym przydziałem punktów
converted_variable_json = convert_to_structured_json_variable_points(df)

# Zapisz do pliku
output_path_variable = "../data/familiada_pytania.json"
with open(output_path_variable, "w", encoding="utf-8") as f:
    json.dump(converted_variable_json, f, ensure_ascii=False, indent=4)