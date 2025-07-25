import mlflow
import mlflow.sklearn
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


mlflow.set_tracking_uri('http://127.0.0.1:5000')

#mlflow.get_tracking_uri()

wine=load_wine()
x=wine.data
y=wine.target


x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.10,random_state=42)

max_depth=5
n_estimators=10

mlflow.set_experiment('MLOPS_MLFLOW')

with mlflow.start_run():#experiment_id=''
    rf=RandomForestClassifier(max_depth=max_depth,n_estimators=n_estimators,random_state=42)
    rf.fit(x_train,y_train)

    y_pred=rf.predict(x_test)
    accuracy=accuracy_score(y_test,y_pred)

    mlflow.log_metric('Accuracy',accuracy)
    mlflow.log_param('max_depth',max_depth)
    mlflow.log_param('n_estimators',n_estimators)

    cm=confusion_matrix(y_test,y_pred)
    plt.figure(figsize=(6,6))
    sns.heatmap(cm,annot=True,fmt='d',cmap='Blues',xticklabels=wine.target_names,yticklabels=wine.target_names)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title('Confusion Matrix')

    plt.savefig('ConfusionMatrix.png')

    mlflow.log_artifact('ConfusionMatrix.png')
    mlflow.log_artifact(__file__)

    mlflow.set_tags({'Author':'Ridesh','Project':'Wine Classification'})

    mlflow.sklearn.log_model(rf,'RandoForestClassifier')

    print(accuracy)