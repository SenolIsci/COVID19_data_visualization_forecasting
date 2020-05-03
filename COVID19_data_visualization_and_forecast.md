```python
# %load COVID19_data_visualization_and_forecast.py
"""
Created on Fri Apr  3 17:48:45 2020

@author: User
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sb
import matplotlib 
import sys
import  chart_story_parameters as cspp
import algo as algo
%matplotlib inline  
```


```python
def load_and_prep_data(file_address,verbose=False):
    """
    

    Parameters
    ----------
    file_address : TYPE
        DESCRIPTION.
    verbose : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """

    df_org = pd.read_csv(file_address)
    df_org.head()
    df=df_org[['dateRep','cases','deaths','countryterritoryCode','countriesAndTerritories','popData2018','continentExp']].copy()
   
    #insert record for world counts
    world_pop=df[['countriesAndTerritories','popData2018']].drop_duplicates()['popData2018'].sum()
    table = pd.pivot_table(df[['dateRep','cases','deaths','countriesAndTerritories']], index=['dateRep', 'countriesAndTerritories']).copy()    
    table=table.sort_index(ascending=False)
    record_world=table.groupby(by='dateRep',level=0,axis=0).sum()
    record_world=record_world.reset_index()
    record_world=record_world.sort_index(ascending=False)
    record_world=record_world.reset_index(drop=True)
    record_world['popData2018']=world_pop
    record_world['countryterritoryCode']='WORLD'
    record_world['countriesAndTerritories']='WORLD'
    record_world['continentExp']='WORLD'
    record_world = record_world[['dateRep', 'cases', 'deaths', 'countryterritoryCode','countriesAndTerritories', 'popData2018','continentExp']]
    
    df=df.append(record_world,ignore_index=True)
    df['dateRep']= pd.to_datetime(df['dateRep']) 
    df=df.set_index('dateRep')
    return df
    

def gen_country_stats(df,cnt_code,covidcase_type,day_thr,mawindow):
    """
    

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    cnt_code : TYPE
        DESCRIPTION.
    covidcase_type : TYPE
        DESCRIPTION.
    day_thr : TYPE
        DESCRIPTION.
    mawindow : TYPE
        DESCRIPTION.

    Returns
    -------
    cntAdf : TYPE
        DESCRIPTION.
    country_name : TYPE
        DESCRIPTION.

    """
    cntAdf=df[df.countryterritoryCode==cnt_code].copy()
    cntAdf=cntAdf.sort_index()
    cntAdf.columns = ['cases.'+cnt_code,'deaths.'+cnt_code,'countryterritoryCode.'+cnt_code,'countriesAndTerritories.'+cnt_code,'popData2018.'+cnt_code,'continentExp'+cnt_code]
    cntAdf['total_cases.'+cnt_code]=cntAdf['cases.'+cnt_code].cumsum()
    cntAdf['total_deaths.'+cnt_code]=cntAdf['deaths.'+cnt_code].cumsum()
    cntAdf['ratio_of_total_deaths_to_total_cases.'+cnt_code]=cntAdf['total_deaths.'+cnt_code]/cntAdf['total_cases.'+cnt_code]
    cntAdf['cases(MovAvg).'+cnt_code]=cntAdf['cases.'+cnt_code].rolling(mawindow).mean()
    cntAdf['deaths(MovAvg).'+cnt_code]=cntAdf['deaths.'+cnt_code].rolling(mawindow).mean()
    cntAdf['cases(MovAvg)perPop1M.'+cnt_code]=cntAdf['cases(MovAvg).'+cnt_code]*1e6/cntAdf['popData2018.'+cnt_code]
    cntAdf['deaths(MovAvg)perPop1M.'+cnt_code]=cntAdf['deaths(MovAvg).'+cnt_code]*1e6/cntAdf['popData2018.'+cnt_code]
    cntAdf['total_casesperPop1M.'+cnt_code]=cntAdf['total_cases.'+cnt_code]*1e6/cntAdf['popData2018.'+cnt_code]
    cntAdf['total_deathsperPop1M.'+cnt_code]=cntAdf['total_deaths.'+cnt_code]*1e6/cntAdf['popData2018.'+cnt_code]
    cntAdf['casesperPop1M.'+cnt_code]=cntAdf['cases.'+cnt_code]*1e6/cntAdf['popData2018.'+cnt_code]
    cntAdf['deathsperPop1M.'+cnt_code]=cntAdf['deaths.'+cnt_code]*1e6/cntAdf['popData2018.'+cnt_code]
    cntAdf=cntAdf.dropna()
    #cntAdf['cases(MovAvg).'+cnt_code]=np.log1p(cntAdf['cases(MovAvg).'+cnt_code])
    cntAdf=cntAdf[cntAdf[covidcase_type+cnt_code]>day_thr].reset_index()
    country_name=cntAdf['countriesAndTerritories.'+cnt_code][0]
    return cntAdf,country_name
```


```python
def RUNcoviddatastory(selected_story_name,PubDate,country_list,day_thr,mawindow,fdays,loga=False,forecast_flag=False,forecast_mdl_list=['hwes'],plot_figures_flag=False,save_figures_flag=True,verbose=False,show_mdl_detail=False): 
    """
    

    Parameters
    ----------
    selected_story_name : TYPE
        DESCRIPTION.
    PubDate : TYPE
        DESCRIPTION.
    country_list : TYPE
        DESCRIPTION.
    day_thr : TYPE
        DESCRIPTION.
    mawindow : TYPE
        DESCRIPTION.
    fdays : TYPE
        DESCRIPTION.
    loga : TYPE, optional
        DESCRIPTION. The default is False.
    forecast_flag : TYPE, optional
        DESCRIPTION. The default is False.
    forecast_mdl_list : TYPE, optional
        DESCRIPTION. The default is ['hwes'].
    plot_figures_flag : TYPE, optional
        DESCRIPTION. The default is False.
    save_figures_flag : TYPE, optional
        DESCRIPTION. The default is True.
    verbose : TYPE, optional
        DESCRIPTION. The default is False.
    show_mdl_detail : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    new_dict : TYPE
        DESCRIPTION.

    """
    np.set_printoptions(precision=2)
    np.random.seed(25)
    cspp.set_plt_conf(plt)
    sb.set_style('whitegrid')
    file_address='./data/'+'COVID-19-geographic-disbtribution-worldwide-'+PubDate+'.csv'
    
    Chart_Story_df=cspp.gen_chart_story_params_dict(forecast_flag,mawindow, fdays,day_thr)
    selected_story=Chart_Story_df[selected_story_name]  
    df=load_and_prep_data(file_address,verbose)

    covidcase_type=selected_story['covidcase_type']
    FIGylabel_text=selected_story['FIGylabel_text']
    FIGxlabel_text=selected_story['FIGxlabel_text']
    Chart_title=selected_story['Chart_title']
    INFOtext=selected_story['INFOtext'] 
    yvalformat=selected_story['FIGyvalformat']
    new_dict={}
    pred_dic={}
    fig, ax = plt.subplots(figsize=(8, 8))
    for cntA in country_list:
        dfc=df[(df.countryterritoryCode==cntA)]
        dfc=df.sort_index()
        cntAdf,country=gen_country_stats(dfc,cntA,covidcase_type,day_thr,mawindow)
        new_dict[cntA]=cntAdf
    for cntA,mdl_name in zip(country_list,forecast_mdl_list):
        df_s=new_dict[cntA]
        markers_on=df_s.shape[0]*[False]
        markers_on[-1]=True #last point in the series
        predictor_column=covidcase_type+cntA
        forecast_mdl=mdl_name
        if forecast_flag==True:
            if forecast_mdl=='hwes':
                forecast_res=algo.utility_hwes_predict(df_s[predictor_column].dropna(),fdays,loga,show_mdl_detail=show_mdl_detail)
            elif forecast_mdl=='sarimax':
                forecast_res=algo.utility_sarimax_predict(df_s[predictor_column].dropna(),fdays,loga,plot_figures_flag=plot_figures_flag,show_mdl_detail=show_mdl_detail)
            forecast_res=forecast_res.astype(int)
                #datetime index
            startdate=pd.to_datetime(PubDate).date()
            enddate=startdate+pd.Timedelta(forecast_res.shape[0]-1,unit='D')
            forecast_with_date=forecast_res.copy()
            didx = pd.date_range(start=startdate,end=enddate,freq ='D')
            forecast_with_date.index=didx
            if verbose==True:
                print(cntA)
                print(selected_story_name)
                print(forecast_with_date)
        country_nameA=df_s['countriesAndTerritories.'+cntA][0]
        ax.plot(df_s.index,df_s[predictor_column],label=''+country_nameA,markersize=15,marker='.',markevery=markers_on)
        if forecast_flag==True:
            ax.plot(forecast_res.index,forecast_res,label='_nolegend_',ls='--',color=plt.gca().lines[-1].get_color())
    #ax.set_yscale('log')        
    ax.legend(loc='upper left')
    ax.set_ylabel(FIGylabel_text,fontsize=cspp.BIGGER_SIZE)
    ax.set_xlabel(FIGxlabel_text,fontsize=cspp.BIGGER_SIZE)
    ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:,'+yvalformat+'}'))
    ax.annotate(INFOtext, (0,0), (0, -55), xycoords='axes fraction', textcoords='offset points', va='top',fontsize=10,fontstyle='italic',color='gray') 
    ax.set_title("COVID-19 "+Chart_title+" by Country\n"+' '+'as of '+PubDate+' 6:00-10:00 CET' ,fontsize=cspp.BIGGER_SIZE)
    fig.tight_layout()
    if save_figures_flag==True:
        figtitletosave='./figures/' + selected_story_name + '.png'      
        if verbose==True:
            #print("\nsaving figures to the local figures folder:\n"+figtitletosave+"\n")
            pass
        fig.savefig(figtitletosave,dpi=300)
 
    new_df=pd.DataFrame() 
    for cntA in country_list:
        s=new_dict[cntA]
        predictor_column=covidcase_type+cntA
        s=s[predictor_column]
        new_df=pd.concat((new_df,s),axis=1)

    return new_dict

```


```python
# Country selection codes:
       #  'AFG', 'ALB', 'AND', 'DZA', 'AGO', nan, 'ATG', 'ARG', 'ARM', 'ABW',
       # 'AUS', 'AUT', 'AZE', 'BHS', 'BHR', 'BGD', 'BRB', 'BLR', 'BEL',
       # 'BLZ', 'BEN', 'BMU', 'BTN', 'BOL', 'BIH', 'BWA', 'BRA', 'VGB',
       # 'BRN', 'BGR', 'BFA', 'BDI', 'KHM', 'CMR', 'CAN', 'CPV', 'CYM',
       # 'CAF', 'TCD', 'CHL', 'CHN', 'COL', 'COG', 'CRI', 'CIV', 'HRV',
       # 'CUB', 'CUW', 'CYP', 'CZE', 'COD', 'DNK', 'DJI', 'DMA', 'DOM',
       # 'ECU', 'EGY', 'SLV', 'GNQ', 'ERI', 'EST', 'SWZ', 'ETH', 'FRO',
       # 'FJI', 'FIN', 'FRA', 'PYF', 'GAB', 'GMB', 'GEO', 'DEU', 'GHA',
       # 'GIB', 'GRC', 'GRL', 'GRD', 'GUM', 'GTM', 'GGY', 'GIN', 'GNB',
       # 'GUY', 'HTI', 'VAT', 'HND', 'HUN', 'ISL', 'IND', 'IDN', 'IRN',
       # 'IRQ', 'IRL', 'IMN', 'ISR', 'ITA', 'JAM', 'JPN', 'JEY', 'JOR',
       # 'KAZ', 'KEN', 'XKX', 'KWT', 'KGZ', 'LAO', 'LVA', 'LBN', 'LBR',
       # 'LBY', 'LIE', 'LTU', 'LUX', 'MDG', 'MWI', 'MYS', 'MDV', 'MLI',
       # 'MLT', 'MRT', 'MUS', 'MEX', 'MDA', 'MCO', 'MNG', 'MNE', 'MSR',
       # 'MAR', 'MOZ', 'MMR', 'NAM', 'NPL', 'NLD', 'NCL', 'NZL', 'NIC',
       # 'NER', 'NGA', 'MKD', 'MNP', 'NOR', 'OMN', 'PAK', 'PSE', 'PAN',
       # 'PNG', 'PRY', 'PER', 'PHL', 'POL', 'PRT', 'PRI', 'QAT', 'ROU',
       # 'RUS', 'RWA', 'KNA', 'LCA', 'VCT', 'SMR', 'SAU', 'SEN', 'SRB',
       # 'SYC', 'SLE', 'SGP', 'SXM', 'SVK', 'SVN', 'SOM', 'ZAF', 'KOR',
       # 'ESP', 'LKA', 'SDN', 'SUR', 'SWE', 'CHE', 'SYR', 'TWN', 'THA',
       # 'TLS', 'TGO', 'TTO', 'TUN', 'TUR', 'TCA', 'UGA', 'UKR', 'ARE',
       # 'GBR', 'TZA', 'USA', 'VIR', 'URY', 'UZB', 'VEN', 'VNM', 'ZMB',
       # 'ZWE','WORLD'    
# Country selection codes:
       #  'AFG', 'ALB', 'AND', 'DZA', 'AGO', nan, 'ATG', 'ARG', 'ARM', 'ABW',
       # 'AUS', 'AUT', 'AZE', 'BHS', 'BHR', 'BGD', 'BRB', 'BLR', 'BEL',
       # 'BLZ', 'BEN', 'BMU', 'BTN', 'BOL', 'BIH', 'BWA', 'BRA', 'VGB',
       # 'BRN', 'BGR', 'BFA', 'BDI', 'KHM', 'CMR', 'CAN', 'CPV', 'CYM',
       # 'CAF', 'TCD', 'CHL', 'CHN', 'COL', 'COG', 'CRI', 'CIV', 'HRV',
       # 'CUB', 'CUW', 'CYP', 'CZE', 'COD', 'DNK', 'DJI', 'DMA', 'DOM',
       # 'ECU', 'EGY', 'SLV', 'GNQ', 'ERI', 'EST', 'SWZ', 'ETH', 'FRO',
       # 'FJI', 'FIN', 'FRA', 'PYF', 'GAB', 'GMB', 'GEO', 'DEU', 'GHA',
       # 'GIB', 'GRC', 'GRL', 'GRD', 'GUM', 'GTM', 'GGY', 'GIN', 'GNB',
       # 'GUY', 'HTI', 'VAT', 'HND', 'HUN', 'ISL', 'IND', 'IDN', 'IRN',
       # 'IRQ', 'IRL', 'IMN', 'ISR', 'ITA', 'JAM', 'JPN', 'JEY', 'JOR',
       # 'KAZ', 'KEN', 'XKX', 'KWT', 'KGZ', 'LAO', 'LVA', 'LBN', 'LBR',
       # 'LBY', 'LIE', 'LTU', 'LUX', 'MDG', 'MWI', 'MYS', 'MDV', 'MLI',
       # 'MLT', 'MRT', 'MUS', 'MEX', 'MDA', 'MCO', 'MNG', 'MNE', 'MSR',
       # 'MAR', 'MOZ', 'MMR', 'NAM', 'NPL', 'NLD', 'NCL', 'NZL', 'NIC',
       # 'NER', 'NGA', 'MKD', 'MNP', 'NOR', 'OMN', 'PAK', 'PSE', 'PAN',
       # 'PNG', 'PRY', 'PER', 'PHL', 'POL', 'PRT', 'PRI', 'QAT', 'ROU',
       # 'RUS', 'RWA', 'KNA', 'LCA', 'VCT', 'SMR', 'SAU', 'SEN', 'SRB',
       # 'SYC', 'SLE', 'SGP', 'SXM', 'SVK', 'SVN', 'SOM', 'ZAF', 'KOR',
       # 'ESP', 'LKA', 'SDN', 'SUR', 'SWE', 'CHE', 'SYR', 'TWN', 'THA',
       # 'TLS', 'TGO', 'TTO', 'TUN', 'TUR', 'TCA', 'UGA', 'UKR', 'ARE',
       # 'GBR', 'TZA', 'USA', 'VIR', 'URY', 'UZB', 'VEN', 'VNM', 'ZMB',
       # 'ZWE','WORLD'    
      
# chart story selection list:
        # 'Total_cases'
        # 'Total_deaths'
        # 'Daily_cases'
        # 'Daily_deaths'
        # 'Daily_cases_MovAvg'
        # 'Daily_deaths_MovAvg'
        # 'Daily_cases_MovAvg_perPopulation'
        # 'Daily_deaths_MovAvg_perPopulation'
        #'Total_cases_perPopulation'
        #'Total_deaths_perPopulation'
        #'Daily_cases_perPopulation'
        #'Daily_deaths_perPopulation'
        #'Ratio_of_total_deaths_to_total_cases'
PubDate='2020-05-03' # pubdate of the data file by European Centre for Disease Prevention and Control
# original data link: https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide
forecast_flag=True  
forecast_mdl=['hwes','hwes','sarimax','hwes'] #options are ['hwes','sarimax']
loga=False #take log of data
plot_figures_flag=True
save_figures_flag=True
verbose=True
show_mdl_detail=False
mawindow=3 #moving average window size for smoothing charts
fdays=3 # number of steps forecasts (forward  time points) 
case_thr=10 # the day threshold that the first N cases recorded
deat_thr=3 # the day threshold that the first N deaths recorded
caseperpop_thr=0
deatperpop_thr=0
country_list=['ITA','DEU','GBR','USA']
 
```


```python
new_dict1=RUNcoviddatastory('Total_cases',PubDate,country_list,case_thr,mawindow,fdays,loga,forecast_flag,forecast_mdl,plot_figures_flag,save_figures_flag,verbose,show_mdl_detail)        
```

    ITA
    Total_cases
    2020-05-03    211245
    2020-05-04    213180
    2020-05-05    215133
    Freq: D, Name: hwes_model, dtype: int32
    DEU
    Total_cases
    2020-05-03    163671
    2020-05-04    164855
    2020-05-05    166048
    Freq: D, Name: hwes_model, dtype: int32
    GBR
    Total_cases
    2020-05-03    185769
    2020-05-04    188632
    2020-05-05    190221
    Freq: D, Name: sarimax_model, dtype: int32
    USA
    Total_cases
    2020-05-03    1165411
    2020-05-04    1198279
    2020-05-05    1232074
    Freq: D, Name: hwes_model, dtype: int32
    


![png](output_4_1.png)



```python
new_dict2=RUNcoviddatastory('Total_deaths',PubDate,country_list,deat_thr,mawindow,fdays,loga,forecast_flag,forecast_mdl,plot_figures_flag,save_figures_flag,verbose,show_mdl_detail)        

```

    ITA
    Total_deaths
    2020-05-03    29131
    2020-05-04    29577
    2020-05-05    30030
    Freq: D, Name: hwes_model, dtype: int32
    DEU
    Total_deaths
    2020-05-03    6782
    2020-05-04    6918
    2020-05-05    7057
    Freq: D, Name: hwes_model, dtype: int32
    GBR
    Total_deaths
    2020-05-03    28708
    2020-05-04    29270
    2020-05-05    29803
    Freq: D, Name: sarimax_model, dtype: int32
    USA
    Total_deaths
    2020-05-03    68228
    2020-05-04    70029
    2020-05-05    71877
    Freq: D, Name: hwes_model, dtype: int32
    


![png](output_5_1.png)



```python
new_dict3=RUNcoviddatastory('Ratio_of_total_deaths_to_total_cases',PubDate,country_list,caseperpop_thr,mawindow,fdays,loga,False,forecast_mdl,plot_figures_flag,save_figures_flag,verbose,show_mdl_detail)        
```


![png](output_6_0.png)



```python
new_dict4=RUNcoviddatastory('Total_cases_perPopulation',PubDate,country_list,caseperpop_thr,mawindow,fdays,loga,forecast_flag,forecast_mdl,plot_figures_flag,save_figures_flag,verbose,show_mdl_detail)        

```

    ITA
    Total_cases_perPopulation
    2020-05-03    3495
    2020-05-04    3527
    2020-05-05    3559
    Freq: D, Name: hwes_model, dtype: int32
    DEU
    Total_cases_perPopulation
    2020-05-03    1973
    2020-05-04    1987
    2020-05-05    2001
    Freq: D, Name: hwes_model, dtype: int32
    GBR
    Total_cases_perPopulation
    2020-05-03    2816
    2020-05-04    2890
    2020-05-05    2962
    Freq: D, Name: sarimax_model, dtype: int32
    USA
    Total_cases_perPopulation
    2020-05-03    3562
    2020-05-04    3662
    2020-05-05    3765
    Freq: D, Name: hwes_model, dtype: int32
    


![png](output_7_1.png)



```python
new_dict5=RUNcoviddatastory('Total_deaths_perPopulation',PubDate,country_list,deatperpop_thr,mawindow,fdays,loga,forecast_flag,forecast_mdl,plot_figures_flag,save_figures_flag,verbose,show_mdl_detail)        

```

    ITA
    Total_deaths_perPopulation
    2020-05-03    481
    2020-05-04    489
    2020-05-05    496
    Freq: D, Name: hwes_model, dtype: int32
    DEU
    Total_deaths_perPopulation
    2020-05-03    81
    2020-05-04    83
    2020-05-05    85
    Freq: D, Name: hwes_model, dtype: int32
    GBR
    Total_deaths_perPopulation
    2020-05-03    432
    2020-05-04    440
    2020-05-05    449
    Freq: D, Name: sarimax_model, dtype: int32
    USA
    Total_deaths_perPopulation
    2020-05-03    208
    2020-05-04    214
    2020-05-05    219
    Freq: D, Name: hwes_model, dtype: int32
    


![png](output_8_1.png)



```python
new_dict6=RUNcoviddatastory('Daily_cases',PubDate,country_list,case_thr,mawindow,fdays,loga,forecast_flag,forecast_mdl,plot_figures_flag,save_figures_flag,verbose,show_mdl_detail)        

```

    ITA
    Daily_cases
    2020-05-03    1853
    2020-05-04    1811
    2020-05-05    1769
    Freq: D, Name: hwes_model, dtype: int32
    DEU
    Daily_cases
    2020-05-03    1296
    2020-05-04    1253
    2020-05-05    1211
    Freq: D, Name: hwes_model, dtype: int32
    GBR
    Daily_cases
    2020-05-03    5235
    2020-05-04    5092
    2020-05-05    4897
    Freq: D, Name: sarimax_model, dtype: int32
    USA
    Daily_cases
    2020-05-03    30900
    2020-05-04    31484
    2020-05-05    32079
    Freq: D, Name: hwes_model, dtype: int32
    


![png](output_9_1.png)



```python
new_dict7=RUNcoviddatastory('Daily_deaths',PubDate,country_list,deat_thr,mawindow,fdays,loga,forecast_flag,forecast_mdl,plot_figures_flag,save_figures_flag,verbose,show_mdl_detail)        

```

    ITA
    Daily_deaths
    2020-05-03    356
    2020-05-04    372
    2020-05-05    390
    Freq: D, Name: hwes_model, dtype: int32
    DEU
    Daily_deaths
    2020-05-03    91
    2020-05-04    87
    2020-05-05    82
    Freq: D, Name: hwes_model, dtype: int32
    GBR
    Daily_deaths
    2020-05-03    650
    2020-05-04    600
    2020-05-05    661
    Freq: D, Name: sarimax_model, dtype: int32
    USA
    Daily_deaths
    2020-05-03    1831
    2020-05-04    1836
    2020-05-05    1842
    Freq: D, Name: hwes_model, dtype: int32
    


![png](output_10_1.png)



```python
new_dict8=RUNcoviddatastory('Daily_cases_perPopulation',PubDate,country_list,caseperpop_thr,mawindow,fdays,loga,forecast_flag,forecast_mdl,plot_figures_flag,save_figures_flag,verbose,show_mdl_detail)        

```

    ITA
    Daily_cases_perPopulation
    2020-05-03    30
    2020-05-04    29
    2020-05-05    29
    Freq: D, Name: hwes_model, dtype: int32
    DEU
    Daily_cases_perPopulation
    2020-05-03    17
    2020-05-04    16
    2020-05-05    16
    Freq: D, Name: hwes_model, dtype: int32
    GBR
    Daily_cases_perPopulation
    2020-05-03    76
    2020-05-04    73
    2020-05-05    72
    Freq: D, Name: sarimax_model, dtype: int32
    USA
    Daily_cases_perPopulation
    2020-05-03    94
    2020-05-04    95
    2020-05-05    96
    Freq: D, Name: hwes_model, dtype: int32
    


![png](output_11_1.png)



```python
new_dict9=RUNcoviddatastory('Daily_deaths_perPopulation',PubDate,country_list,deatperpop_thr,mawindow,fdays,loga,forecast_flag,forecast_mdl,plot_figures_flag,save_figures_flag,verbose,show_mdl_detail)        

```

    ITA
    Daily_deaths_perPopulation
    2020-05-03    5
    2020-05-04    6
    2020-05-05    6
    Freq: D, Name: hwes_model, dtype: int32
    DEU
    Daily_deaths_perPopulation
    2020-05-03    1
    2020-05-04    1
    2020-05-05    1
    Freq: D, Name: hwes_model, dtype: int32
    GBR
    Daily_deaths_perPopulation
    2020-05-03     9
    2020-05-04     9
    2020-05-05    10
    Freq: D, Name: sarimax_model, dtype: int32
    USA
    Daily_deaths_perPopulation
    2020-05-03    5
    2020-05-04    5
    2020-05-05    5
    Freq: D, Name: hwes_model, dtype: int32
    


![png](output_12_1.png)



```python
new_dict10=RUNcoviddatastory('Daily_cases_MovAvg',PubDate,country_list,case_thr,mawindow,fdays,loga,forecast_flag,forecast_mdl,plot_figures_flag,save_figures_flag,verbose,show_mdl_detail)        

```

    ITA
    Daily_cases_MovAvg
    2020-05-03    1852
    2020-05-04    1794
    2020-05-05    1737
    Freq: D, Name: hwes_model, dtype: int32
    DEU
    Daily_cases_MovAvg
    2020-05-03    1109
    2020-05-04    1092
    2020-05-05    1076
    Freq: D, Name: hwes_model, dtype: int32
    GBR
    Daily_cases_MovAvg
    2020-05-03    5621
    2020-05-04    5448
    2020-05-05    5379
    Freq: D, Name: sarimax_model, dtype: int32
    USA
    Daily_cases_MovAvg
    2020-05-03    32129
    2020-05-04    33231
    2020-05-05    34370
    Freq: D, Name: hwes_model, dtype: int32
    


![png](output_13_1.png)



```python
new_dict11=RUNcoviddatastory('Daily_deaths_MovAvg',PubDate,country_list,deat_thr,mawindow,fdays,loga,forecast_flag,forecast_mdl,plot_figures_flag,save_figures_flag,verbose,show_mdl_detail)        

```

    ITA
    Daily_deaths_MovAvg
    2020-05-03    358
    2020-05-04    374
    2020-05-05    390
    Freq: D, Name: hwes_model, dtype: int32
    DEU
    Daily_deaths_MovAvg
    2020-05-03    119
    2020-05-04    117
    2020-05-05    116
    Freq: D, Name: hwes_model, dtype: int32
    GBR
    Daily_deaths_MovAvg
    2020-05-03    716
    2020-05-04    699
    2020-05-05    655
    Freq: D, Name: sarimax_model, dtype: int32
    USA
    Daily_deaths_MovAvg
    2020-05-03    1797
    2020-05-04    1788
    2020-05-05    1779
    Freq: D, Name: hwes_model, dtype: int32
    


![png](output_14_1.png)



```python
new_dict12=RUNcoviddatastory('Daily_cases_MovAvg_perPopulation',PubDate,country_list,caseperpop_thr,mawindow,fdays,loga,forecast_flag,forecast_mdl,plot_figures_flag,save_figures_flag,verbose,show_mdl_detail)        

```

    ITA
    Daily_cases_MovAvg_perPopulation
    2020-05-03    30
    2020-05-04    29
    2020-05-05    28
    Freq: D, Name: hwes_model, dtype: int32
    DEU
    Daily_cases_MovAvg_perPopulation
    2020-05-03    13
    2020-05-04    13
    2020-05-05    13
    Freq: D, Name: hwes_model, dtype: int32
    GBR
    Daily_cases_MovAvg_perPopulation
    2020-05-03    84
    2020-05-04    82
    2020-05-05    81
    Freq: D, Name: sarimax_model, dtype: int32
    USA
    Daily_cases_MovAvg_perPopulation
    2020-05-03    95
    2020-05-04    96
    2020-05-05    98
    Freq: D, Name: hwes_model, dtype: int32
    


![png](output_15_1.png)



```python
new_dict13=RUNcoviddatastory('Daily_deaths_MovAvg_perPopulation',PubDate,country_list,deatperpop_thr,mawindow,fdays,loga,forecast_flag,forecast_mdl,plot_figures_flag,save_figures_flag,verbose,show_mdl_detail)        
```

    ITA
    Daily_deaths_MovAvg_perPopulation
    2020-05-03    5
    2020-05-04    6
    2020-05-05    6
    Freq: D, Name: hwes_model, dtype: int32
    DEU
    Daily_deaths_MovAvg_perPopulation
    2020-05-03    1
    2020-05-04    1
    2020-05-05    1
    Freq: D, Name: hwes_model, dtype: int32
    GBR
    Daily_deaths_MovAvg_perPopulation
    2020-05-03    9
    2020-05-04    9
    2020-05-05    9
    Freq: D, Name: sarimax_model, dtype: int32
    USA
    Daily_deaths_MovAvg_perPopulation
    2020-05-03    5
    2020-05-04    5
    2020-05-05    5
    Freq: D, Name: hwes_model, dtype: int32
    


![png](output_16_1.png)



```python

```
