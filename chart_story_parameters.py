# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 15:51:13 2020

@author: User
"""

SMALL_SIZE = 12
MEDIUM_SIZE = 15
BIGGER_SIZE = 20
BIGGEST_SIZE=25

def set_plt_conf(plt):
    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=BIGGEST_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGEST_SIZE)  # fontsize of the figure title
    plt.rc('lines',linewidth=3)

def gen_chart_story_params_dict(forecast_flag,mawindow,fdays,day_thr):
    import pandas as pd
    
    INFOdata_origin='\nData: EDCD - European Centre for Disease Prevention and Control. Reports at 6:00-10:00 CET'
    INFOcontact='\nGraphics: generated using code: https://github.com/SenolIsci/COVID19_data_visualization_forecasting.git '
    #INFOcontact=''
    INFOnote2='\nDashed lines are '+str(fdays)+' day forecasts calculated using Time-Series Forecasting model'
   
    story_params=['covidcase_type','FIGylabel_text','FIGxlabel_text','Chart_title','INFOtext','FIGyvalformat']
    
    S1=pd.Series(index=story_params)
    S1.covidcase_type='total_cases.'
    S1.FIGylabel_text="Total cases"
    S1.FIGxlabel_text="Number of days"
    S1.Chart_title=" Total Cases"
    INFOnote1='\nNumber of days are of the days since '+ str(day_thr)+ ' total cases first recorded'
    S1.INFOtext=INFOdata_origin+INFOcontact+INFOnote1+INFOnote2 if forecast_flag==True else INFOdata_origin+INFOcontact+INFOnote1
    S1.FIGyvalformat='.0f'
    
    S2=pd.Series(index=story_params)
    S2.covidcase_type='total_deaths.'
    S2.FIGylabel_text="Total deaths"
    S2.FIGxlabel_text="Number of days"
    S2.Chart_title="Total Deaths"
    INFOnote1='\nNumber of days are of the days since '+ str(day_thr)+ ' total deaths first recorded'
    S2.INFOtext=INFOdata_origin+INFOcontact+INFOnote1+INFOnote2 if forecast_flag==True else INFOdata_origin+INFOcontact+INFOnote1
    S2.FIGyvalformat='.0f'
    
    S3=pd.Series(index=story_params)
    S3.covidcase_type='cases.'
    S3.FIGylabel_text="Daily cases"
    S3.FIGxlabel_text="Number of days"
    S3.Chart_title="Daily Cases"
    INFOnote1='\nNumber of days are of the days since '+ str(day_thr)+ ' daily cases first recorded'
    S3.INFOtext=INFOdata_origin+INFOcontact+INFOnote1+INFOnote2 if forecast_flag==True else INFOdata_origin+INFOcontact+INFOnote1
    S3.FIGyvalformat='.0f'
    
    S4=pd.Series(index=story_params)
    S4.covidcase_type='deaths.'
    S4.FIGylabel_text='Daily deaths'
    S4.FIGxlabel_text="Number of days"
    S4.Chart_title="Daily Deaths"
    INFOnote1='\nNumber of days are of the days since '+ str(day_thr)+ ' daily deaths first recorded'
    S4.INFOtext=INFOdata_origin+INFOcontact+INFOnote1+INFOnote2 if forecast_flag==True else INFOdata_origin+INFOcontact+INFOnote1
    S4.FIGyvalformat='.0f'
    
    S5=pd.Series(index=story_params)
    S5.covidcase_type='cases(MovAvg).'
    S5.FIGylabel_text="Daily cases ("+str(mawindow)+"-day moving average)"
    S5.FIGxlabel_text="Number of days"
    S5.Chart_title="Daily Cases"
    INFOnote1='\nNumber of days are of the days since '+ str(day_thr)+ ' daily cases (smoothed) first recorded'
    S5.INFOtext=INFOdata_origin+INFOcontact+INFOnote1+INFOnote2 if forecast_flag==True else INFOdata_origin+INFOcontact+INFOnote1
    S5.FIGyvalformat='.0f'
    
    S6=pd.Series(index=story_params)
    S6.covidcase_type='deaths(MovAvg).'
    S6.FIGylabel_text="Daily deaths ("+str(mawindow)+"-day moving average)"
    S6.FIGxlabel_text="Number of days"
    S6.Chart_title="Daily Deaths"
    INFOnote1='\nNumber of days are of the days since '+ str(day_thr)+ ' death cases (smoothed) first recorded'
    S6.INFOtext=INFOdata_origin+INFOcontact+INFOnote1+INFOnote2 if forecast_flag==True else INFOdata_origin+INFOcontact+INFOnote1
    S6.FIGyvalformat='.0f'
    
    S7=pd.Series(index=story_params)
    S7.covidcase_type='cases(MovAvg)perPop1M.'
    S7.FIGylabel_text="Daily cases ("+str(mawindow)+"-day moving average)\n per 1 Million of Country population"
    S7.FIGxlabel_text="Number of days"
    S7.Chart_title="Daily Cases (scaled)"
    INFOnote1='\nNumber of days are of the days since '+ str(day_thr)+ ' daily cases (smoothed) first recorded'
    S7.INFOtext=INFOdata_origin+INFOcontact+INFOnote1+INFOnote2 if forecast_flag==True else INFOdata_origin+INFOcontact+INFOnote1
    S7.FIGyvalformat='.0f'
    
    S8=pd.Series(index=story_params)
    S8.covidcase_type='deaths(MovAvg)perPop1M.'
    S8.FIGylabel_text="Daily deaths ("+str(mawindow)+"-day moving average)\n per 1 Million of Country population"
    S8.FIGxlabel_text="Number of days"
    S8.Chart_title="Daily Deaths (scaled)"
    INFOnote1='\nNumber of days are of the days since '+ str(day_thr)+ ' daily deaths (smoothed) first recorded'
    S8.INFOtext=INFOdata_origin+INFOcontact+INFOnote1+INFOnote2 if forecast_flag==True else INFOdata_origin+INFOcontact+INFOnote1
    S8.FIGyvalformat='.0f'
    
    S9=pd.Series(index=story_params)
    S9.covidcase_type='total_casesperPop1M.'
    S9.FIGylabel_text="Total cases\n per 1 Million of Country population"
    S9.FIGxlabel_text="Number of days"
    S9.Chart_title=" Total Cases (scaled)"
    INFOnote1='\nNumber of days are of the days since '+ str(day_thr)+ ' total cases first recorded\n per 1 Million of Country population'
    S9.INFOtext=INFOdata_origin+INFOcontact+INFOnote1+INFOnote2 if forecast_flag==True else INFOdata_origin+INFOcontact
    S9.FIGyvalformat='.0f'
    
    S10=pd.Series(index=story_params)
    S10.covidcase_type='total_deathsperPop1M.'
    S10.FIGylabel_text="Total deaths\n per 1 Million of Country population"
    S10.FIGxlabel_text="Number of days"
    S10.Chart_title="Total Deaths (scaled)"
    INFOnote1='\nNumber of days are of the days since '+ str(day_thr)+ ' total deaths first recorded\n per 1 Million of Country population'
    S10.INFOtext=INFOdata_origin+INFOcontact+INFOnote1+INFOnote2 if forecast_flag==True else INFOdata_origin+INFOcontact
    S10.FIGyvalformat='.0f'
    
    S11=pd.Series(index=story_params)
    S11.covidcase_type='casesperPop1M.'
    S11.FIGylabel_text="Daily cases\n per 1 Million of Country population"
    S11.FIGxlabel_text="Number of days"
    S11.Chart_title="Daily Cases (scaled)"
    INFOnote1='\nNumber of days are of the days since '+ str(day_thr)+ ' daily cases first recorded\n per 1 Million of Country population'
    S11.INFOtext=INFOdata_origin+INFOcontact+INFOnote1+INFOnote2 if forecast_flag==True else INFOdata_origin+INFOcontact
    S11.FIGyvalformat='.0f'
    
    S12=pd.Series(index=story_params)
    S12.covidcase_type='deathsperPop1M.'
    S12.FIGylabel_text='Daily deaths\n per 1 Million of Country population'
    S12.FIGxlabel_text="Number of days"
    S12.Chart_title="Daily Deaths (scaled)"
    INFOnote1='\nNumber of days are of the days since '+ str(day_thr)+ ' daily deaths first recorded\n per 1 Million of Country population'
    S12.INFOtext=INFOdata_origin+INFOcontact+INFOnote1+INFOnote2 if forecast_flag==True else INFOdata_origin+INFOcontact
    S12.FIGyvalformat='.0f'
    
    S13=pd.Series(index=story_params)
    S13.covidcase_type='ratio_of_total_deaths_to_total_cases.'
    S13.FIGylabel_text="Ratio of total deaths to total cases"
    S13.FIGxlabel_text="Number of days"
    S13.Chart_title=" Ratio of Total Deaths to Total Cases"
    INFOnote1='\nNumber of days are of the days since '+ str(day_thr)+ ' total cases first recorded'
    S13.INFOtext=INFOdata_origin+INFOcontact+INFOnote1+INFOnote2 if forecast_flag==True else INFOdata_origin+INFOcontact+INFOnote1
    S13.FIGyvalformat='.2f'
    
    
    Chart_Story_df=pd.DataFrame({
    'Total_cases':S1,
    'Total_deaths':S2,
    'Daily_cases':S3,
    'Daily_deaths':S4,
    'Daily_cases_MovAvg':S5,
    'Daily_deaths_MovAvg':S6,
    'Daily_cases_MovAvg_perPopulation':S7,
    'Daily_deaths_MovAvg_perPopulation':S8,
    'Total_cases_perPopulation':S9,
    'Total_deaths_perPopulation':S10,
    'Daily_cases_perPopulation':S11,
    'Daily_deaths_perPopulation':S12,
    'Ratio_of_total_deaths_to_total_cases':S13
    })
    
    return Chart_Story_df