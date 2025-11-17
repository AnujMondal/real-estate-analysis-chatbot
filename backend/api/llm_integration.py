"""
Optional Google Gemini integration for generating real LLM summaries
"""
import os
from django.conf import settings

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def generate_llm_summary(area: str, stats: dict, trend_data: dict) -> str:
    """
    Generate a summary using Google Gemini API
    
    Args:
        area: Area name
        stats: Statistics dictionary
        trend_data: Trend data for the area
        
    Returns:
        Generated summary or fallback to mock summary
    """
    if not GEMINI_AVAILABLE or not settings.GEMINI_API_KEY:
        return None
    
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        # Prepare context for LLM
        prompt = f"""
        As a real estate market analyst, analyze the following data for {area}:
        
        Statistics:
        - Average Price: ₹{stats.get('avg_price', 0):,.2f}
        - Price Range: ₹{stats.get('min_price', 0):,.2f} - ₹{stats.get('max_price', 0):,.2f}
        - Total Demand: {stats.get('total_demand', 0)} transactions
        - Average Demand: {stats.get('avg_demand', 0):.2f} per period
        - Average Size: {stats.get('avg_size', 0):.2f} sq ft
        - Total Records: {stats.get('total_records', 0)}
        
        Price Trend: {trend_data}
        
        Provide a concise 3-4 sentence analysis of this real estate market, 
        including insights on pricing trends, market activity, and investment potential.
        Keep it professional and data-driven.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        print(f"Error generating LLM summary: {e}")
        return None
