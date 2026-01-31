'use client'
import { useState } from "react";
import InputMessage from "@/components/inputMessage";
import DoughnutChart from "@/components/dognutChart";
import CardStats from "@/components/cardStats";
import Table from "@/components/table";
import Result from "@/components/result";
import Image from "next/image";
export default function Home() {
  const [isVisible , setIsVisible] = useState<boolean>(false);
  const [prediction , setPrediction] = useState<string>("");
  const [precisionHam , setPrecisionHam] = useState<number>(0);
  const [precisionSpam , setPrecisionSpam] = useState<number>(0);
  const [confidence , setConfidence] = useState<number>(0);
  return (
    <div className="px-10 py-10 ">
        {isVisible && <Result prediction={prediction} precisionHam={precisionHam} precisionSpam={precisionSpam} confidence={confidence} setIsVisible={setIsVisible}/>}
        <div className="flex items-center gap-4">
         <Image src="/messageicon.png" alt="Spam or Ham" className="w-10" width={200} height={200} />
          <h1 className="text-3xl font-semibold">SPAM OU HAM?</h1>
        </div>
        Lien github : https://github.com/Lucas-Hr/SpamOrHamPrediction.git
      <div className="flex gap-4   mt-8">
        <div className="flex flex-col justify-between ">
          <InputMessage setIsVisible={setIsVisible} setPrediction={setPrediction} setPrecisionHam={setPrecisionHam} setPrecisionSpam={setPrecisionSpam} setConfidence={setConfidence} />
          <div className="flex items-start gap-4">
            <Table />
            <DoughnutChart spam={12} ham={3}/>  
          </div>
        </div>
        <div className="flex flex-col gap-4 ">
          <div className="grid grid-cols-2 gap-4 ">
            <CardStats title="F1-Score" color="rgba(255, 249, 62, 1)" value={0.8}/>
            <CardStats title="Recall" color="rgba(255, 107, 107, 1)" value={0.7}/>  
          </div>
          <div className="grid grid-cols-2 gap-4 ">
            <CardStats title="Accuracy" color="rgba(84, 255, 62, 1)" value={0.4}/>
            <CardStats title="Precision" color="rgb(104, 62, 255)" value={0.6}/>
          </div>
        </div>
      </div>
    </div>
  );
}
