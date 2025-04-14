import pandas as pd
from collections import Counter
from pathlib import Path

# Define o diretório base do projeto (auto-detecção)
BASE_DIR = Path(__file__).resolve().parent.parent

# Define o caminho do arquivo de entrada
INPUT_FILE = BASE_DIR / "data/DataSample.xlsx"

def calculate_time_statistics(file_path):
    # Carrega o arquivo Excel
    xls = pd.ExcelFile(file_path)
    
    # Verifica se a planilha existe
    if 'APULastStart' not in xls.sheet_names:
        print("Sheet 'APULastStart' not found in the Excel file.")
        return
    
    df = xls.parse('APULastStart')
    
    # Verifica se as colunas necessárias existem
    if 'StartUTC' not in df.columns or 'EndUTC' not in df.columns:
        print("Columns 'StartUTC' or 'EndUTC' not found in the sheet.")
        return
    
    # Converte colunas para datetime
    df['StartUTC'] = pd.to_datetime(df['StartUTC'], errors='coerce')
    df['EndUTC'] = pd.to_datetime(df['EndUTC'], errors='coerce')
    
    # Remove valores inválidos
    df = df.dropna(subset=['StartUTC', 'EndUTC'])
    
    # Calcula o tempo decorrido em segundos
    df['ElapsedSeconds'] = (df['EndUTC'] - df['StartUTC']).dt.total_seconds()
    
    # Remove valores negativos (caso existam erros nos dados)
    df = df[df['ElapsedSeconds'] >= 0]
    
    if df.empty:
        print("No valid elapsed time data available.")
        return
    
    # Calcula estatísticas
    avg_time = df['ElapsedSeconds'].mean()
    mode_time = df['ElapsedSeconds'].mode().iloc[0] if not df['ElapsedSeconds'].mode().empty else None
    min_time = df['ElapsedSeconds'].min()
    max_time = df['ElapsedSeconds'].max()
    
    # Exibe os resultados
    print(f"Média do tempo decorrido: {avg_time:.2f} segundos")
    print(f"Moda do tempo decorrido: {mode_time:.2f} segundos")
    print(f"Menor tempo decorrido: {min_time:.2f} segundos")
    print(f"Maior tempo decorrido: {max_time:.2f} segundos")

# Exemplo de uso
calculate_time_statistics(INPUT_FILE)