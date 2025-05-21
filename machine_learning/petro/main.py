'''Fernando de Souza Teixeira'''

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import os


def load_data():
    """Loads and validates raw data from CSV file"""
    try:
        return pd.read_csv("Bovespa.csv")
    except FileNotFoundError:
        print(f"Error: File 'Bovespa.csv' not found in:\n{os.getcwd()}")
        exit()

def process_data(raw_df):
    """Processes and transforms raw data for analysis"""
    # Filter for Petrobras stocks
    petro_df = raw_df.query("Ticker in ['PETR3', 'PETR4']").copy()
    if petro_df.empty:
        print("No Petrobras data found!")
        exit()
    
    # Data cleaning
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    petro_df[numeric_cols] = petro_df[numeric_cols].replace(',','.', regex=True).astype(float)
    petro_df['Date'] = pd.to_datetime(petro_df['Date'], dayfirst=True)
    
    # Feature engineering
    return create_technical_indicators(petro_df)

def create_technical_indicators(df):
    """Creates technical indicators for analysis"""
    return df.groupby('Ticker', group_keys=False).apply(
        lambda x: x.assign(
            sma_5 = x['Close'].rolling(5).mean(),
            sma_20 = x['Close'].rolling(20).mean(),
            volatility_5 = x['Close'].rolling(5).std(),
            daily_return = x['Close'].pct_change()
        ).dropna()
    )

def split_data(df):
    """Performs temporal split of the data"""
    def _split(group):
        split_idx = int(len(group) * 0.8)
        return group.iloc[:split_idx], group.iloc[split_idx:]
    
    train_parts = []
    test_parts = []
    for ticker in ['PETR3', 'PETR4']:
        train, test = _split(df[df['Ticker'] == ticker])
        train_parts.append(train)
        test_parts.append(test)
    
    return (
        pd.concat(train_parts).sort_values('Date'),
        pd.concat(test_parts).sort_values('Date')
    )

def prepare_features(train_df, test_df):
    """Prepares feature matrices and target vectors"""
    features = ['Open', 'High', 'Low', 'Volume', 
                'sma_5', 'sma_20', 'volatility_5', 'daily_return']
    target = 'Close'
    
    return (
        train_df[features],
        train_df[target],
        test_df[features],
        test_df[target]
    )

def train_models(X_train, y_train):
    """Trains machine learning models"""
    return {
        'Decision Tree': DecisionTreeRegressor(random_state=42).fit(X_train, y_train),
        'Linear Regression': LinearRegression().fit(X_train, y_train)
    }

def evaluate_models(models, X_test, y_test):
    """Evaluates models and returns predictions"""
    predictions = {}


    print("\n ** Model Evaluation Results **")
    
    for name, model in models.items():
        preds = model.predict(X_test)
        predictions[name] = preds
        print_metrics(y_test, preds, name)
    return predictions

def print_metrics(y_true, y_pred, model_name):
    """Displays formatted evaluation metrics"""
    print(f"\n╔══════════════════════════════╗")
    print(f"║ {model_name:^28} ║")
    print(f"╠══════════════════╦═══════════╣")
    print(f"║ R²               ║ {r2_score(y_true, y_pred):>9.4f} ║")
    print(f"║ RMSE             ║ {np.sqrt(mean_squared_error(y_true, y_pred)):>9.4f} ║")
    print(f"╚══════════════════╩═══════════╝")

def plot_results(y_test, predictions):
    """Generates and saves comparison plots"""
    plt.figure(figsize=(15, 6))
    for idx, (model_name, preds) in enumerate(predictions.items(), 1):
        plt.subplot(1, 2, idx)
        plt.plot(y_test.values, label='Actual', alpha=0.7)
        plt.plot(preds, '--', label='Predicted')
        plt.title(f'{model_name} Performance')
        plt.xlabel('Time Period (days)')
        plt.ylabel('Closing Price (R$)')
        plt.legend()
    
    save_results()

def save_results():
    """Saves predictions to CSV files"""

    path = f"result-genered/model_comparison.png"

    os.makedirs('result-genered', exist_ok=True)
    plt.tight_layout()
    plt.savefig(path)
    print(f"\nSaved in path: {path}")

if __name__ == "__main__" :
    raw_data = load_data()
    processed_data = process_data(raw_data)
    train_set, test_set = split_data(processed_data)
    X_train, y_train, X_test, y_test = prepare_features(train_set, test_set)
    models = train_models(X_train, y_train)
    predictions = evaluate_models(models, X_test, y_test)
    plot_results(y_test, predictions)
