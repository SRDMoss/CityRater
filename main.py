from modules.db_init import generate_cities
from modules.point_config import point_values as pv
from modules.point_config import point_weights as pw


top_cities = []


def calculate_points(doc, pw=pw, pv=pv):
    total = 0

    def get_bin(value, keys):
        bin = 0
        for key in keys:
            if float(value) > float(key):
                bin = key
            else:
                break
        return bin

    ## City Stats ##
    pop_bin = get_bin(doc['population'], pv['city_stats']['population'].keys())    
    total += pv['city_stats']['population'][pop_bin] * pw['city_stats']['population']

    total += pv['city_stats']['lang_2'][doc['lang_1']] * pw['city_stats']['lang_2']
    total += pv['city_stats']['lang_2'][doc['lang_1']] * pw['city_stats']['lang_2']

    total += pv['city_stats']['continent'][doc['continent']] * pw['city_stats']['continent']  

    ## Weather ##
    rain_bin = get_bin(doc['annual_rainy_days'], pv['weather']['annual_rainy_days'].keys())    
    total += pv['weather']['annual_rainy_days'][rain_bin] * pw['weather']['annual_rainy_days']

    snow_bin = get_bin(doc['annual_snow_days'], pv['weather']['annual_snow_days'].keys())    
    total += pw['weather']['annual_snow_days'] * pv['weather']['annual_snow_days'][snow_bin]

    total += pv['weather']['cold_month'][doc['cold_month']] * pw['weather']['cold_month']
    total += pv['weather']['hot_month'][doc['hot_month']] * pw['weather']['hot_month']

        # Temperatures    
    cold_low_bin = get_bin(doc['cold_month_ave_low_temp'], pv['weather']['cold_month_ave_low_temp'].keys())
    cold_high_bin = get_bin(doc['cold_month_ave_high_temp'], pv['weather']['cold_month_ave_high_temp'].keys())
    hot_low_bin = get_bin(doc['hot_month_ave_low_temp'], pv['weather']['hot_month_ave_low_temp'].keys())
    hot_high_bin = get_bin(doc['hot_month_ave_high_temp'], pv['weather']['hot_month_ave_high_temp'].keys())

    total += pv['weather']['cold_month_ave_low_temp'][cold_low_bin] * pw['weather']['cold_month_ave_low_temp']  
    total += pv['weather']['cold_month_ave_high_temp'][cold_high_bin] * pw['weather']['cold_month_ave_high_temp'] 
    total += pv['weather']['hot_month_ave_low_temp'][hot_low_bin] * pw['weather']['hot_month_ave_low_temp']
    total += pv['weather']['hot_month_ave_high_temp'][hot_high_bin] * pw['weather']['hot_month_ave_high_temp']


    ## Government ##
    total += pv['government']['basis_of_legitimacy'][doc['basis_of_legitimacy']] * pw['government']['basis_of_legitimacy']
    total += pv['government']['constitutional_form'][doc['constitutional_form']] * pw['government']['constitutional_form']
    total += pv['government']['head_of_state'][doc['head_of_state']] * pw['government']['head_of_state']

        # Health System
    for key in pv["government"]['health_system']:
        if doc['health_system'][:3] == key:
            total += pv["government"]['health_system'][key] * pw["government"]['health_system']
            # print(total)
        if doc['health_system'][-3:] == key:
            total += pv["government"]['health_system'][key] * pw["government"]['health_system']
            # print(total)

        # Laws    
            # Firearms
    total += pv['government']['laws_firearms']['handguns'][doc['handguns']] * pw['government']['laws_firearms']['handguns']
    total += pv['government']['laws_firearms']['long_guns'][doc['long_guns']] * pw['government']['laws_firearms']['long_guns']
    total += pv['government']['laws_firearms']['automatics'][doc['automatics']] * pw['government']['laws_firearms']['automatics']
    total += pv['government']['laws_firearms']['open_carry'][doc['open_carry']] * pw['government']['laws_firearms']['open_carry']
    total += pv['government']['laws_firearms']['concealed_carry'][doc['concealed_carry']] * pw['government']['laws_firearms']['concealed_carry']
    total += pv['government']['laws_firearms']['registration'][doc['registration']] * pw['government']['laws_firearms']['registration']
            # Abortion    
    total += pv['government']['laws_abortion']['risk_to_life'][doc['risk_to_life']] * pw['government']['laws_abortion']['risk_to_life']
    total += pv['government']['laws_abortion']['risk_to_health'][doc['risk_to_health']] * pw['government']['laws_abortion']['risk_to_health']
    total += pv['government']['laws_abortion']['rape'][doc['rape']] * pw['government']['laws_abortion']['rape']
    total += pv['government']['laws_abortion']['fetal_impairment'][doc['fetal_impairment']] * pw['government']['laws_abortion']['fetal_impairment']
    total += pv['government']['laws_abortion']['economic_social'][doc['economic_social']] * pw['government']['laws_abortion']['economic_social']
    total += pv['government']['laws_abortion']['on_request'][doc['on_request']] * pw['government']['laws_abortion']['on_request']
            # LGBT
    total += pv['government']['laws_lgbt']['same_sex_sexual_activity'][doc['same_sex_sexual_activity']] * pw['government']['laws_lgbt']['same_sex_sexual_activity']
    total += pv['government']['laws_lgbt']['same_sex_unions'][doc['same_sex_unions']] * pw['government']['laws_lgbt']['same_sex_unions']
    total += pv['government']['laws_lgbt']['same_sex_marriage'][doc['same_sex_marriage']] * pw['government']['laws_lgbt']['same_sex_marriage']
    total += pv['government']['laws_lgbt']['same_sex_adoption'][doc['same_sex_adoption']] * pw['government']['laws_lgbt']['same_sex_adoption']
    total += pv['government']['laws_lgbt']['open_in_military'][doc['open_in_military']] * pw['government']['laws_lgbt']['open_in_military']
    total += pv['government']['laws_lgbt']['anti_disc_laws'][doc['anti_disc_laws']] * pw['government']['laws_lgbt']['anti_disc_laws']
    total += pv['government']['laws_lgbt']['gender_positive_laws'][doc['gender_positive_laws']] * pw['government']['laws_lgbt']['gender_positive_laws']
    total += pv['government']['laws_lgbt']['no_anti_lgbt_laws'][doc['no_anti_lgbt_laws']] * pw['government']['laws_lgbt']['no_anti_lgbt_laws']

    return total

counter = 0

for city_doc in generate_cities():

    points = calculate_points(city_doc)
    top_cities.append((points, city_doc))
    top_cities = sorted(top_cities, key=lambda x: x[0], reverse=True)


with open("all_cities.txt", mode="a") as file:
    for i in range(len(top_cities)):
        file.write(f"{i+1}: {top_cities[i][1]['city']}, {top_cities[i][1]['country']}: {top_cities[i][0]}\n")


