'use client'
import { useState } from "react";
type InputMessageProps = {
  setIsVisible: (isVisible: boolean) => void;
  setPrediction: (prediction: string) => void;
  setPrecisionHam: (precisionHam: number) => void;
  setPrecisionSpam: (precisionSpam: number) => void;
}

export default function InputMessage({setIsVisible, setPrediction, setPrecisionHam, setPrecisionSpam}: InputMessageProps) {
  const [message , setMessage] = useState<string>("");
  const predict = async () => {
    
    const res = await fetch('https://spam-or-ham-prediction.vercel.app/backend/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: message }),
    });
    setIsVisible(true);
    const data = await res.json();
    console.log(data);
    setPrediction(data.prediction);
    setPrecisionHam(data.probabilities.ham);
    setPrecisionSpam(data.probabilities.spam);
  }
  return (
    <div className="bg-white px-10 rounded-lg shadow-md border border-gray-200 py-8 ">
      <h2 className="text-md font-semibold text-center">TESTEZ VOTRE MESSAGE ...</h2>
      <div className="flex flex-col gap-4">
        <textarea className="w-full h-full py-2 border-b-1 outline-none" placeholder="Entrez votre message ici pour savoir s'il s'agit de spam ou de ham."
        onChange={(e) => setMessage(e.target.value)}
        ></textarea>
        <button className="w-25 px-4 py-2 bg-[#20a7db] text-white font-semibold rounded-md cursor-pointer"
        onClick={predict}
        >Tester</button>
      </div>
    </div>
  );
}
