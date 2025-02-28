from django.core.management.base import BaseCommand
from windsurf.models import Organization, CarbonEmission
from datetime import datetime, timedelta
import numpy as np

class Command(BaseCommand):
    help = 'Generates sample data for carbon emissions'

    def handle(self, *args, **kwargs):
        
        Organization.objects.all().delete()
        CarbonEmission.objects.all().delete()

        
        orgs = [
            Organization.objects.create(
                name='Tech Corp',
                industry_type='Technology'
            ),
            Organization.objects.create(
                name='Green Manufacturing',
                industry_type='Manufacturing'
            ),
            Organization.objects.create(
                name='EcoLogistics',
                industry_type='Transportation'
            )
        ]

       
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=730)
        dates = [start_date + timedelta(days=x) for x in range(731)]

        for org in orgs:
            
            if org.name == 'Tech Corp':
                base_emission = 800
                trend = 0.1  
                seasonal_factor = 50
                noise_factor = 20
            elif org.name == 'Green Manufacturing':
                base_emission = 3000
                trend = -0.3  
                seasonal_factor = 200
                noise_factor = 100
            else: 
                base_emission = 2000
                trend = 0.2  
                seasonal_factor = 150
                noise_factor = 80

           
            for i, date in enumerate(dates):
                
                day_of_year = date.timetuple().tm_yday
                
               
                trend_component = i * trend
                
               
                seasonal_component = seasonal_factor * np.sin(2 * np.pi * day_of_year / 365)
                
              
                weekly_component = -50 if date.weekday() >= 5 else 50
                
              
                noise = np.random.normal(0, noise_factor)
                
               
                total = base_emission + trend_component + seasonal_component + weekly_component + noise
                
               
                total = max(total, 0)
                
                
                CarbonEmission.objects.create(
                    organization=org,
                    date=date,
                    total_emissions=total,
                    energy_consumption=total * 0.4 + np.random.normal(0, noise_factor * 0.1),
                    transportation_emissions=total * 0.35 + np.random.normal(0, noise_factor * 0.1),
                    waste_emissions=total * 0.25 + np.random.normal(0, noise_factor * 0.1)
                )

        self.stdout.write(self.style.SUCCESS('Successfully generated sample data'))
