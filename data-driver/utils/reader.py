import os
import csv

fields = ['product'
'brewer_value',
'brand_value',
'package_value',
'segment_value',
'ab_segment_value',
'ab_subsegment_value',
'ab_megasegment_value',
'date ',
'display_count',
'display_share',
'distribution',
'feature_count',
'feature_share',
'price_per_unit',
'price_per_volume',
'unit_sales',
'volume_sales',
'volume_share_of_category',
'average_of_max_temperaturec',
'average_of_mean_temperaturec',
'average_of_min_temperaturec',
'average_of_dew_pointc',
'average_of_meandew_pointc',
'average_of_min_dewpointc',
'average_of_max_humidity',
'average_of_mean_humidity',
'average_of_min_humidity',
'average_of_max_sea_level_pressurehpa',
'average_of_mean_sea_level_pressurehpa ',
'average_of_min_sea_level_pressurehpa',
'average_of_max_visibilitykm',
'average_of__mean_visibilitykm',
'average_of__min_visibilitykm',
'average_of__max_wind_speedkmh',
'average_of__mean_wind_speedkmh',
'average_of__max_gust_speedkmh',
'average_of_precipitationmm',
'average_of__cloudcover',
'average_of_winddirdegrees',
'state_gdp',
'alcohol_retail_trade_employees',
'state_personal_income',
'resident_population_in_city',
'per_capita_personal_income_in_city',
'occupancy',
'labor_force_in_city',
'employment_in_city',
'unemployment_in_city',
'unemp_rate_in_city',
'consumer_price_index_malt_beverages',
'consumer_price_index_wine',
'producer_price_index_by_industry'
]

X_labels = fields

Y_labels = [
'unit_sales',
'volume_sales',
'volume_share_of_category'
]

for y in Y_labels:
    X_labels = list(filter(lambda a: a != y, X_labels))

print(X_labels)
print(Y_labels)

def read_file(input_file):
    count = 0
    X = []
    Y = []
    with open(input_file) as infile:
        csv_reader = csv.DictReader(infile, fieldnames=fields)
        next(csv_reader)
        for row in csv_reader:
            input_row = ()
            for label in X_labels:
                input_row = input_row + ( row[label] , )
            X.append(input_row)
            output_row = ()
            for target in Y_labels:
                output_row = output_row + ( row[label] , )
            Y.append(output_row)
            count += 1
            if( count % 100 == 0):
                print(count)
                break
    return (X, Y)

(X, Y) = read_file('data/sales_data.csv')
print(X)
print(Y)
