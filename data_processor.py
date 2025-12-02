import pandas as pd
import numpy as np

def load_data(file_path):
    """
    Loads and processes data from the Excel file.
    Returns a cleaned DataFrame ready for the dashboard.
    """
    try:
        # Get all sheet names
        xl = pd.ExcelFile(file_path)
        
        # Define sheets to process
        cad_sheets = [
            ('CAD 3 2023', 'CAD 3'),
            ('CAD 3 2024', 'CAD 3'),
            ('CAD 3 2025', 'CAD 3'),
            ('CAD 1 2024-2025', 'CAD 1')
        ]
        
        all_data = []
        
        for sheet_name, cad_name in cad_sheets:
            if sheet_name not in xl.sheet_names:
                continue
                
            # Load raw data - Header is at row 1 (0-indexed)
            df_raw = pd.read_excel(file_path, sheet_name=sheet_name, header=1)
            
            # --- Process Daily Data ---
            # Columns 0-6: Tempo, Energia, Pot Inv, Pot kWp, Energia esp, FC, Energia Esp Anual
            df_daily = df_raw.iloc[:, [0, 1, 2, 3, 4, 5]].copy()
            df_daily.columns = ['Tempo', 'Energia_kWh', 'Pot_Inv_kW', 'Pot_kWp', 'Energia_Especifica_kWh_kWp', 'FC']
            
            # Drop rows where 'Tempo' is not a valid datetime
            df_daily = df_daily[pd.to_datetime(df_daily['Tempo'], errors='coerce').notna()]
            df_daily['Tempo'] = pd.to_datetime(df_daily['Tempo'])
            
            # Add auxiliary time columns
            df_daily['Ano'] = df_daily['Tempo'].dt.year
            df_daily['Mes'] = df_daily['Tempo'].dt.month
            df_daily['Mes_Nome'] = df_daily['Tempo'].dt.strftime('%B')
            
            # --- Process Monthly Data ---
            # Columns 8-17: Month, Mean Energy, Sum Energy, Spec Energy, PR, FC, City, Irrad
            df_monthly = df_raw.iloc[:, [8, 9, 10, 11, 12, 13, 17]].copy()
            df_monthly.columns = ['Mes_Ref', 'Media_Energia_Mensal', 'Soma_Energia_Mensal', 
                                 'Energia_Esp_Mensal', 'PR_Mensal', 'FC_Mensal', 'Irradiacao_Mensal']
            
            # Clean monthly data
            df_monthly = df_monthly.dropna(subset=['Mes_Ref'])
            
            # Create a mapping dictionary for months
            month_map = {
                'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4, 'Maio': 5, 'Junho': 6,
                'Julho': 7, 'Agosto': 8, 'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
            }
            df_monthly['Mes_Num'] = df_monthly['Mes_Ref'].map(month_map)
            
            # Merge monthly data into daily data
            df_merged = pd.merge(df_daily, df_monthly, left_on='Mes', right_on='Mes_Num', how='left')
            
            # Add CAD identifier
            df_merged['CAD'] = cad_name
            
            all_data.append(df_merged)
        
        # Combine all data
        if all_data:
            df_final = pd.concat(all_data, ignore_index=True)
            # Sort by date
            df_final = df_final.sort_values('Tempo').reset_index(drop=True)
            return df_final
        else:
            return pd.DataFrame()

    except Exception as e:
        print(f"Error processing data: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()


if __name__ == "__main__":
    # Test the function
    df = load_data('Monitoramento (1).xlsx')
    print("Columns:", df.columns)
    print("Head:", df.head())
    print("Shape:", df.shape)
