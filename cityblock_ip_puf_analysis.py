#import python packages
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#--------------------------------------------------------------------------------------------------------------------------
#%%1. IMPORT PUF DATA
#--------------------------------------------------------------------------------------------------------------------------

#folder location to PUF data
folder_path = r"C:\Users\tcphan\OneDrive\Documents"
#name of PUF file
filename = "Medicare_IP_Hospitals_by_Provider_and_Service"
#list of years to import
years_lst = [2013, 2014, 2015, 2016, 2017, 2018]


puf_data = pd.DataFrame()
for year in years_lst:
    
    #read in PUF data
    data = pd.read_csv(os.path.join(folder_path, filename + "_" + str(year) + ".csv"))
    
    #standardize column names to be all in uppercase
    data.columns = [i.upper() for i in data.columns]

    #set the year that the PUF data is for
    data["YEAR"] = year

    #stack all yearly PUF data file into a single pandas dataframe
    puf_data = pd.concat([puf_data, data])


#filter to rows belonging to New York
ny_puf_data = puf_data[puf_data["RNDRNG_PRVDR_STATE_ABRVTN"] == "NY"]


#delete unncessary intermediate datasets or variables
del_vars_lst = ["year", "years_lst", "data", "puf_data"]
for i in del_vars_lst:
    try:
        exec("del {0}".format(i))
    except:
        pass


#--------------------------------------------------------------------------------------------------------------------------
#%%2. CALCULATE HIGH LEVEL SUMMARY OF PUF DATA
#--------------------------------------------------------------------------------------------------------------------------

#get count and mean of number of IP hospitals, discharges, and cost available in data
ny_puf_summ = ny_puf_data.groupby("YEAR").agg({"RNDRNG_PRVDR_ZIP5": "nunique",
                                               "RNDRNG_PRVDR_ORG_NAME": "nunique",
                                               "TOT_DSCHRGS": "sum",
                                               "AVG_TOT_PYMT_AMT": "mean"}).reset_index()

#--------------------------------------------------------------------------------------------------------------------------
#%%3. PLOT AVG INPATIENT DISCHARGES AND COST OVER TIME
#--------------------------------------------------------------------------------------------------------------------------

#summarize IP discharge and cost by year and CCN
ny_summ_by_ccn_yr = ny_puf_data.groupby(["YEAR", "RNDRNG_PRVDR_CCN"]).agg({"TOT_DSCHRGS": "sum",
                                                                           "AVG_TOT_PYMT_AMT": "mean"}).reset_index()

#calculate the average and standard deviation of IP discharges and cost by year
ny_summ_by_yr = ny_summ_by_ccn_yr.groupby(["YEAR"]).agg({"TOT_DSCHRGS": ["mean", "std"],
                                                         "AVG_TOT_PYMT_AMT": ["mean", "std"]}).reset_index()


outcome_yvars_lst = [(     'TOT_DSCHRGS', 'mean'), (     'AVG_TOT_PYMT_AMT', 'mean')]
outcome_stdvars_lst = [(     'TOT_DSCHRGS', 'std'), (     'AVG_TOT_PYMT_AMT', 'std')]
plot_titles_lst = ["Avg # of IP Discharges in NY Over Time", "Avg IP Cost in NY Over Time"]


for yvar, stdvar, titlevar in zip(outcome_yvars_lst, outcome_stdvars_lst, plot_titles_lst):
    
    #define the data columns to be shown on the x and y axis of the plot
    x_axis_vals = (            'YEAR',     '')
    y_axis_vals = yvar
    std_vals = stdvar
    
    #create time series plot showing number of IP discharges by year
    plt.plot(ny_summ_by_yr[x_axis_vals].values,
             ny_summ_by_yr[y_axis_vals].values,
             marker = "o")
    
    #add labels to each data point showing the value being plotted
    for i, txt in enumerate(ny_summ_by_yr[y_axis_vals].values):
        plt.text(ny_summ_by_yr[x_axis_vals].values[i],
                 ny_summ_by_yr[y_axis_vals].values[i] + 0.1 * ny_summ_by_yr[y_axis_vals].values[i],
                 f'{txt:,.1f}',
                 ha = "center",
                 fontsize = 8,
                 color = "black")
    
    #show the standard deviation of the data as bands around the line plot
    plt.fill_between(ny_summ_by_yr[x_axis_vals].values,
                     ny_summ_by_yr[y_axis_vals].values - ny_summ_by_yr[std_vals].values,
                     ny_summ_by_yr[y_axis_vals].values + ny_summ_by_yr[std_vals].values,
                     color = "blue",
                     alpha = 0.2)
    
    #define the start year when the program was implemented
    program_start_year = 2017
    #indicate the start year as a vertical line on the plot
    plt.axvline(x = program_start_year,
                color = "red",
                linestyle = '--',
                linewidth = 1)
    
    #apply formatting and labeling to plot
    plt.xticks(fontsize = 8)
    plt.yticks([])
    plt.title(titlevar, fontsize = 10, fontweight = "bold")
    
    #remove border lines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    
    plt.show()


#delete unncessary intermediate datasets or variables
del_vars_lst = ["ny_summ_by_ccn_yr",
                "ny_summ_by_yr",
                "outcome_stdvars_lst",
                "outcome_yvars_lst",
                "plot_titles_lst",
                "program_start_year",
                "spine",
                "std_vals",
                "stdvar",
                "titlevar",
                "txt",
                "x_axis_vals",
                "y_axis_vals",
                "yvar"]
for i in del_vars_lst:
    try:
        exec("del {0}".format(i))
    except:
        pass
    
#--------------------------------------------------------------------------------------------------------------------------
#%%4. PLOT CHANGE IN IP DISCHARGE AND COST RELATIVE TO HISTORICAL PERFORMANCE BY ZIP CODE
#--------------------------------------------------------------------------------------------------------------------------

#******************************
#4A. CALCULATE YEAR-OVER-YEAR CHANGE IN IP PERFORMANCE
#******************************

#summarize IP discharge and cost by year, CCN, and zip code
ny_summ_by_ccn_zip_yr = ny_puf_data.groupby(["YEAR",
                                             "RNDRNG_PRVDR_RUCA_DESC",
                                             "RNDRNG_PRVDR_ZIP5",
                                             "RNDRNG_PRVDR_CCN"]).agg({"TOT_DSCHRGS": "sum",
                                                                       "AVG_TOT_PYMT_AMT": "mean"}).reset_index()

#calculate the avg number of IP discharges and cost by zip code and year
ny_summ_by_zip_yr = ny_summ_by_ccn_zip_yr.groupby(["RNDRNG_PRVDR_RUCA_DESC", "RNDRNG_PRVDR_ZIP5", "YEAR"]).agg({"TOT_DSCHRGS": "mean",
                                                                                                                "AVG_TOT_PYMT_AMT": "mean"}).reset_index()

#get the prior year's discharge and cost amount for each zip code
ny_summ_by_zip_yr["TOT_DSCHRGS_LAG1"] = ny_summ_by_zip_yr.groupby(["RNDRNG_PRVDR_RUCA_DESC", "RNDRNG_PRVDR_ZIP5"])["TOT_DSCHRGS"].shift(1)
ny_summ_by_zip_yr["TOT_PYMT_AMT_LAG1"] = ny_summ_by_zip_yr.groupby(["RNDRNG_PRVDR_RUCA_DESC", "RNDRNG_PRVDR_ZIP5"])["AVG_TOT_PYMT_AMT"].shift(1)

#calculate the difference between the current year's and prior year's discharge and cost amount
ny_summ_by_zip_yr["DISCHRGS_YR_DIFF"] = (ny_summ_by_zip_yr["TOT_DSCHRGS"] - ny_summ_by_zip_yr["TOT_DSCHRGS_LAG1"]) / ny_summ_by_zip_yr["TOT_DSCHRGS_LAG1"]
ny_summ_by_zip_yr["PYMT_AMT_YR_DIFF"] = (ny_summ_by_zip_yr["AVG_TOT_PYMT_AMT"] - ny_summ_by_zip_yr["TOT_PYMT_AMT_LAG1"]) / ny_summ_by_zip_yr["TOT_PYMT_AMT_LAG1"]


#define the start year when the program was implemented
program_start_year = 2017
#create flag indicating if the year is during the program effective period
ny_summ_by_zip_yr["PROGRAM_IN_EFFECT_FLAG"] = np.where(ny_summ_by_zip_yr["YEAR"] >= program_start_year, 1, 0)

#calculate the average year-over-year change in discharge and cost amount for each zip code
yr_diff_summ_by_zip = ny_summ_by_zip_yr.groupby(["RNDRNG_PRVDR_RUCA_DESC",
                                                 "RNDRNG_PRVDR_ZIP5",
                                                 "PROGRAM_IN_EFFECT_FLAG"]).agg({"YEAR": "nunique",
                                                                                 "TOT_DSCHRGS": "mean",
                                                                                 "AVG_TOT_PYMT_AMT": "mean",
                                                                                 "DISCHRGS_YR_DIFF": "mean",
                                                                                 "PYMT_AMT_YR_DIFF": "mean"}).reset_index()

#filter to rows belonging to years when the program was in effect                                                                                 
summ_prog_in_eff = yr_diff_summ_by_zip[yr_diff_summ_by_zip["PROGRAM_IN_EFFECT_FLAG"] == 1]
summ_prog_in_eff = summ_prog_in_eff.rename(columns = {"TOT_DSCHRGS": "TOT_DSCHRGS_IN_EFF",
                                                      "AVG_TOT_PYMT_AMT": "TOT_PYMT_IN_EFF",
                                                      "DISCHRGS_YR_DIFF": "DISCHRGS_YR_DIFF_IN_EFF",
                                                      "PYMT_AMT_YR_DIFF": "PYMT_AMT_YR_DIFF_IN_EFF",
                                                      "YEAR": "NUM_YEARS_IN_EFF"}).drop(columns = ["PROGRAM_IN_EFFECT_FLAG"])

#filter to rows belonging to years when the program was NOT in effect
summ_prog_notin_eff = yr_diff_summ_by_zip[yr_diff_summ_by_zip["PROGRAM_IN_EFFECT_FLAG"] == 0]
summ_prog_notin_eff = summ_prog_notin_eff.rename(columns = {"TOT_DSCHRGS": "TOT_DSCHRGS_NOTIN_EFF",
                                                            "AVG_TOT_PYMT_AMT": "TOT_PYMT_NOTIN_EFF",
                                                            "DISCHRGS_YR_DIFF": "DISCHRGS_YR_DIFF_NOTIN_EFF",
                                                            "PYMT_AMT_YR_DIFF": "PYMT_AMT_YR_DIFF_NOTIN_EFF",
                                                            "YEAR": "NUM_YEARS_NOTIN_EFF"}).drop(columns = ["PROGRAM_IN_EFFECT_FLAG"])

#calculate the difference in the average year-over-year change in discharge and cost between when the program was in effect versus when it was not in effect
summ_prog_eff_all = pd.merge(summ_prog_in_eff,
                             summ_prog_notin_eff,
                             on = ["RNDRNG_PRVDR_RUCA_DESC", "RNDRNG_PRVDR_ZIP5"],
                             how = "inner")
summ_prog_eff_all["PROG_CHANGE_DISCHRGS"] = summ_prog_eff_all["DISCHRGS_YR_DIFF_IN_EFF"] - summ_prog_eff_all["DISCHRGS_YR_DIFF_NOTIN_EFF"]
summ_prog_eff_all["PROG_CHANGE_PYMT_AMT"] = summ_prog_eff_all["PYMT_AMT_YR_DIFF_IN_EFF"] - summ_prog_eff_all["PYMT_AMT_YR_DIFF_NOTIN_EFF"]



#******************************
#4B. PLOT YEAR-OVER-YEAR CHANGE BY ZIP CODE
#*****************************

outcome_xvars_lst = ["DISCHRGS_YR_DIFF_NOTIN_EFF", "PYMT_AMT_YR_DIFF_NOTIN_EFF"]
outcome_yvars_lst = ["PROG_CHANGE_DISCHRGS", "PROG_CHANGE_PYMT_AMT"]
plot_titles_lst = ["Change in IP Discharge Produced by Program Based on Zip Code",
                   "Change in IP Cost Produced by Program Based on Zip Code"]

for xvar, yvar, titlevar in zip(outcome_xvars_lst, outcome_yvars_lst, plot_titles_lst):
    
    #define the data columns to be shown on the x and y axis of the plot
    x_axis_vals = xvar
    y_axis_vals = yvar
    
    #convert each RUCA group to a categorical code
    summ_prog_eff_all["RUCA_CODE"] = pd.Categorical(summ_prog_eff_all["RNDRNG_PRVDR_RUCA_DESC"]).codes
    
    
    #create scatterplot showing historical IP performance relative to the change produced by the new program
    plt.scatter(summ_prog_eff_all[x_axis_vals].values * 100, 
                summ_prog_eff_all[y_axis_vals].values,
                c = summ_prog_eff_all["RUCA_CODE"],
                cmap = "tab10")
    
    #create legend
    unique_groups = summ_prog_eff_all["RNDRNG_PRVDR_RUCA_DESC"].unique()
    legend_patches = [plt.scatter([], [], color=plt.cm.tab10(i), label=group, s = 20) for i, group in enumerate(unique_groups)]
    plt.legend(title = "RUC Group",
               fontsize = 7,
               handles = legend_patches,
               loc = "upper center",
               bbox_to_anchor = (0.5, -0.2),
               frameon = False)
    
    #apply formatting and labeling to plot
    plt.xlabel("Historical IP Performance (%)", fontsize = 9)
    plt.ylabel("Change Produced by Program in Percentage Points", fontsize = 9)
    plt.title(titlevar,
              pad = 20,
              fontsize = 9,
              fontweight = "bold")
    
    #remove border lines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
        
    plt.show()
    

#delete unncessary intermediate datasets or variables
del_vars_lst = ["group",
                "legend_patches",
                "ny_summ_by_zip_yr",
                "ny_summ_by_ccn_zip_yr",
                "outcome_xvars_lst",
                "outcome_yvars_lst",
                "plot_titles_lst",
                "program_start_year",
                "summ_prog_eff_all",
                "summ_prog_in_eff",
                "summ_prog_notin_eff",
                "titlevar",
                "unique_groups",
                "x_axis_vals",
                "xvar",
                "y_axis_vals",
                "yr_diff_summ_by_zip",
                "yvar"]
for i in del_vars_lst:
    try:
        exec("del {0}".format(i))
    except:
        pass
    
#--------------------------------------------------------------------------------------------------------------------------
#%%5. PLOT CHANGE IN IP DISCHARGE AND COST RELATIVE TO HISTORICAL PERFORMANCE BY DRG
#--------------------------------------------------------------------------------------------------------------------------

#******************************
#5A. CALCULATE YEAR-OVER-YEAR CHANGE IN IP PERFORMANCE
#******************************

#summarize IP discharge and cost by year, CCN, and DRG
ny_summ_by_ccn_drg_yr = ny_puf_data.groupby(["DRG_CD",
                                             "RNDRNG_PRVDR_CCN",
                                             "YEAR"]).agg({"TOT_DSCHRGS": "sum",
                                                           "AVG_TOT_PYMT_AMT": "mean"}).reset_index()


#get the prior year's discharge and cost amount for each DRG
ny_summ_by_ccn_drg_yr["TOT_DSCHRGS_LAG1"] = ny_summ_by_ccn_drg_yr.groupby(["DRG_CD", "RNDRNG_PRVDR_CCN"])["TOT_DSCHRGS"].shift(1)
ny_summ_by_ccn_drg_yr["TOT_PYMT_AMT_LAG1"] = ny_summ_by_ccn_drg_yr.groupby(["DRG_CD", "RNDRNG_PRVDR_CCN"])["AVG_TOT_PYMT_AMT"].shift(1)

#calculate the difference between the current year's and prior year's discharge and cost amount
ny_summ_by_ccn_drg_yr["DISCHRGS_YR_DIFF"] = (ny_summ_by_ccn_drg_yr["TOT_DSCHRGS"] - ny_summ_by_ccn_drg_yr["TOT_DSCHRGS_LAG1"]) / ny_summ_by_ccn_drg_yr["TOT_DSCHRGS_LAG1"]
ny_summ_by_ccn_drg_yr["PYMT_AMT_YR_DIFF"] = (ny_summ_by_ccn_drg_yr["AVG_TOT_PYMT_AMT"] - ny_summ_by_ccn_drg_yr["TOT_PYMT_AMT_LAG1"]) / ny_summ_by_ccn_drg_yr["TOT_PYMT_AMT_LAG1"]


#define the start year when the program was implemented
program_start_year = 2017
#create flag indicating if the year is during the program effective period
ny_summ_by_ccn_drg_yr["PROGRAM_IN_EFFECT_FLAG"] = np.where(ny_summ_by_ccn_drg_yr["YEAR"] >= program_start_year, 1, 0)


#calculate the average year-over-year change in discharge and cost amount for each DRG
yr_diff_summ_by_drg = ny_summ_by_ccn_drg_yr.groupby(["DRG_CD",
                                                     "RNDRNG_PRVDR_CCN",
                                                     "PROGRAM_IN_EFFECT_FLAG"]).agg({"YEAR": "nunique",
                                                                                     "TOT_DSCHRGS": "mean",
                                                                                     "AVG_TOT_PYMT_AMT": "mean",
                                                                                     "DISCHRGS_YR_DIFF": "mean",
                                                                                     "PYMT_AMT_YR_DIFF": "mean"}).reset_index()

#filter to rows belonging to years when the program was in effect                                                                                 
summ_prog_in_eff = yr_diff_summ_by_drg[yr_diff_summ_by_drg["PROGRAM_IN_EFFECT_FLAG"] == 1]
summ_prog_in_eff = summ_prog_in_eff.rename(columns = {"TOT_DSCHRGS": "TOT_DSCHRGS_IN_EFF",
                                                      "AVG_TOT_PYMT_AMT": "TOT_PYMT_IN_EFF",
                                                      "DISCHRGS_YR_DIFF": "DISCHRGS_YR_DIFF_IN_EFF",
                                                      "PYMT_AMT_YR_DIFF": "PYMT_AMT_YR_DIFF_IN_EFF",
                                                      "YEAR": "NUM_YEARS_IN_EFF"}).drop(columns = ["PROGRAM_IN_EFFECT_FLAG"])

#filter to rows belonging to years when the program was NOT in effect
summ_prog_notin_eff = yr_diff_summ_by_drg[yr_diff_summ_by_drg["PROGRAM_IN_EFFECT_FLAG"] == 0]
summ_prog_notin_eff = summ_prog_notin_eff.rename(columns = {"TOT_DSCHRGS": "TOT_DSCHRGS_NOTIN_EFF",
                                                            "AVG_TOT_PYMT_AMT": "TOT_PYMT_NOTIN_EFF",
                                                            "DISCHRGS_YR_DIFF": "DISCHRGS_YR_DIFF_NOTIN_EFF",
                                                            "PYMT_AMT_YR_DIFF": "PYMT_AMT_YR_DIFF_NOTIN_EFF",
                                                            "YEAR": "NUM_YEARS_NOTIN_EFF"}).drop(columns = ["PROGRAM_IN_EFFECT_FLAG"])

#calculate the difference in the average year-over-year change in discharge and cost between when the program was in effect versus when it was not in effect
summ_prog_eff_all = pd.merge(summ_prog_in_eff,
                             summ_prog_notin_eff,
                             on = ["DRG_CD", "RNDRNG_PRVDR_CCN"],
                             how = "inner")
summ_prog_eff_all["PROG_CHANGE_DISCHRGS"] = summ_prog_eff_all["DISCHRGS_YR_DIFF_IN_EFF"] - summ_prog_eff_all["DISCHRGS_YR_DIFF_NOTIN_EFF"]


#******************************
#5B. PLOT YEAR-OVER-YEAR CHANGE BY DRG SEVERITY
#*****************************

#create cost buckets indicating the severity level of the DRG
#$0-$25,000: low-severity DRG
#$25,001 - $50,000: medium severity DRG
#> $50,000: high severity DRG
summ_prog_eff_all["HIST_COST_BUCKET"] = np.where(summ_prog_eff_all["TOT_PYMT_NOTIN_EFF"].between(0, 25000),
                                                 "Low Severity",
                                                  np.where(summ_prog_eff_all["TOT_PYMT_NOTIN_EFF"].between(25001, 50000),
                                                           "Medium Severity",
                                                           "High Severity"))


prog_eff_by_ccn_severity = summ_prog_eff_all.groupby(["RNDRNG_PRVDR_CCN",
                                                      "HIST_COST_BUCKET"]).agg({"PROG_CHANGE_DISCHRGS": "mean"}).reset_index()


#create boxplot showing the distribution of change in IP discharge for each DRG
sns.boxplot(x = "HIST_COST_BUCKET",
            y = "PROG_CHANGE_DISCHRGS",
            data = prog_eff_by_ccn_severity,
            flierprops = dict(marker = "o", markersize = 5),
            palette = "tab10")

#apply formatting and labeling to plot
plt.title("Change in IP Discharge Produced by Program Based on DRG Severity",
          pad = 10,
          fontsize = 9,
          fontweight = "bold")
plt.xlabel("")
plt.xticks(fontsize = 9)
plt.ylabel("Change Produced by Program in Percentage Points", fontsize = 9)
plt.show()


#delete unncessary intermediate datasets or variables
del_vars_lst = ["ny_summ_by_ccn_drg_yr",
                "outcome_xvars_lst",
                "outcome_yvars_lst",
                "plot_titles_lst",
                "program_start_year",
                "summ_prog_eff_all",
                "summ_prog_in_eff",
                "summ_prog_notin_eff",
                "titlevar",
                "x_axis_vals",
                "xvar",
                "y_axis_vals",
                "yvar",
                "yr_diff_summ_by_drg"]
for i in del_vars_lst:
    try:
        exec("del {0}".format(i))
    except:
        pass
    