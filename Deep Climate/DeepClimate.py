import re
from collections import Counter

def DeepClimate():
    results = []

    with open("USW00013959.csv", "r") as file:
        for line in file:
            if re.search(r"^\d{4}", line):
                results.append([line.replace("\n", "").split(",")[0], line.replace("\n", "").split(",")[2], line.replace("\n", "").split(",")[3], line.replace("\n", "").split(",")[4]])

    max_temp_change = []
    old_climate = results[0][1]
    for result in results[1:]:
        try:
            max_temp_change.append(abs(int(result[1]) - int(old_climate)))
            old_climate = result[1]

        except:
            pass

    data = Counter(max_temp_change).most_common(len(max_temp_change))
    print(data)

if __name__ == "__main__":
    deep_climate()
