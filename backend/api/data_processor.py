import pandas as pd
import os
from typing import Dict, List, Any, Optional
from django.conf import settings


class DataProcessor:
    """Handles Excel data processing and analysis"""
    
    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize the data processor
        
        Args:
            file_path: Path to Excel file. If None, uses default data file.
        """
        self.file_path = file_path
        self.df = None
        
    def load_data(self) -> bool:
        """
        Load data from Excel file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.file_path and os.path.exists(self.file_path):
                self.df = pd.read_excel(self.file_path)
            else:
                # Try to load from default location
                default_path = os.path.join(settings.BASE_DIR, 'data', 'real_estate_data.xlsx')
                if os.path.exists(default_path):
                    self.df = pd.read_excel(default_path)
                else:
                    return False
            
            # Clean column names (remove extra spaces, standardize)
            self.df.columns = self.df.columns.str.strip()
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def get_available_areas(self) -> List[str]:
        """
        Get list of all available areas in the dataset
        
        Returns:
            List of area names
        """
        if self.df is None:
            return []
        
        # Common column names for area
        area_columns = ['final location', 'Area', 'area', 'Location', 'location', 'Locality', 'locality']
        for col in area_columns:
            if col in self.df.columns:
                areas = self.df[col].dropna().unique().tolist()
                return sorted([str(area) for area in areas])
        return []
    
    def filter_by_area(self, area: str) -> pd.DataFrame:
        """
        Filter data by area name
        
        Args:
            area: Area name to filter by
            
        Returns:
            Filtered DataFrame
        """
        if self.df is None:
            return pd.DataFrame()
        
        # Find the area column
        area_columns = ['final location', 'Area', 'area', 'Location', 'location', 'Locality', 'locality']
        area_col = None
        for col in area_columns:
            if col in self.df.columns:
                area_col = col
                break
        
        if area_col is None:
            return pd.DataFrame()
        
        # Case-insensitive filtering
        filtered_df = self.df[self.df[area_col].astype(str).str.lower() == area.lower()]
        return filtered_df
    
    def filter_by_areas(self, areas: List[str]) -> pd.DataFrame:
        """
        Filter data by multiple areas
        
        Args:
            areas: List of area names to filter by
            
        Returns:
            Filtered DataFrame
        """
        if self.df is None:
            return pd.DataFrame()
        
        # Find the area column
        area_columns = ['final location', 'Area', 'area', 'Location', 'location', 'Locality', 'locality']
        area_col = None
        for col in area_columns:
            if col in self.df.columns:
                area_col = col
                break
        
        if area_col is None:
            return pd.DataFrame()
        
        # Case-insensitive filtering for multiple areas
        areas_lower = [a.lower() for a in areas]
        filtered_df = self.df[self.df[area_col].astype(str).str.lower().isin(areas_lower)]
        return filtered_df
    
    def get_price_trend(self, area: str) -> Dict[str, Any]:
        """
        Get price trend data for an area
        
        Args:
            area: Area name
            
        Returns:
            Dictionary with labels and data for charting
        """
        filtered_df = self.filter_by_area(area)
        
        if filtered_df.empty:
            return {'labels': [], 'data': []}
        
        # Find year and price columns
        year_col = self._find_column(['year', 'Year', 'Date', 'date'])
        price_col = self._find_column([
            'flat - weighted average rate', 
            'office - weighted average rate',
            'others - weighted average rate',
            'shop - weighted average rate',
            'Price', 'price', 'Average Price', 'avg_price', 'AvgPrice'
        ])
        
        if year_col is None or price_col is None:
            return {'labels': [], 'data': []}
        
        # Group by year and calculate average price
        trend_data = filtered_df.groupby(year_col)[price_col].mean().sort_index()
        
        return {
            'labels': [str(year) for year in trend_data.index.tolist()],
            'data': trend_data.values.tolist()
        }
    
    def get_demand_trend(self, area: str) -> Dict[str, Any]:
        """
        Get demand trend data for an area
        
        Args:
            area: Area name
            
        Returns:
            Dictionary with labels and data for charting
        """
        filtered_df = self.filter_by_area(area)
        
        if filtered_df.empty:
            return {'labels': [], 'data': []}
        
        # Find year and demand columns
        year_col = self._find_column(['year', 'Year', 'Date', 'date'])
        demand_col = self._find_column([
            'total_sales - igr',
            'total sold - igr',
            'flat_sold - igr',
            'total units',
            'Demand', 'demand', 'Sales', 'sales', 'Transactions', 'transactions'
        ])
        
        if year_col is None or demand_col is None:
            return {'labels': [], 'data': []}
        
        # Group by year and sum demand
        trend_data = filtered_df.groupby(year_col)[demand_col].sum().sort_index()
        
        return {
            'labels': [str(year) for year in trend_data.index.tolist()],
            'data': trend_data.values.tolist()
        }
    
    def compare_areas_demand(self, areas: List[str]) -> Dict[str, Any]:
        """
        Compare demand trends across multiple areas
        
        Args:
            areas: List of area names
            
        Returns:
            Dictionary with comparison data for charting
        """
        filtered_df = self.filter_by_areas(areas)
        
        if filtered_df.empty:
            return {'labels': [], 'datasets': []}
        
        # Find columns
        year_col = self._find_column(['year', 'Year', 'Date', 'date'])
        demand_col = self._find_column([
            'total_sales - igr',
            'total sold - igr', 
            'flat_sold - igr',
            'total units',
            'Demand', 'demand', 'Sales', 'sales', 'Transactions', 'transactions'
        ])
        area_col = self._find_column(['final location', 'Area', 'area', 'Location', 'location', 'Locality', 'locality'])
        
        if year_col is None or demand_col is None or area_col is None:
            return {'labels': [], 'datasets': []}
        
        # Get unique years
        years = sorted(filtered_df[year_col].unique())
        
        # Create dataset for each area
        datasets = []
        colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
        
        for idx, area in enumerate(areas):
            area_data = filtered_df[filtered_df[area_col].astype(str).str.lower() == area.lower()]
            trend = area_data.groupby(year_col)[demand_col].sum().reindex(years, fill_value=0)
            
            datasets.append({
                'label': area,
                'data': trend.values.tolist(),
                'borderColor': colors[idx % len(colors)],
                'backgroundColor': colors[idx % len(colors)] + '33'
            })
        
        return {
            'labels': [str(year) for year in years],
            'datasets': datasets
        }
    
    def get_table_data(self, area: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get filtered table data for an area
        
        Args:
            area: Area name
            limit: Maximum number of rows to return
            
        Returns:
            List of dictionaries representing table rows
        """
        filtered_df = self.filter_by_area(area)
        
        if filtered_df.empty:
            return []
        
        # Limit rows
        filtered_df = filtered_df.head(limit)
        
        # Convert to dictionary
        return filtered_df.to_dict('records')
    
    def get_statistics(self, area: str) -> Dict[str, Any]:
        """
        Get statistical summary for an area
        
        Args:
            area: Area name
            
        Returns:
            Dictionary with statistics
        """
        filtered_df = self.filter_by_area(area)
        
        if filtered_df.empty:
            return {}
        
        price_col = self._find_column([
            'flat - weighted average rate',
            'office - weighted average rate', 
            'Price', 'price', 'Average Price', 'avg_price', 'AvgPrice'
        ])
        demand_col = self._find_column([
            'total_sales - igr',
            'total sold - igr',
            'flat_sold - igr',
            'total units',
            'Demand', 'demand', 'Sales', 'sales', 'Transactions', 'transactions'
        ])
        size_col = self._find_column([
            'total carpet area supplied (sqft)',
            'Size', 'size', 'Area_sqft', 'area_sqft', 'Square Feet', 'sqft'
        ])
        
        stats = {
            'total_records': len(filtered_df),
        }
        
        if price_col:
            stats['avg_price'] = float(filtered_df[price_col].mean())
            stats['min_price'] = float(filtered_df[price_col].min())
            stats['max_price'] = float(filtered_df[price_col].max())
        
        if demand_col:
            stats['total_demand'] = int(filtered_df[demand_col].sum())
            stats['avg_demand'] = float(filtered_df[demand_col].mean())
        
        if size_col:
            stats['avg_size'] = float(filtered_df[size_col].mean())
        
        return stats
    
    def _find_column(self, possible_names: List[str]) -> Optional[str]:
        """
        Find a column by trying multiple possible names
        
        Args:
            possible_names: List of possible column names
            
        Returns:
            Column name if found, None otherwise
        """
        if self.df is None:
            return None
        
        for name in possible_names:
            if name in self.df.columns:
                return name
        return None
    
    def generate_summary(self, area: str, stats: Dict[str, Any], trend_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a text summary for an area using Gemini LLM or fallback to mock
        
        Args:
            area: Area name
            stats: Statistics dictionary
            trend_data: Optional trend data for price/demand
            
        Returns:
            Text summary
        """
        if not stats:
            return f"No data available for {area}."
        
        # Try to use LLM integration
        try:
            from .llm_integration import generate_llm_summary
            
            # Prepare trend data if not provided
            if trend_data is None:
                trend_data = self.get_price_trend(area)
            
            llm_summary = generate_llm_summary(area, stats, trend_data)
            if llm_summary:
                return llm_summary
        except Exception as e:
            print(f"LLM generation failed, using fallback: {e}")
        
        # Fallback to mock summary
        summary_parts = [f"Analysis for {area}:"]
        
        if 'avg_price' in stats:
            summary_parts.append(
                f"The average property price is ₹{stats['avg_price']:,.2f}, "
                f"ranging from ₹{stats['min_price']:,.2f} to ₹{stats['max_price']:,.2f}."
            )
        
        if 'total_demand' in stats:
            summary_parts.append(
                f"Total demand recorded is {stats['total_demand']} transactions with "
                f"an average of {stats['avg_demand']:.2f} per period."
            )
        
        if 'avg_size' in stats:
            summary_parts.append(
                f"The average property size is {stats['avg_size']:.2f} square feet."
            )
        
        summary_parts.append(
            f"Based on {stats['total_records']} records, "
            f"{area} shows {'strong' if stats.get('total_demand', 0) > 100 else 'moderate'} "
            "market activity. This locality is suitable for both investment and residential purposes."
        )
        
        return " ".join(summary_parts)
