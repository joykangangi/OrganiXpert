"""
Function to determine the number of bags of fertilizer required
Parameters: nutrient_requirements, soil_content, predicted_fertilizer
Returns: number_of_bags
"""


def determine_number_of_bags(nutrient_requirements, soil_content, predicted_fertilizer):
    number_of_bags = 0
    if predicted_fertilizer == 'Safi Sarvi Planting Fertilizer':
        nitrogen_content_in_fertilizer = 1.5
        phosphorus_content_in_fertilizer = 2.5
        potassium_content_in_fertilizer = 1.5
        nitrogen_deficit = nutrient_requirements[0] - soil_content[0]
        phosphorus_deficit = nutrient_requirements[1] - soil_content[1]
        potassium_deficit = nutrient_requirements[2] - soil_content[2]
        # get the total deficit values for all the nutrients
        total_deficit = nitrogen_deficit + phosphorus_deficit + potassium_deficit
        # get the total content of the nutrients in the fertilizer
        total_nutrient_content_in_fertilizer = nitrogen_content_in_fertilizer + phosphorus_content_in_fertilizer + potassium_content_in_fertilizer
        # get the number of bags of fertilizer required
        number_of_bags = total_deficit / total_nutrient_content_in_fertilizer
    elif predicted_fertilizer == 'Safi Biochar':
        nitrogen_content_in_fertilizer = 1.7
        phosphorus_content_in_fertilizer = 1.7
        potassium_content_in_fertilizer = 1.7
        nitrogen_deficit = nutrient_requirements[0] - soil_content[0]
        phosphorus_deficit = nutrient_requirements[1] - soil_content[1]
        potassium_deficit = nutrient_requirements[2] - soil_content[2]
        # get the total deficit values for all the nutrients
        total_deficit = nitrogen_deficit + phosphorus_deficit + potassium_deficit
        # get the total content of the nutrients in the fertilizer
        total_nutrient_content_in_fertilizer = nitrogen_content_in_fertilizer + phosphorus_content_in_fertilizer + potassium_content_in_fertilizer
        # get the number of bags of fertilizer required
        number_of_bags = total_deficit / total_nutrient_content_in_fertilizer
    elif predicted_fertilizer == 'Safi Sarvi Topper':
        nitrogen_content_in_fertilizer = 2.5
        phosphorus_content_in_fertilizer = 1.5
        potassium_content_in_fertilizer = 1.5
        nitrogen_deficit = nutrient_requirements[0] - soil_content[0]
        phosphorus_deficit = nutrient_requirements[1] - soil_content[1]
        potassium_deficit = nutrient_requirements[2] - soil_content[2]
        # get the total deficit values for all the nutrients
        total_deficit = nitrogen_deficit + phosphorus_deficit + potassium_deficit
        # get the total content of the nutrients in the fertilizer
        total_nutrient_content_in_fertilizer = nitrogen_content_in_fertilizer + phosphorus_content_in_fertilizer + potassium_content_in_fertilizer
        # get the number of bags of fertilizer required
        number_of_bags = total_deficit / total_nutrient_content_in_fertilizer
    else:
        print('No fertilizer was recommended')
    return number_of_bags