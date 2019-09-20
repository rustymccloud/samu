from fish_predict import *
get_ipython().run_line_magic('matplotlib', 'inline')
IFrame('https://caltopo.com/m/SEN5', width=700, height=350)
fish = pd.read_csv('fish_capture.csv')
fish.head(7)
fish['CAPTURE_CODE'].hist()
samp = np.random.rand(len(fish)) < 0.7
x_fish = fish.iloc[:,2:]
y_train, x_train = fish['CAPTURE_CODE'][samp], x_fish[samp]
y_test, x_test = fish['CAPTURE_CODE'][~samp], x_fish[~samp]
rfc = RandomForestClassifier(100).fit(x_train,y_train)
y_predict,y_predict_proba = rfc.predict(x_test),rfc.predict_proba(x_test)
print('ROC AUC Score: >>>>> '+str(round(roc_auc_score(y_test,y_predict_proba[:,1]),2)*100)+'% <<<<< | '+'There is a '+str(round(roc_auc_score(y_test,y_predict_proba[:,1]),2)*100)+"% chance this model's prediction will correctly distinguish between captured and non-capture fish")
feature_importances = pd.DataFrame(rfc.feature_importances_,index = x_train.columns,columns=['importance']).sort_values('importance',ascending=False)
feature_importances.plot(kind='bar',title='Most Important Features in Predicting Fish Survival')
fish[fish['SS_FLAG']==1]['CAPTURE_CODE'].hist()
fish[fish['SS_FLAG']!=1]['CAPTURE_CODE'].hist(alpha=0.5)