from django.shortcuts import render, get_object_or_404, redirect
from .models import Shop
from .forms import ShopForm, LocationForm
import math

EARTH_RADIUS = 6371


def create_shop(request):
    if request.method == "POST":
        form = ShopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("shops:shop-list")
    else:
        form = ShopForm()
    return render(request, "shops/create_shop.html", {"form": form})


def shop_list(request):
    shops = Shop.objects.all()
    return render(request, "shops/shop_list.html", {"shops": shops})


def update_shop(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if request.method == "POST":
        form = ShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            return redirect("shops:shop-list")
    else:
        form = ShopForm(instance=shop)
    return render(request, "shops/update_shop.html", {"form": form})


def location_view(request):
    form = LocationForm()
    return render(request, "shops/location.html", {"form": form})


def haversine_distance(lat1, lon1, lat2, lon2):
    # converting latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # calculate the differences between the latitudes and longitudes
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Apply the Haversine formula
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = EARTH_RADIUS * c

    return distance


def shop_within_distance(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            latitude = form.cleaned_data["latitude"]
            longitude = form.cleaned_data["longitude"]
            distance = form.cleaned_data["distance"]

            # print the received values for debugging
            print("Received values:")
            print("Latitude:", latitude)
            print("Longitude:", longitude)
            print("Distance:", distance)

            # manually using haversine formula
            shops = Shop.objects.all()
            nearby_shops = []
            for shop in shops:
                shop_distance = haversine_distance(
                    latitude, longitude, shop.latitude, shop.longitude
                )

                # print the calculated distance for each shop
                print("Shop:", shop.name)
                print("Shop Distance:", shop_distance)

                if shop_distance <= distance:
                    nearby_shops.append(shop)

            # print the list of nearby shops
            print("Nearby Shops:")
            for shop in nearby_shops:
                print(shop.name)

            return render(request, "shops/shops.html", {"shops": nearby_shops})
    else:
        form = LocationForm()
    return redirect("shops:location")
