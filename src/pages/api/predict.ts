import type { NextApiRequest, NextApiResponse } from 'next';

const BACKEND_URL = process.env.BACKEND_URL || "https://backendspamorham.up.railway.app";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }

  try {
    const { text } = req.body;
    if (!text) {
      return res.status(400).json({ error: 'Texte manquant' });
    }

    const response = await fetch(`${BACKEND_URL}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      // Si Railway répond une erreur, on la transmet à Vercel pour débugger
      const errorData = await response.text();
      return res.status(response.status).json({ error: 'Railway Error', details: errorData });
    }

    const data = await response.json();
    return res.status(200).json(data);
  } catch (error: any) {
    return res.status(500).json({ error: 'Erreur de connexion au backend Python', details: error.message });
  }
}
