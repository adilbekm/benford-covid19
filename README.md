# Benford's Law Applied to COVID-19 Case Reports

**A look at COVID-19 case reports around the world to see how well, or how poorly, the numbers of daily positive cases from each location fit into Benford's Law. The better the fit, the more likely the data to be accurate and trustworthy.**

### What is Benford's Law?

Numbers that represent real-life events follow a certain regularity. Specifically, the first digit of these numbers is distributed non-uniformly, with the number 1 appearing about 30% of the time, the number 2 about 18% of the time, etc. - having a frequency that declines in a logarithmic way. This pattern is known as the Benford's Law and it can be used to identify fraud and other irregularities with reported numbers.

### How Does This Work with COVID-19?

Using the .. for the U.S. data, and the .. for the world data, I obtained the daily positive case numbers by country, state, or province. These daily case numbers  

I obtained the daily positive case numbers for the U.S. states (data source: [Covid Tracking Project](https://covidtracking.com/)) and countries and provinces around the world (data source: [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19)), and computed the frequency of numbers 1 to 9 in the first digit of each number by location. I compared the frequencies with the expected frequencies by Benford, and calculated the difference, or the error. I used this error to rank the locations from the smallest (best fit) to the largest (worse fit), and also created plots for each location showing the difference.



For example, Malaysia has reported 373 numbers of daily positive cases in the period from January 23, 2020 to February 27, 2021. I found that the frequency of the number 1 in the first digit of those numbers was 0.37. 

I collected COVID-19 reports around the world to see how well, or how poorly, the numbers of daily positive cases from each location fit into Benford's Law. The better a report fits into the pattern, the more likely it is to be accurate and trustworthy. 



In this project, I applied Benford's Law to the reported numbers of COVID-19 cases around the world to see how well the numbers fit the expected pattern. 

February 28, 2021

