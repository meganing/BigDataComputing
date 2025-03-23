
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, max, col

# start the session
spark = SparkSession.builder \
.appName('Stock Analysis') \
.getOrCreate()

# read the dataset
df = spark.read.csv('gs://bigdata_assess2/indexProcessed.csv', sep=',',header=True, inferSchema=True)

# show the first 5 rows
print("Sample Data:")
df.show(5)

# show the schema
print("DataFrame Schema:")
df.printSchema()

# 1. Finds all unique stock indices in the dataset
print("Unique Stock Indices:")
unique_indices = df.select('Index').distinct()
unique_indices.show()

# 2. Calculates the average Open and Close prices for each index
print("Average Open and Close Prices for each Index:")
avg_prices = df.groupBy('Index').agg(avg('Open').alias('Average Open Price'), avg('Close').alias('Average Close Price'))
avg_prices.show()

# 3. Identifies the index with the highest CloseUSD value  
print("Index with the Highest CloseUSD Value:")
max_close_value = df.agg(max('CloseUSD')).first()[0]
highest_close = df.filter(col('CloseUSD') == max_close_value).select('Index', 'Date', 'CloseUSD')
highest_close.show()

# 4. Saves the results to GCS
print("Saving the results to GCS:")
unique_indices.write.csv('gs://bigdata_assess2/unique_indices.csv', header=True)
avg_prices.write.csv('gs://bigdata_assess2/avg_prices.csv', header=True)
highest_close.write.csv('gs://bigdata_assess2/highest_close.csv', header=True)


print("Unique Stock Indices saved to gs://bigdata_assess2/unique_indices.csv")
print("Average Open and Close Prices saved to gs://bigdata_assess2/avg_prices.csv")
print("Index with the Highest CloseUSD Value saved to gs://bigdata_assess2/highest_close.csv")

# Display the results summary
print("\nResults Summary:")
print("Number of unique indices: " + str(unique_indices.count()))
print("\nAverage Open and Close Prices for each Index:")
avg_prices.show()
print("\nIndex with the Highest CloseUSD Value:")
highest_close.show()

# stop the session
spark.stop()
print("Spark Session Stopped.")




 


