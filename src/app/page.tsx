'use client'
import InputMessage from "@/components/inputMessage";
import DoughnutChart from "@/components/dognutChart";
import CardStats from "@/components/cardStats";
import Table from "@/components/table";
import Image from "next/image";
export default function Home() {
  return (
    <div className="px-10 py-8 h-screen overflow-y-hidden">
        <div className="flex items-center gap-4">
         <Image src="/messageicon.png" alt="Spam or Ham" className="w-15" width={200} height={200} />
          <h1 className="text-5xl font-semibold mb-4">SPAM OR HAM?</h1>
        </div>
      <div className="grid grid-cols-2 gap-8 mt-8">
        <div className="flex flex-col justify-between ">
          <InputMessage />
          <Table />
        </div>
        <div className="flex flex-col gap-2 ">
          <div className="grid grid-cols-2 gap-4 ">
            <CardStats title="F1-Score" color="rgba(255, 249, 62, 1)" value={0.8}/>
            <CardStats title="Recall" color="rgba(255, 107, 107, 1)" value={0.7}/>  
          </div>
         <div className="grid grid-cols-2 gap-4 ">
          <CardStats title="Accuracy" color="rgba(84, 255, 62, 1)" value={0.4}/>
          <DoughnutChart spam={12} ham={3}/>    
        </div>
        </div>
      </div>
    </div>
  );
}
