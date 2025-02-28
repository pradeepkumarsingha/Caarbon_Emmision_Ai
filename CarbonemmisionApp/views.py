from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from .models import Equipment, Event, BlogPost, Organization, CarbonEmission
import numpy as np
from datetime import datetime, timedelta
import json
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

# Create your views here.

def home(request):
    latest_equipment = Equipment.objects.order_by('-created_at')[:3]
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    latest_posts = BlogPost.objects.order_by('-created_at')[:3]
    
    context = {
        'latest_equipment': latest_equipment,
        'upcoming_events': upcoming_events,
        'latest_posts': latest_posts,
    }
    return render(request, 'windsurf/home.html', context)

def equipment_list(request):
    equipment = Equipment.objects.all().order_by('-created_at')
    return render(request, 'windsurf/equipment_list.html', {'equipment': equipment})

def event_list(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'windsurf/event_list.html', {'events': events})

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'windsurf/blog_list.html', {'posts': posts})

def contact(request):
    if request.method == 'POST':
        # Handle form submission here
        # You can add email sending functionality
        return render(request, 'windsurf/contact.html', {'message': 'Thank you for your message!'})
    return render(request, 'windsurf/contact.html')

def train_linear_model(emissions_data):
    """Train a linear regression model on historical data"""
    if len(emissions_data) < 30:
        return None, None, "Not enough historical data"

    # Convert to DataFrame
    dates = [e.date for e in emissions_data]
    emissions = [e.total_emissions for e in emissions_data]
    df = pd.DataFrame({
        'Date': pd.to_datetime(dates),  # Convert to pandas datetime
        'Carbon_Emissions': emissions
    })

    # Convert Date to numerical format (days since first date)
    first_date = df['Date'].min()
    df['Days_Since_Start'] = df['Date'].apply(lambda x: (x - first_date).days)

    # Scale features
    scaler = StandardScaler()
    df['Days_Scaled'] = scaler.fit_transform(df[['Days_Since_Start']])

    # Prepare features and target
    X = df[['Days_Scaled']].values
    y = df['Carbon_Emissions'].values

    # Train Linear Regression model
    model = LinearRegression()
    model.fit(X, y)

    # Calculate R2 score
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)

    return model, scaler, r2

@csrf_exempt
def predict_emissions(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            org_name = data.get('organization')
            target_date_str = data.get('date')
            
            if not org_name or not target_date_str:
                return JsonResponse({
                    'error': 'Missing organization name or date'
                }, status=400)

            # Get organization and historical data
            org = Organization.objects.get(name=org_name)
            target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()

            # Get all historical data for better trend analysis
            historical_data = CarbonEmission.objects.filter(
                organization=org,
                date__lte=target_date
            ).order_by('date')

            if not historical_data:
                return JsonResponse({
                    'error': 'No historical data available'
                }, status=400)

            # Train model
            model, scaler, r2 = train_linear_model(historical_data)
            
            if model is None:
                return JsonResponse({'error': r2}, status=400)

            # Prepare prediction data
            first_date = historical_data[0].date
            days_since_start = (target_date - first_date).days
            X_pred = scaler.transform([[days_since_start]])
            prediction = model.predict(X_pred)[0]

            # Generate trend line data
            future_days = 90  # Show 3 months into future
            trend_dates = [target_date + timedelta(days=x) for x in range(-180, future_days)]
            trend_days = [(d - first_date).days for d in trend_dates]
            X_trend = scaler.transform([[d] for d in trend_days])
            trend_predictions = model.predict(X_trend)

            # Prepare response data
            response_data = {
                'prediction': round(float(prediction), 2),
                'r2_score': round(float(r2), 4),
                'model_info': {
                    'coefficient': round(float(model.coef_[0]), 4),
                    'intercept': round(float(model.intercept_), 4)
                },
                'historical_data': [
                    {
                        'date': e.date.strftime('%Y-%m-%d'),
                        'total': round(e.total_emissions, 2),
                        'energy': round(e.energy_consumption, 2),
                        'transport': round(e.transportation_emissions, 2),
                        'waste': round(e.waste_emissions, 2)
                    }
                    for e in historical_data
                ],
                'trend_line': [
                    {
                        'date': d.strftime('%Y-%m-%d'),
                        'prediction': round(float(p), 2)
                    }
                    for d, p in zip(trend_dates, trend_predictions)
                ]
            }

            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON data'
            }, status=400)
        except Organization.DoesNotExist:
            return JsonResponse({
                'error': 'Organization not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)

    return render(request, 'windsurf/carbon_prediction.html')
