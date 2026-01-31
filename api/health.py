import json


def handler(request):
    """Health check endpoint - Vercel compatible"""
    
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # OPTIONS request
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    # GET request
    if request.method == 'GET':
        response = {
            'status': 'ok',
            'service': 'Spam Detector API'
        }
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response)
        }
    
    # 404
    return {
        'statusCode': 404,
        'headers': headers,
        'body': json.dumps({'error': 'Not found'})
    }
