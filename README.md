# IP Discharges Case Study
A new program seeking to reduce the number of unnecessary emergency department (ED) to inpatient (IP) admissions among Medicare patients was launched in 2017. This study seeks to evaluate whether there was a reduction in IP discharge rates during the period following the program
implementation (i.e. 2017-2018) compared to the baseline period of 2013-2016. Additional analysis is conducted to determine whether program had differing impact between geographic areas and DRG severity groups.

## Data Inputs
<b>CMS Public Use File (PUF) - Medicare Inpatient Hospitals by Provider and Service:</b> <br>
* <b>Input Files and API can be accessed and downloaded here:</b> <h>https://data.cms.gov/provider-summary-by-type-of-service/medicare-inpatient-hospitals/medicare-inpatient-hospitals-by-provider-and-service</h>
* <b>Data Dictionary:</b> <h>https://data.cms.gov/resources/medicare-inpatient-hospitals-by-provider-and-service-data-dictionary-0</h>

## Measure Definitions

* <b>Historical IP Performance:</b> Average year-over-year change in # of IP discharges between 2013 to 2016.
* <b>Treatment Period IP Performance:</b> Average year-over-year change in # of IP discharges between 2017 to 2018.
* <b>Change Produced by Program:</b> The impact of the program is evaluated as the difference between the year-over-year trend found in the historical period compared to the year-over-year trend produced after the program is in place.

The image below shows an example of how each measure would be calculated for a given hospital. The Change Produced by the Program for a given hospital would be evaluated as -13.8% - (-13.7%) = -0.1 percentage point difference. 

![Image](https://github.com/user-attachments/assets/367ff0e3-3db8-410f-99a1-98959dccf481)

## Examples of Ouputs
<b>I. IP Discharge Rates in New York Over Time</b><br>

![Image](https://github.com/user-attachments/assets/981c42d9-0229-4494-a241-83754c5920bf)


<b>II. IP Discharge Rates in New York by RUC Group</b><br>

![Image](https://github.com/user-attachments/assets/0bbf87ae-f996-4cef-9d0c-d74cc3fef3c9)


<b>III. IP Discharge Rates in New York by DRG Severity</b><br>

![Image](https://github.com/user-attachments/assets/307bfabb-f37d-42da-835a-e3710718ae03)
