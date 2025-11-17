from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.conf import settings
import os
import re
from .data_processor import DataProcessor


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_file(request):
    """
    Upload Excel file endpoint
    """
    try:
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = request.FILES['file']
        
        # Validate file type
        if not file.name.endswith(('.xlsx', '.xls')):
            return Response(
                {'error': 'Invalid file type. Please upload an Excel file.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save file
        file_path = default_storage.save(f'data/{file.name}', file)
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)
        
        # Test loading the file
        processor = DataProcessor(full_path)
        if not processor.load_data():
            return Response(
                {'error': 'Failed to load Excel file. Please check the format.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'message': 'File uploaded successfully',
            'file_path': file_path,
            'available_areas': processor.get_available_areas()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Error uploading file: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@parser_classes([JSONParser])
def process_query(request):
    """
    Process user query and return analysis
    """
    try:
        query = request.data.get('query', '')
        file_path = request.data.get('file_path', None)
        
        if not query:
            return Response(
                {'error': 'No query provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialize processor
        if file_path:
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            processor = DataProcessor(full_path)
        else:
            processor = DataProcessor()
        
        if not processor.load_data():
            return Response(
                {'error': 'Failed to load data. Please upload a file first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parse query to extract intent and areas
        query_lower = query.lower()
        available_areas = processor.get_available_areas()
        
        # Find mentioned areas in query
        mentioned_areas = []
        for area in available_areas:
            if area.lower() in query_lower:
                mentioned_areas.append(area)
        
        if not mentioned_areas:
            return Response({
                'summary': f"I couldn't find any specific locality in your query. Available areas are: {', '.join(available_areas[:10])}{'...' if len(available_areas) > 10 else ''}",
                'chart_data': None,
                'table_data': [],
                'chart_type': None
            }, status=status.HTTP_200_OK)
        
        # Determine query type
        is_comparison = 'compare' in query_lower or 'vs' in query_lower or len(mentioned_areas) > 1
        is_demand = 'demand' in query_lower
        is_price = 'price' in query_lower or 'growth' in query_lower
        
        response_data = {}
        
        if is_comparison:
            # Comparison query
            chart_data = processor.compare_areas_demand(mentioned_areas)
            response_data['chart_type'] = 'line'
            response_data['chart_data'] = chart_data
            response_data['summary'] = f"Comparing demand trends for {', '.join(mentioned_areas)}. "
            
            # Add basic comparison insights
            if chart_data['datasets']:
                total_demands = [sum(ds['data']) for ds in chart_data['datasets']]
                highest_idx = total_demands.index(max(total_demands))
                response_data['summary'] += f"{mentioned_areas[highest_idx]} shows the highest overall demand with {total_demands[highest_idx]:,.0f} total transactions."
            
            # Get table data for first area
            response_data['table_data'] = processor.get_table_data(mentioned_areas[0], limit=20)
            
        elif is_demand:
            # Demand analysis
            area = mentioned_areas[0]
            chart_data = processor.get_demand_trend(area)
            stats = processor.get_statistics(area)
            
            response_data['chart_type'] = 'line'
            response_data['chart_data'] = {
                'labels': chart_data['labels'],
                'datasets': [{
                    'label': f'{area} Demand',
                    'data': chart_data['data'],
                    'borderColor': '#36A2EB',
                    'backgroundColor': '#36A2EB33'
                }]
            }
            response_data['summary'] = processor.generate_summary(area, stats)
            response_data['table_data'] = processor.get_table_data(area, limit=20)
            
        elif is_price:
            # Price analysis
            area = mentioned_areas[0]
            chart_data = processor.get_price_trend(area)
            stats = processor.get_statistics(area)
            
            response_data['chart_type'] = 'line'
            response_data['chart_data'] = {
                'labels': chart_data['labels'],
                'datasets': [{
                    'label': f'{area} Price Trend',
                    'data': chart_data['data'],
                    'borderColor': '#FF6384',
                    'backgroundColor': '#FF638433'
                }]
            }
            response_data['summary'] = processor.generate_summary(area, stats)
            response_data['table_data'] = processor.get_table_data(area, limit=20)
            
        else:
            # General analysis
            area = mentioned_areas[0]
            stats = processor.get_statistics(area)
            price_data = processor.get_price_trend(area)
            
            response_data['chart_type'] = 'line'
            response_data['chart_data'] = {
                'labels': price_data['labels'],
                'datasets': [{
                    'label': f'{area} Price Trend',
                    'data': price_data['data'],
                    'borderColor': '#FF6384',
                    'backgroundColor': '#FF638433'
                }]
            }
            response_data['summary'] = processor.generate_summary(area, stats)
            response_data['table_data'] = processor.get_table_data(area, limit=20)
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Error processing query: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_available_areas(request):
    """
    Get list of available areas from dataset
    """
    try:
        file_path = request.query_params.get('file_path', None)
        
        if file_path:
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            processor = DataProcessor(full_path)
        else:
            processor = DataProcessor()
        
        if not processor.load_data():
            return Response(
                {'error': 'Failed to load data'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        areas = processor.get_available_areas()
        
        return Response({
            'areas': areas,
            'count': len(areas)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Error getting areas: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@parser_classes([JSONParser])
def export_data(request):
    """
    Export filtered data based on query
    """
    try:
        area = request.data.get('area', '')
        file_path = request.data.get('file_path', None)
        
        if not area:
            return Response(
                {'error': 'No area provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if file_path:
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            processor = DataProcessor(full_path)
        else:
            processor = DataProcessor()
        
        if not processor.load_data():
            return Response(
                {'error': 'Failed to load data'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        table_data = processor.get_table_data(area, limit=1000)
        
        return Response({
            'data': table_data,
            'area': area,
            'count': len(table_data)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Error exporting data: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
