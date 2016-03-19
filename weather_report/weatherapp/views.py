from django.shortcuts import render

import os
from libs.my_models import my_models

def index(request):
    return render(request, 'weatherapp/index.html', {})

def kmeans(request):
    try:
        k = int(request.POST['k'])
    except ValueError:
        return render(request, 'weatherapp/index.html', {'error_message': 'You must submit a integer!',})
    else:
        if k<1 or k>10:
            return render(request, 'weatherapp/index.html', {'error_message': 'K must be between 1-10!',})
        else:
            model = my_models()
            tr = model.get_training_data(str(os.getcwd())+"/weather_report/static")
            try:
                means, cls = model.k_means(tr, k, 20)
            except ValueError:
                return render(request, 'weatherapp/index.html', {'error_message': 'One or more of the clusters were empty! Please try again!',})
            else:
                closest, mean_indx = model.get_closest_to_mean(tr, means, cls)
                return render(request, 'weatherapp/index.html', {'mean_indx': mean_indx, 'run': 1})


def kmeanspp(request):
    try:
        k = int(request.POST['k'])
    except ValueError:
        return render(request, 'weatherapp/index.html', {'error_message': 'You must submit a integer!',})
    else:
        if k<1 or k>10:
            return render(request, 'weatherapp/index.html', {'error_message': 'K must be between 1-10!',})
        else:
            model = my_models()
            tr = model.get_training_data(str(os.getcwd())+"/weather_report/libs/ml-stuff/pics")
            try:
                means, cls = model.k_means_pp(tr, k, 20)
            except ValueError:
                return render(request, 'weatherapp/index.html', {'error_message': 'One or more of the clusters were empty! Please try again!',})
            else:
                closest, mean_indx = model.get_closest_to_mean(tr, means, cls)
                return render(request, 'weatherapp/index.html', {'mean_indx': mean_indx, 'run': 1})


def kmedoids(request):
    try:
        k = int(request.POST['k'])
    except ValueError:
        return render(request, 'weatherapp/index.html', {'error_message': 'You must submit a integer!',})
    else:
        if k<1 or k>10:
            return render(request, 'weatherapp/index.html', {'error_message': 'K must be between 1-10!',})
        else:
            model = my_models()
            tr = model.get_training_data(str(os.getcwd())+"/weather_report/static")
            try:
                means, cls = model.k_medoids(tr, k, 20)
            except ValueError:
                return render(request, 'weatherapp/index.html', {'error_message': 'One or more of the clusters were empty! Please try again!',})
            else:
                mean_indx = model.get_cluster_kernel_indx()
                return render(request, 'weatherapp/index.html', {'mean_indx': mean_indx, 'run': 1})
