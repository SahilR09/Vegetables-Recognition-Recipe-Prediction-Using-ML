from django.shortcuts import render, redirect
import tensorflow as tf
import numpy as np
from django.core.files.storage import default_storage
from django.conf import settings
import os
import csv
from django.contrib.auth.decorators import login_required

# Paths for the new model and labels
MODEL_PATH = "keras_model.h5"  # Update with actual path
LABELS_PATH = "labels.txt"    # Update with actual path
RECIPES_PATH = "IndianFoodDatasetCSV_1.csv"

# Try to load the model and catch errors if it fails
try:
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)  # Avoid compile=True for older models
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

# Load labels from the text file
def load_labels():
    try:
        with open(LABELS_PATH) as f:
            return [line.strip() for line in f]
    except Exception as e:
        print(f"Error loading labels: {e}")
        return []

labels = load_labels()

# Function to make a prediction from the model
def model_prediction(image_path):
    try:
        image = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.array([input_arr])  # Convert single image to a batch
        input_arr = (input_arr / 127.5) - 1  # Normalize the image
        prediction = model.predict(input_arr)
        return np.argmax(prediction)
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

# Load recipes from CSV
def load_recipes():
    recipes = {}
    try:
        with open(RECIPES_PATH, mode='r') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                veg_name = row['VegNames']
                if veg_name not in recipes:
                    recipes[veg_name] = []
                recipes[veg_name].append({
                    'RecipeName': row['RecipeName'],
                    'Ingredients': row['Ingredients'],
                    'PrepTimeInMins': row['PrepTimeInMins'],
                    'CookTimeInMins': row['CookTimeInMins'],
                    'Cuisine': row['Cuisine'],
                    'Instructions': row['Instructions']
                })
    except Exception as e:
        print(f"Error loading recipes: {e}")
    return recipes

recipes = load_recipes()

# Views
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def prediction(request):
    context = {}
    if request.method == 'POST' and request.FILES.getlist('files'):
        files = request.FILES.getlist('files')
        uploaded_image_urls = []
        predictions = []
        predicted_labels = []
        youtube_videos = []

        for file in files:
            file_path = default_storage.save(file.name, file)
            abs_path = os.path.join(settings.MEDIA_ROOT, file_path)
            uploaded_image_urls.append(default_storage.url(file_path))

            if 'predict' in request.POST and model:
                result_index = model_prediction(abs_path)
                if result_index is not None:
                    predicted_label = labels[result_index]
                    predictions.append(predicted_label)
                    predicted_labels.append(predicted_label)
                else:
                    predictions.append('Error in prediction')
                    predicted_labels.append('Unknown')

        # Fetch recipes, limit to 5 per predicted label
        predicted_items = [recipes.get(label, [])[:5] for label in predicted_labels]
        context['uploaded_image_urls'] = uploaded_image_urls
        context['predictions'] = predictions
        context['predicted_items'] = predicted_items

        # Fetch YouTube videos based on the predicted label
        if predicted_labels:
            first_predicted_label = predicted_labels[0]  # Take the first prediction
            youtube_videos = fetch_youtube_videos(first_predicted_label)
        
        context['youtube_videos'] = youtube_videos

    return render(request, 'prediction.html', context)


#################

from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def ProfilePage(request):
    logout(request)
    return render (request,'profile.html')

#################################################
from googleapiclient.discovery import build

# YouTube API settings
YOUTUBE_API_KEY = 'AIzaSyCCmPeXO9ni0BeqLsBd0w_pnFBsIFMRx_E'  # Your API key
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def fetch_youtube_videos(query, max_results=5):
    try:
        search_query = f"{query} Indian recipe "

        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
        search_response = youtube.search().list(
            q=search_query,
            part='snippet',
            maxResults=max_results,
            type='video'
        ).execute()
        
        videos = []
        for item in search_response.get('items', []):
            video_data = {
                'title': item['snippet']['title'],
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                'thumbnail': item['snippet']['thumbnails']['default']['url']
            }
            videos.append(video_data)
        
        return videos
    except Exception as e:
        print(f"Error fetching YouTube videos: {e}")
        return []


###############################################
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FavouriteRecipe

@login_required(login_url='login')
def add_to_favourites(request, recipe_name):
    if request.method == 'POST':
        # Get recipe data from the POST request
        ingredients = request.POST.get('ingredients')
        prep_time = request.POST.get('prep_time')
        cook_time = request.POST.get('cook_time')
        cuisine = request.POST.get('cuisine')
        instructions = request.POST.get('instructions')

        # Create the FavouriteRecipe entry
        FavouriteRecipe.objects.create(
            user=request.user,
            recipe_name=recipe_name,
            ingredients=ingredients,
            prep_time=prep_time,
            cook_time=cook_time,
            cuisine=cuisine,
            instructions=instructions
        )

        return redirect('favourites')

@login_required(login_url='login')
def favourites(request):
    # Get the favourite recipes for the logged-in user
    favourite_recipes = FavouriteRecipe.objects.filter(user=request.user)
    return render(request, 'favourites.html', {'favourite_recipes': favourite_recipes})


from django.shortcuts import get_object_or_404
from .models import FavouriteRecipe

@login_required(login_url='login')
def remove_from_favourites(request, recipe_id):
    # Fetch the favourite recipe using the recipe_id and delete it
    favourite_recipe = get_object_or_404(FavouriteRecipe, id=recipe_id, user=request.user)
    favourite_recipe.delete()

    # Redirect to the favourites page after removal
    return redirect('favourites')
