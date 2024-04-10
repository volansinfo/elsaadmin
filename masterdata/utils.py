# from .models import Axxess

# def get_axxess_data(species, ingredients):
#     # Retrieve data from the Axxess model
#     data = Axxess.objects.filter(species=species, ingredients__in=ingredients)

#     result = []

#     # Iterate over the queryset and populate the result list
#     for record in data:
#         species = record.species
#         ingredients = record.ingredients
#         sol_ax = record.sol_ax
#         insol_ax = record.insol_ax
#         me = record.me
#         ne = record.ne
#         me_kcal = record.me_kcal

#         result.append({
#             'Id' : id,
#             'Species': species,
#             'Ingredients': ingredients,
#             'Sol_AX': sol_ax,
#             'Insol_AX': insol_ax,
#             'ME': me,
#             'NE': ne,
#             'ME Kcal': me_kcal
#         })

#     # Print a message to indicate when the loop is done
#     print('done')

#     # Return the result list
#     return result
from .models import masterdata_axxess

def get_axxess_data(species, ingredients):
    # Retrieve data from the Axxess model
    data = masterdata_axxess.objects.filter(species=species, ingredients__in=ingredients)

    result = []

    # Iterate over the queryset and populate the result list
    for record in data:
        result.append({
            'Id' : record.id,
            'Species': record.species,
            'Ingredients': record.ingredients,
            'Sol_AX': record.sol_ax,
            'Insol_AX': record.insol_ax,
            'ME': record.me,
            'NE': record.ne,
            'ME Kcal': record.me_kcal
        })

    # Print a message to indicate when the loop is done
    print('done')

    # Return the result list
    return result
