import json


def handler(req, res):
    """Vercel Serverless Function - Health check"""
    
    # CORS headers
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    res.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    
    # OPTIONS request
    if req.method == 'OPTIONS':
        return res.status(200).end()
    
    # GET request
    if req.method == 'GET':
        return res.status(200).json({
            'status': 'ok',
            'service': 'Spam Detector API'
        })
    
    # 404
    return res.status(404).json({'error': 'Not found'})
