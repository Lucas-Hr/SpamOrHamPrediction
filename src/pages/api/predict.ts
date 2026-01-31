import type { NextApiRequest, NextApiResponse } from 'next';
import { spawn } from 'child_process';
import path from 'path';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }

  const { text } = req.body;
  if (!text) {
    return res.status(400).json({ error: 'Texte manquant' });
  }

  // Appel du script Python pour la prédiction
  const scriptPath = path.join(process.cwd(), 'api', 'predict.py');
  const py = spawn('python', [scriptPath, text]);

  let data = '';
  let error = '';

  py.stdout.on('data', (chunk) => {
    data += chunk;
  });
  py.stderr.on('data', (chunk) => {
    error += chunk;
  });
  py.on('close', (code) => {
    if (code !== 0 || error) {
      return res.status(500).json({ error: error || 'Erreur lors de la prédiction' });
    }
    try {
      const result = JSON.parse(data);
      res.status(200).json(result);
    } catch (e) {
      res.status(500).json({ error: 'Erreur de parsing JSON' });
    }
  });
}
