import argparse
import math
import os
import random
import shutil
from collections import Counter
from numba import njit
from PIL import Image

CYAN = "\033[1;36m"

def calculate_distance(gather):
    distance_array = []
    for i in range(62):
        for j in range(0, 63):
            x1 = gather[i][j]
            y1 = gather[i][j + 1]
            x2 = gather[i + 1][j]
            y2 = gather[i + 1][j + 1]
            distance = ((x2- x1) ** 2 + (y2 - y1) ** 2) ** (1 / 2)
            distance_array.append(math.floor(distance))

    return distance_array

@njit
def numba_transform(r, g, b, a, tolerance):
    count = -1
    for red in range(256):
        for green in range(256):
            for blue in range(256):
                for alpha in range(256):
                    count += 1
                    if red - tolerance <= r <= red + tolerance and green - tolerance <= g <= green + tolerance and blue - tolerance <= b <= blue + tolerance and alpha - tolerance <= a <= alpha + tolerance:
                        return count

def train(samples, my_model, tolerance):
    folders = [my_model]
    shutil.rmtree("trained_models")
    os.mkdir("trained_models")
    
    for folder in folders:
        files = os.listdir(folder)

        images = []

        print(CYAN + "loading images")
        for file in files:
            image = Image.open(f"{folder}/{file}").convert("L").convert("RGBA")
            image = image.resize((64, 64))
            images.append(image)

    for sample in samples:
        hits = []
        
        with open(f"trained_models/model_{sample[0]}_t{tolerance}.csv", "w") as file:
            file.write("distance,weight\n")

        temp_models = []

        print(CYAN + f"training on {sample[0]}/tolerance-{tolerance}")

        for image in images:
            gather = []
            for x in range(0, 64):
                for y in range(0, 64):
                    r, g, b, a = image.getpixel((x, y))
                    gather.append([x, y, numba_transform(r, g, b, a, tolerance)])

            # transform
            count = 0
            temp_var = 0
            models = []
            gather.sort(key = lambda x: x[2])
            for temp in gather:
                if temp_var != temp[2]:
                    count += 1
                    models.append([temp[0], temp[1], count])

                else:
                     models.append([temp[0], temp[1], count])

                temp_var = temp[2]

            models.sort(key = lambda x: (str(x[0]), str(x[1]), str(x[2])))

            # convert to correct size for distance formula to work
            init_new_model = []
            new_model = []
            old_x = 0
            for model in models:
                init_new_model.append(model[2])

                if old_x != model[0]:
                    new_model.append(init_new_model)
                    init_new_model = []

                old_x = model[0]

            results = calculate_distance(new_model)
            for result in results:
                hits.append(result)

        data = Counter(hits).most_common(sample[1])
        
        with open(f"trained_models/model_{sample[0]}_t{tolerance}.csv", "a") as file:
            for i in data:
                file.write(f"{i[0]},{i[1]}\n")
                
def main():
    os.system("clear")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-mode", required = True, type = str, choices = ["train"])
    parser.add_argument("-model", required = True, type = str)
    parser.add_argument("-tolerance", required = False, type = int)
    args = parser.parse_args()

    if args.mode == "generate":
        generate(args.model)

    if args.mode == "train":
        samples = [["low", 100],
                   ["medium", 1000],
                   ["large", 10000],
                   ["xl", 100000],
                   ["infinite", 1000000]]

        tolerances = [1, 2, 4, 8, 16, 32, 64]

        for tolerance in tolerances:
            train(samples, args.model, tolerance)

if __name__ == "__main__":
    main()
