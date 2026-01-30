'use client'

export default function InputMessage({setIsVisible}: {setIsVisible: (isVisible: boolean) => void}) {
  return (
    <div className="bg-white px-10 rounded-lg shadow-md border border-gray-200 py-8 ">
      <h2 className="text-md font-semibold text-center">TESTEZ VOTRE MESSAGE ...</h2>
      <div className="flex flex-col gap-4">
        <textarea className="w-full h-full py-2 border-b-1 outline-none" placeholder="Entrez votre message ici pour savoir s'il s'agit de spam ou de ham."></textarea>
        <button className="w-25 px-4 py-2 bg-[#20a7db] text-white font-semibold rounded-md cursor-pointer"
        onClick={() => setIsVisible(true)}
        >Tester</button>
      </div>
    </div>
  );
}
