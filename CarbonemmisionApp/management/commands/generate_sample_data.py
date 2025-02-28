from django.core.management.base import BaseCommand
from windsurf.models import Organization, CarbonEmission
from datetime import datetime, timedelta
import numpy as np

class Command(BaseCommand):
    help = 'Generates sample data for carbon emissions'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Organization.objects.all().delete()
        CarbonEmission.objects.all().delete()

        # Create organizations
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

        # Generate 2 years of daily data for each organization
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=730)
        dates = [start_date + timedelta(days=x) for x in range(731)]

        for org in orgs:
            # Set base values and trends for each organization
            if org.name == 'Tech Corp':
                base_emission = 800
                trend = 0.1  # Slight increase
                seasonal_factor = 50
                noise_factor = 20
            elif org.name == 'Green Manufacturing':
                base_emission = 3000
                trend = -0.3  # Decreasing trend
                seasonal_factor = 200
                noise_factor = 100
            else:  # EcoLogistics
                base_emission = 2000
                trend = 0.2  # Moderate increase
                seasonal_factor = 150
                noise_factor = 80

            # Generate emissions data
            for i, date in enumerate(dates):
                # Calculate components with trends and seasonality
                day_of_year = date.timetuple().tm_yday
                
                # Trend component
                trend_component = i * trend
                
                # Seasonal component (yearly cycle)
                seasonal_component = seasonal_factor * np.sin(2 * np.pi * day_of_year / 365)
                
                # Weekly pattern (higher on weekdays)
                weekly_component = -50 if date.weekday() >= 5 else 50
                
                # Random noise
                noise = np.random.normal(0, noise_factor)
                
                # Calculate total emissions and components
                total = base_emission + trend_component + seasonal_component + weekly_component + noise
                
                # Ensure no negative values
                total = max(total, 0)
                
                # Create emission record
                CarbonEmission.objects.create(
                    organization=org,
                    date=date,
                    total_emissions=total,
                    energy_consumption=total * 0.4 + np.random.normal(0, noise_factor * 0.1),
                    transportation_emissions=total * 0.35 + np.random.normal(0, noise_factor * 0.1),
                    waste_emissions=total * 0.25 + np.random.normal(0, noise_factor * 0.1)
                )

        self.stdout.write(self.style.SUCCESS('Successfully generated sample data'))
