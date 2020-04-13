
def utility_hwes_predict(data,numofforecast=1,loga=False,show_mdl_detail=False):
    """
    Holts Wİnter Exponential Smoothing Forecast model   
    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    numofforecast : TYPE, optional
        DESCRIPTION. The default is 1.
    loga : TYPE, optional
        DESCRIPTION. The default is False.
    show_mdl_detail : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    None.

    """    
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    from sklearn.metrics import mean_squared_error as mse
    from math import sqrt
    import time
    import pandas as pd
    import numpy as np
    from tqdm import tqdm
    from itertools import product
    import warnings

    if loga==True:
        datalog=data.apply(np.log1p)
    else:
        datalog=data
    datalog=datalog.reset_index(drop=True)
    
    def optimize_HWES(data_column,parameters_list):
            results = []
            best_aic = float('inf')
            #for param in tqdm(parameters_list):
            for param in parameters_list:
                try: 
                    import warnings
                    with warnings.catch_warnings():
                        warnings.filterwarnings("ignore") 
                        model=ExponentialSmoothing(data_column,trend=param[0],damped=param[1]).fit()
                except:
                    #print("model not built with params".format(param))
                    pass
                    continue
                aic = model.aic  
                #Save best model, AIC and parameters
                if aic < best_aic:
                    best_model = model
                    best_aic = aic
                    best_param = param
                results.append([param, model.aic])  
            result_table = pd.DataFrame(results)
            result_table.columns = ['parameters', 'aic']
            #Sort in ascending order, lower AIC is better
            result_table = result_table.sort_values(by='aic', ascending=True).reset_index(drop=True)
            
            return result_table

    #Set initial values and some bounds
    trend_p = ['mul'] #['mul','add']
    damped_p=[False]   #[False,True]

    
    #Create a list with all possible combinations of parameters
    parameters = product(trend_p,damped_p)
    parameters_list = list(parameters)
    len(parameters_list)
    result_table = optimize_HWES(datalog,parameters_list)
    
    #Set parameters that give the lowest AIC (Akaike Information Criteria)
    trend_p, damped_p= result_table.parameters[0]
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore") 
        model = ExponentialSmoothing(datalog,trend=trend_p,damped=damped_p)
        model_fit = model.fit()
        yhat = model_fit.forecast(numofforecast)
    
    if show_mdl_detail==True:
        print(model_fit.summary())
    
    if loga==True:
        yhat=np.exp(yhat)-1 #log1p

    yhat=yhat.reset_index(drop=True)
    yhat=yhat.rename("hwes_model")
    new_index=pd.Index(list(range(data[-1:].index.values[0]+1,data[-1:].index.values[0]+1+numofforecast)))
    yhat.index=new_index
    return yhat

def utility_sarimax_predict(series,nforecast=1,loga=False,plot_figures_flag=False,show_mdl_detail=False):
    """
     SARIMA Forecast model  (Seasonal Autoregressive Integrated Moving Average)

    Parameters
    ----------
    series : TYPE
        DESCRIPTION.
    nforecast : TYPE, optional
        DESCRIPTION. The default is 1.
    loga : TYPE, optional
        DESCRIPTION. The default is False.
    plot_figures_flag : TYPE, optional
        DESCRIPTION. The default is False.
    show_mdl_detail : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    from sklearn.metrics import r2_score, median_absolute_error, mean_absolute_error
    from sklearn.metrics import median_absolute_error, mean_squared_error, mean_squared_log_error
    from scipy.optimize import minimize
    import statsmodels.tsa.api as smt
    import statsmodels.api as sm
    import numpy as np
    import pandas as pd
    from tqdm import tqdm  
    from itertools import product
    import warnings
    
    np.random.seed(25)
    
    ## SARIMA
    def mean_absolute_percentage_error(y_true, y_pred):
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    warnings.filterwarnings('ignore')
    
    def optimize_SARIMA(data_column,parameters_list):
        """
            Return dataframe with parameters and corresponding AIC
            
            parameters_list - list with (ps,d, qs, Ps,D, Qs,s) tuples

        """       
        results = []
        best_aic = float('inf')   
        
        #for param in tqdm(parameters_list):
        for param in parameters_list:
            try: model = sm.tsa.statespace.SARIMAX(data_column, order=(param[0], param[1],param[2]),
                                                    seasonal_order=(param[3], param[4], param[5], param[5])).fit(disp=-1)
            # try: model = sm.tsa.statespace.SARIMAX(data_column, order=(param[0], d, param[1])).fit(disp=-1)
            except:
                #print("model not built with params".format(param))
                pass
                continue                
            aic = model.aic           
            #Save best model, AIC and parameters
            if aic < best_aic:
                best_model = model
                best_aic = aic
                best_param = param
            results.append([param, model.aic])         
        result_table = pd.DataFrame(results)
        result_table.columns = ['parameters', 'aic']
        #Sort in ascending order, lower AIC is better
        result_table = result_table.sort_values(by='aic', ascending=True).reset_index(drop=True)      
        return result_table
    
    #Set initial values and some bounds
    ps = range(0, 3)
    d = range(0,1)
    qs = range(0, 3)
    Ps = range(0, 3)
    D = range(0,1)
    Qs = range(0, 3)
    s = [3,5,7]
    #Create a list with all possible combinations of parameters
    parameters = product(ps,d, qs, Ps,D, Qs,s)
    parameters_list = list(parameters)
    len(parameters_list)
    if loga==True:
        series=series.apply(np.log1p)
    series_diff=series
    result_table = optimize_SARIMA(series_diff,parameters_list)
       
    #Set parameters that give the lowest AIC (Akaike Information Criteria) 
    p, d, q, P, D, Q,s = result_table.parameters[0]   
    best_model = sm.tsa.statespace.SARIMAX(series_diff, order=(p, d, q),seasonal_order=(P, D, Q, s)).fit(disp=-1)
    if show_mdl_detail==True:
       print(best_model.summary())
       if plot_figures_flag==True:
           best_model.plot_diagnostics(figsize=(15, 12))    
    #Forecast on n_steps forward
    forecast = best_model.forecast(nforecast)
    if loga==True:
        forecast=np.exp(forecast)-1 #log1p
    forecast=pd.Series(forecast.values,name='sarimax_model')
    lenn=series[:].shape[0]
    new_index=pd.Index(list(range(series[-1:].index.values[0]+1,series[-1:].index.values[0]+1+nforecast)))
    forecast.index=new_index
    return forecast