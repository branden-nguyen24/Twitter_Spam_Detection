# import libraries
import pandas as pd
# import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
# from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
# from sklearn.preprocessing import label_binarize

# ROC Curve for the classification models
# from sklearn.metrics import roc_auc_score, roc_curve, auc
# import matplotlib.cm as cm
import matplotlib.pyplot as plt

# Importing the required modelling libraries
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import accuracy_score, f1_score
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
# from statistics import mean


class ModelsTraining:
    """
    Train data with 7 models:
        # 1. Naïve Bayesian
        # 2. Decision tree classifier (any variation will do) k-NN
        # 3. k-NN
        # 4. Random Forest
        # 5. Logistic regression
        # 6. AdaBoost
        # 7. SVM (Support Vector Machine)

    Input: dataframe, target class name
    """

    def __init__(self, X=None, y=None, df=None, class_name=None, drop_cols=None):
        self.df = df
        self.accuracy_ls = dict()
        self.f1_score_ls = dict()
        self.model_ls = dict()
        self.y_pred_ls = dict()
        self.X, self.y = self.__init_X_y(X, y, df, class_name, drop_cols)
        self.X_test, self.X_train, self.y_test, self.y_train = self.split_data()
        self.train_model()
        # results of df containing accuracy and f1
        self.df_result = self.accuracy_f1()

    def __init_X_y(self, X, y, df, class_name, drop_cols):
        if df is not None:
            drop_cols = self.__get_drop_cols(drop_cols, class_name)
            X = df.drop(columns=(drop_cols))
            y = df[class_name]
        return X, y


    def __get_drop_cols(self, drop_cols, class_name):
        res = list(drop_cols)
        res.append(class_name)
        return res

    def split_data(self):
        # Split data: training set: 80%, testing set: 20%
        X = self.X
        y = self.y
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=0
        )

        # Feature scaling
        sc = StandardScaler()
        print("=" * 100)
        print("Transforming and Standardizing data...")
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)

        return X_test, X_train, y_test, y_train

    def models(self):
        # return a list of ml models

        # 1. Naïve Bayesian
        nb = GaussianNB()
        # 2. Decision tree classifier (any variation will do)
        dtc = DecisionTreeClassifier()
        # 3. k-NN
        knn = KNeighborsClassifier(n_neighbors=3)
        # 4. Random Forest
        # might need to tune parameters
        rfc = RandomForestClassifier(n_estimators=200)
        # 5. Logistic regression
        logistic = LogisticRegression(C = 0.5, max_iter = 500)
        # 6. AdaBoost
        adaboost = AdaBoostClassifier(n_estimators=100, random_state=0)
        # 7. SVC (Support Vector Machine)
        # SVC is time comsuming
        svc = SVC(kernel = 'rbf', max_iter = 1000, probability = True)

        ml_models = {
            "Naive Bayesian": nb,
            "Decision Tree Classifier": dtc,
            "KNeighbors Classifier": knn,
            "Random Forest Classifier": rfc,
            'Logistic Regression': logistic,
            "AdaBoost Classifier": adaboost,
            # 'SVC': svc
        }

        return ml_models

    def train_model(self):
        X_test = self.X_test
        X_train = self.X_train
        y_test = self.y_test
        y_train = self.y_train
        ml_models = self.models()
        total_model = len(ml_models)
        num_folds = 2  # just for now
        # num_folds = 10
        # ten-fold except Random Forest Classifier
        print("=" * 100)
        print(f"Training {total_model} models...")
        for i, model in enumerate(ml_models.keys()):
            print(f"{i+1}. {model}")
        print("=" * 100)
        print(f"{num_folds}-fold Cross Validation")
        print("=" * 100)
        print("\n")

        for i, (name, clf) in enumerate(ml_models.items()):
            self.print_title(f"{i + 1}/{total_model} {name}")
            print("Training model...\n")
            # Train model
            classifier = clf
            model = classifier.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            self.model_ls[name] = model
            self.y_pred_ls[name] = y_pred

            # # K-fold Cross Validation
            # if name != "Random Forest Classifier":
            #     # cross validation k fold
            #     accuracy_scores = cross_val_score(
            #         clf, X_train, y_train, cv=num_folds, scoring="accuracy"
            #     )
            #     f1_scores = cross_val_score(
            #         clf, X_train, y_train, cv=num_folds, scoring="f1"
            #     )
            #     print("accuracy_scores:\n", accuracy_scores)
            #     print("f1_scores:\n", f1_scores)
            #     # mean accuracy and f1-score
            #     accuracy_mean = np.mean(accuracy_scores)
            #     f1_score_mean = np.mean(f1_scores)
            #     print(f"The mean accuracy: {accuracy_mean:.3f}")
            #     print(f"The mean f1 score: {f1_score_mean:.3f}")

            # # Random Forest, no k-fold cv needed
            # else:
            #     accuracy_mean = accuracy_score(y_test, y_pred)
            #     f1_score_mean = f1_score(y_test, y_pred, average="binary")
            #     print(f"The accuracy: {accuracy_mean:.3f}")
            #     print(f"The f1 score: {f1_score_mean:.3f}")
            accuracy_mean = accuracy_score(y_test, y_pred)
            f1_score_mean = f1_score(y_test, y_pred, average="binary")
            print(f"The accuracy: {accuracy_mean:.3f}")
            print(f"The f1 score: {f1_score_mean:.3f}")
            self.accuracy_ls[name] = accuracy_mean
            self.f1_score_ls[name] = f1_score_mean
            # print(str(classifier))

            print("\n")
            print(classification_report(y_pred, y_test))
            print("=" * 100)
            print("\n")

    def confusion_matrix_visualization(self):
        X_test = self.X_test
        y_test = self.y_test
        for name, clf in self.model_ls.items():
            #     print ("The Confusion Matrix of: ", name)
            #     print (pd.DataFrame(confusion_matrix(y_test, y_pred)))
            plt.figure(figsize=(5, 5))
            disp = plot_confusion_matrix(
                clf, X_test, y_test, cmap=plt.cm.Blues, normalize="true"
            )
            disp.ax_.set_title("The Confusion Matrix of: %s" % name)
            plt.show()

    def accuracy_f1(self):
        # Comparison
        results = {
            "ML Models": [name for name in self.model_ls.keys()],
            "Accuracy": [a for a in self.accuracy_ls.values()],
            "F1-score": [f1 for f1 in self.f1_score_ls.values()],
        }

        df_results = pd.DataFrame(data=results)

        # df_results.style.background_gradient(cmap='Blues')
        return df_results


    def print_title(self, title):
        # print break line with title
        # ============== title =============
        total_len = 100
        decoration = "=" * ((total_len - len(title) - 1) // 2)
        print(decoration + " " + title + " " + decoration)
