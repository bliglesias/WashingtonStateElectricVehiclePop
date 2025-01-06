'''
Brandon Iglesias
5/21/24

Final Project
What is the most predominant electric vehicle type? (BEV or HYBRID)
What county has the most electric vehicles?
What is the ratio of electric vehicles that are officially clean alternatives?
'''

# Import libraries
import statistics as stats
import matplotlib.pyplot as plt
import seaborn as sb
from myFunctions import *

# print title
printTitle()

# Read and open the file
textFilePrime = open("CleanedElectricDataTwice.csv")
dataRowsPrime = textFilePrime.readlines()[1:]
textFilePrime.close()

textFile = open("CleanedTotalVehiclePop2023-24.csv")
dataRows = textFile.readlines()[1:]
textFile.close()

# declare lists(they should be empty) -- prime
primeVIN = []
primeCounty = []
primeCity = []
primeModelYear = []
primeMake = []
primeModel = []
primeElectricVehicleType = []
primeCAFE = []
primeElectricRange = []
primeElectricUtility = []

# addendum variables-> prime
cleanAlt = 0
cleanList = []

notClean = 0
notCleanList = []

hybrid = 0
listHybrid = []

fullElectric = 0
listFullElectric = []

hybridMiles = []
electricMiles = []

# declare lists (they should be empty) -- secondary
secondaryFiscalYear = []
secondaryFuelType = []
secondaryPrimaryUseClass = []
secondaryCounts = []


# process the file -- secondary
for row in dataRows:

  # strip the row -- secondary
  row = row.strip()

  # unpack the elements -- secondary
  fiscalYear, transactionDate, transactionCounty, residentialCounty, fuelType, primaryUseClass, counts = row.split(",")

  # convert str --> int for calc/loops ------- hmmm remove? Bro this project is a hot-mess
  counts = int(counts)
  fiscalYear = int(fiscalYear)

  # get the number of vehicles NOT electric or unpowered
  #if fiscalYear == 2023 or fiscalYear == 2024:
  if fuelType != "Electric" and fuelType != "Unpowered":
    secondaryCounts.append(counts) #add them to the list 
  
  # append to lists -- secondary
  secondaryFiscalYear.append(fiscalYear)
  secondaryFuelType.append(fuelType)
  secondaryPrimaryUseClass.append(primaryUseClass)
  #secondaryCounts.append(counts)
#end for loop

# ----------------------------------------------------------------------#
  # process the file -- prime
for row in dataRowsPrime:

  # strip the row -- prime
  row = row.strip()

  # unpack the elements -- prime
  VIN, county, city, modelYear, make, model, electricVehicleType, cleanAlternativeFuelVehicleEligibility, electricRange, electricUtility = row.split(",")

  # convert str to int
  if cleanAlternativeFuelVehicleEligibility == "Clean Alternative Fuel Vehicle Eligible":
    cleanAlt += 1
    cleanList.append(cleanAlt)
  else:
    notClean += 1
    notCleanList.append(notClean)
  if electricVehicleType == "Battery Electric Vehicle (BEV)":
    hybrid += 1
    listHybrid.append(hybrid)
    hybridMiles.append(int(electricRange))
    primeModelYear.append(int(modelYear))
  else:
    fullElectric += 1
    listFullElectric.append(fullElectric)
    if electricRange != "0" or electricRange != 0:
      electricMiles.append(int(electricRange))
      #primeModelYear.append(int(modelYear))


#end for loop

# open and read the file - xy scatterplot assignment
with open("filtered_data.csv") as file:
  newData = file.readlines()[1:]

  #test functionality - works
  #print(newData)

listModelYear = []
listElectricMiles = []

# for-loop
for row in newData:

  #remove line breaks
  row = row.strip()

  #unpack values
  year,electricRange = row.split(",")

  #convert to int
  year = int(year)
  electricRange = int(electricRange)

  #ensure functionality - operational
  #print(year)
  #print(electricRange)

  listModelYear.append(year)
  listElectricMiles.append(electricRange)
# end loop

# data import complete -- prompt Questions
questions()

# Read the user input into a variable - Seadrah
inputNumber = input("\nEnter a question number: ")
inputNumber = int(inputNumber)

# Validate the choice (1-3)
# As long as choice is less than one or greater than 3, prompt again
while inputNumber < 1 or inputNumber > 5:
  inputNumber = int(input("Invalid. Enter 1-5: "))

  # Question 1 - What is the most predominant electric vehicle type? (BEV or HYBRID)
if inputNumber == 1:
  print("\nFully Electric: ",len(listFullElectric))
  print("\nHybrids: ",len(listHybrid))

  fullElectric = len(listFullElectric)
  typeHybrid = len(listHybrid)
  engineType = ['Fully Electric', 'Hybrid']
  numOfCars = [fullElectric, typeHybrid]
  sb.barplot (x=engineType, y=numOfCars)
  plt.title("Prodominant Engine Type for Electric Vehicles 23'-24'")
  plt.xlabel("Electric Vehicle Engine Type")
  plt.ylabel("Number of Cars from Jan 2023 - May 2024")
  plt.text(20000, 12, '39485', zorder =5)
  plt.show()
  

  # Question 2 - Number of vehicles in WA that are electric?
elif inputNumber == 2: #bar graph ---> chnage to puie chart
  cleanAlternative = len(cleanList)
  notEligible = len(notCleanList)
  
  totalElectric = cleanAlternative + notEligible
  totalNonElectric = len(secondaryCounts)
  totalVehicles = totalElectric + totalNonElectric
  #print("Total Electric: ",totalElectric )
  #print("Combustion Engine: ", totalNonElectric)
  #print("Total Registered Cars: ", totalVehicles)
  #print(len(secondaryCounts))
  print("Total number of registered vehicles in WA: ",format(totalVehicles, ","))
  engineTypes = ['Electric', 'Combustion']
  numOfCars = [totalNonElectric, totalElectric]
  sb.barplot (x=engineTypes, y=numOfCars)
  plt.title("Total Registered Vehicles in 2023 - (319,349)")
  plt.ylabel("Number of Vehicles")
  plt.show()
  
  # Question 3 - What is the ratio of electric vehicles that are officially clean alternatives?
elif inputNumber == 3: #pie chart

  #conversion of measurement to percentage
  cleanAlternative = len(cleanList)
  notEligible = len(notCleanList)
  totalCount = cleanAlternative + notEligible
  pctClean = round(cleanAlternative/totalCount * 100,2)
  pctNot = round(notEligible/totalCount * 100,2)

  #concatanate; str->int->str; needs str conversion
  cleanLabel = "Clean Alt (" + str(pctClean) + ") %"
  notCleanLabel = "Not an Alt (" + str(pctNot) + ") %"

  #produce results
  plt.title("2023 Percentage of Vehicles Eligible For Clean Alternatives")
  plt.pie([cleanAlternative, notEligible], labels=[cleanLabel, notCleanLabel])
  plt.show()

  # Avg miles per charge between model years
elif inputNumber == 4:
  print("\nMean Model Year: ", round(stats.mean(listModelYear),1))
  print("\nMean Electric Miles: ", round(stats.mean(listElectricMiles),1))

  sb.regplot(x=listModelYear, y=listElectricMiles)
  plt.title("Average Miles per charge by model year")
  plt.xlabel("Model Year")
  plt.ylabel("Miles per charge (100%)")
  plt.text(2000,150, "r=-0.0732", zorder=5)
  plt.show()

  # avg miles per type of vehicle Hybrid
elif inputNumber == 5:
  print("\nTotal Electric Miles: ",sum(electricMiles))
  print("\nTotal Number of Full Electric Vehicles",len(listFullElectric))

  print("\nTotal Hybrid Miles: ",sum(hybridMiles))
  print("\nTotal Number of Hybrid Cars",len(listHybrid))

  #primeModelYear = int(primeModelYear)
  #meanElectricMiles = stats.mean(electricMiles)
  #meanHybridMiles = stats.mean(hybridMiles)
  #meanYear = stats.mean(primeModelYear)

  #print(len(primeModelYear))
  plt.figure(figsize=(10, 6))  # Adjust figure size as needed
  sb.lineplot(x=primeModelYear, y=hybridMiles)
  plt.title("Electric Miles by Model Year")
  plt.xlabel("Model Year")
  plt.ylabel("Electric Miles")
  plt.show()
  
