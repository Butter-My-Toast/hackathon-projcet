import requests
import html
import json
import time
import os


def retrieve_info(link):
    # clear local namespace
    for var in locals().copy():
        if var.startswith('__'):
            continue
        del locals()[var]
    website = requests.get(link)
    website = website.text.replace(
        'class=" raw__09f24__T4Ezm"', 'class="raw__09f24__T4Ezm"').replace("&quot;", "")
    split_response = website.split("{full:")
    reviews = []
    for part in split_response:
        split_response2 = part.split("__typename:ReviewText")[0]
        # FORMAT STRING HERE ! ! !
        if len(split_response2) < 4000:
            split_response2 = html.unescape(split_response2)
            split_response2 = split_response2.replace("\\n", "\n")
            # print(split_response2)
            split_response2 = split_response2[0:len(split_response2) - 1]
            reviews.append(split_response2)
            # print(split_response2)
        if (len(reviews) >= 20):
            break

    foodset = set()

    API_URL = "https://api-inference.huggingface.co/models/Dizex/InstaFoodRoBERTa-NER"
    headers = {"Authorization": "Bearer " + os.getenv('AIkey')}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    for review in reviews:
        ner_entity_results = query(review)

        for i in range(len(ner_entity_results)):
            if ner_entity_results[i]["word"][0] == ' ':
                ner_entity_results[i]["word"] = ner_entity_results[i]["word"][1:]
                ner_entity_results[i]["start"] += 1

        curfoodlist = []
        for i in range(len(ner_entity_results)):
            if i != 0 and (ner_entity_results[i]["start"] - ner_entity_results[i - 1]["end"]) <= 1:
                curfoodlist[-1] += (ner_entity_results[i]["word"])
            else:
                curfoodlist.append(ner_entity_results[i]["word"])

        for i in curfoodlist:
            foodset.add(i)

    fw = []

    # print(foodset)

    for food in foodset:
        fw.append([])
        for word in food.split():
            fw[len(fw) - 1].append(word.capitalize())
    for i in range(len(fw)):
        for j in range(len(fw)):
            if i == j:
                continue
            f1 = fw[i]
            f2 = fw[j]
            check1 = True
            for k in f1:
                check2 = False
                for l in f2:
                    if k in l:
                        check2 = True
                if not check2:
                    check1 = False
            if check1:
                fw[i].clear()
    ffoods = []
    for i in fw:
        if len(i) != 0:
            ffoods.append([i[0]])
            for j in range(1, len(i)):
                ffoods[len(ffoods) - 1].append(i[j])
    ff = []
    for i in ffoods:
        ff.append(i[0])
        for j in range(1, len(i)):
            ff[len(ff) - 1] = ff[len(ff) - 1] + ' ' + i[j]

    # print(ff)

    # Finds scores for each food

    foodlist = ff
    with open("ingredients.json") as f:
        ingredients_list = json.load(f)
    ingredients_plural_list = []
    for ingredient in ingredients_list:
        ingredients_plural_list.append(ingredient + "s")

    print(ingredients_list)
    print(foodlist)

    for i in reversed(range(len(foodlist))):
        food = foodlist[i]
        removed = False
        for ingredient in ingredients_list:
            if food == ingredient:
                foodlist.remove(food)
                removed = True
                break
        if not removed:
            for ingredient in ingredients_plural_list:
                if food == ingredient:
                    foodlist.remove(food)
                    break

    print(foodlist)

    reviewlist = reviews
    negativetotal = []
    neutraltotal = []
    positivetotal = []
    count = []

    API_URL = "https://api-inference.huggingface.co/models/yangheng/deberta-v3-large-absa-v1.1"
    headers = {"Authorization": f"Bearer {'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'}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    for food in foodlist:
        negativelist = []
        neutrallist = []
        positivelist = []
        for review in reviewlist:
            if (food.lower() in review.lower()) is True:
                input = "[CLS] " + review.lower() + " [SEP] " + food.lower() + " [SEP]"
                time.sleep(0.08)
                outdata = query({"inputs": input})
                # print(outdata)
                # outdata = outdata[0]
                outdata[0].sort(key=lambda x: x["label"])
                negativelist.append(outdata[0][0]["score"])
                neutrallist.append(outdata[0][1]["score"])
                positivelist.append(outdata[0][2]["score"])
        negativetotal.append(negativelist)
        neutraltotal.append(neutrallist)
        positivetotal.append(positivelist)
        count.append(len(negativelist))

    rawscore = []
    weightscore = []
    popularity = []
    for i in range(len(foodlist)):
        sum = 0
        for j in range(count[i]):
            sum += positivetotal[i][j] - negativetotal[i][j]
        if count[i] != 0:
            sum /= count[i]
        rawscore.append([sum, i])
        if count[i] >= 3:
            sum += 0.05
        weightscore.append([sum, i])
        popularity.append([count[i], i])

    rawscore.sort(reverse=True, key=lambda x: x[0])
    print("Raw Scores:")
    for i in range(min(len(rawscore), 3)):
        print(foodlist[rawscore[i][1]])

    weightscore.sort(reverse=True, key=lambda x: x[0])
    print("\nWeighted Scores:")
    for i in range(min(len(weightscore), 3)):
        print(foodlist[weightscore[i][1]])

    popularity.sort(reverse=True, key=lambda x: x[0])
    print("\nPopularity:")
    for i in range(min(len(popularity), 3)):
        print(foodlist[popularity[i][1]])

        weightscorefood = []
        weightscorerating = []
        for i in weightscore:
            weightscorerating.append(i[0])
            weightscorefood.append(foodlist[i[1]])

        popularityfood = []
        popularityrating = []
        for i in popularity:
            popularityrating.append(i[0])
            popularityfood.append(foodlist[i[1]])

    food_api_key = os.getenv('foodkey')

    popularityfood_calories = []
    weightscorefood_calories = []

    print("dfdsfds")
    calories = -1
    for n in range(3):
        try:
            response = requests.get(
                f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={food_api_key}&query={popularityfood[n]}')
            data = response.json()
            food_data = data['foods'][0]
            for i, nutrient in enumerate(food_data['foodNutrients']):
                if food_data['foodNutrients'][i]['nutrientName'] == 'Energy':
                    print("assigned")
                    calories = food_data['foodNutrients'][i]['value']
        except:
            calories = -1
            print("errored")

        popularityfood_calories.append(calories)

        try:
            response = requests.get(
                f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={food_api_key}&query={weightscorefood[n]}')
            data = response.json()
            food_data = data['foods'][0]
            for i, nutrient in enumerate(food_data['foodNutrients']):
                if food_data['foodNutrients'][i]['nutrientName'] == 'Energy':
                    calories = food_data['foodNutrients'][i]['value']
        except:
            calories = -1

        weightscorefood_calories.append(calories)

    # if calories = -1 then the food name is something obscure and can not be searched in

    items = [weightscorefood, weightscorerating, popularityfood, popularityrating, weightscorefood_calories,
             popularityfood_calories]
    return json.dumps(items)

