import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    status: 'ok',
    message: 'API Server is running',
    endpoints: {
      predict: '/api/predict (POST only)',
      health: '/api (GET only)'
    }
  });
}
