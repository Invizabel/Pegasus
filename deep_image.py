import argparse
import numpy as np
import os
import random
import re
from collections import Counter
from numba import njit
from PIL import Image

CYAN = "\033[1;36m"

@njit
def numba_train(r, g, b, a, tolerance):
    count = -1
    for red in range(0, 255):
        for green in range(0, 255):
            for blue in range(0, 255):
                for alpha in range(0, 255):
                    count += 1
                    if red - tolerance <= r <= red + tolerance and green - tolerance <= g <= green + tolerance and blue - tolerance <= b <= blue + tolerance and alpha - tolerance <= a <= alpha + tolerance:
                        return count

def generate(my_model):
    with open(f"{my_model}.csv", "r") as file:
        data = file.read()

    data = data.replace(";", ",")

    results = re.findall("(\d+),(\d+),(.+),(\d+)", data)

    data_sets = []
    new_data_set = []
    new_result = results[0]
    for result in results:
        if result[0] == new_result[0] and result[1] == new_result[1]:
            new_data_set.append(result)

        else:
            data_sets.append(new_data_set[:])
            new_data_set = []

        new_result = result

    image = Image.new("RGBA", (64, 64))

    if "low" in my_model:
        noise = random.randint(0, 10 - 2)

    if "medium" in my_model:
        noise = random.randint(0, 100 - 2)

    if "large" in my_model:
        noise = random.randint(0, 1000 - 2)

    if "xl" in my_model:
        noise = random.randint(0, 10000 - 2)

    for data_set in data_sets:
        image.putpixel((int(data_set[0][0]), int(data_set[0][1])), (int(data_set[noise][2].split(",")[0].replace("(", "")), int(data_set[noise][2].split(",")[1]), int(data_set[noise][2].split(",")[2]), int(data_set[noise][2].split(",")[3].replace(")", ""))))

    image = image.resize((1920, 1080))
    image.save(f"{my_model.replace('.csv', '')}.png")

def train(samples, my_model, tolerance):
    pixels = []
    models = []
    folders = [my_model]
    
    for folder in folders:
        files = os.listdir(folder)

        images = []
        
        for file in files:
            print(CYAN + f"{folder}/{file}")
            image = Image.open(f"{folder}/{file}").convert("RGBA")
            image = image.resize((64, 64))
            images.append(image)

        for sample in samples:
            with open(f"model_{sample[0]}_t{tolerance}.csv", "w") as file:
                file.write("x,y,pixel,vector\n")

            for x in range(0, 64):
                for y in range(0, 64):
                    print(CYAN + f"{sample[0]}/t{tolerance}: ({x}, {y})")
                    models = []
                    pixels = []
                    for image in images:
                        # process pixels: (x, y)
                        r, g, b, a = image.getpixel((x, y))
                        pixels.append(numba_train(r, g, b, a, tolerance))

                    tokens = Counter(pixels).most_common(sample[1])
                    for token in tokens:
                        models.append([str(x), str(y), str(token[0]), str(token[1])])

                    with open(f"model_{sample[0]}_t{tolerance}.csv", "a") as file:
                        for model in models:
                            file.write(f"{model[0]},{model[1]},{model[2].replace(',', ';')},{model[3]}\n")

def main():
    os.system("clear")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-mode", required = True, type = str, choices = ["generate", "train", "verify"])
    parser.add_argument("-model", required = True, type = str)
    parser.add_argument("-tolerance", required = False, type = int)
    args = parser.parse_args()

    if args.mode == "generate":
        generate(args.model)

    if args.mode == "train":
        '''samples = [["low", 10],
                   ["medium", 100],
                   ["large", 1000],
                   ["xl", 10000]]'''

        samples = [["large", 1000]]

        tolerances = [8, 16, 32, 64]

        for tolerance in tolerances:
            train(samples, args.model, tolerance)

if __name__ == "__main__":
    main()
