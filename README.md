# Benford's Law Applied to COVID-19 Reports

**A look at COVID-19 case reports around the world to see how well the numbers of daily positive cases fit into Benford's Law. The better the fit, the more likely the data for the location to be accurate and trustworthy.**

### What is Benford's Law?

Numbers that represent real-life events follow a certain regularity. Specifically, the first digit of these numbers follows a strange pattern with the number 1 appearing about 30% of the time, the number 2 about 18% of the time, etc. -- a frequency that declines in a logarithmic way. This pattern is known as the Benford's Law, and it can be used to identify fraud and other irregularities with reported numbers. To learn more, see the [wikipedia page](https://en.wikipedia.org/wiki/benford's_law).

### How does it apply to COVID-19 numbers?

I obtained the daily positive case numbers for the U.S. (data source: [Covid Tracking Project](https://covidtracking.com/)) and the countries around the world (data source: [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19)). For each reporting location, I computed the frequency of numbers 1 to 9 in the first digit of the positive case numbers and compared it the Benford frequency, and the difference is the error. I used this error to rank the locations - U.S. states and world countries - from best (smallest error) to worst (largest error), and created plots for each location that show the error from Benford visually.

### What are the results?

`usa_rank.csv` - use this file to see how each U.S. state or territory ranks from best to worst, based on how their COVID-19 case numbers fit into Benford's Law. The last column has the file name with the visual plot for the state or territory.

`usa_output/` - directory with the visual plots for each U.S. state or territory.

`world_rank.csv` - use this file to see how each country and province ranks from best to worst, based on how their COVID-19 case numbers fit into Benford's Law. The last column has the file name with the visual plot for the location.

`world_output/` - directory with the visual plots for each country or province.

### How to interpret the results?

For the U.S., the error ranges from 0.08 for Oregon to 0.55 for New Jersey. For the world, the error ranges from 0.06 for Jordan, to 1.05 for Mordovia, Russia. When the error is small, the COVID-19 cases reported for the location are more likely to be accurate and trustworthy. And as the error increases, so does the doubt into the accuracy of the COVID-19 cases. Large errors could be a sign of insufficient testing, misreporting, or direct falsification.

February 28, 2021

