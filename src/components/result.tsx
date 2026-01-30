import { AnimatedCircularProgressBar } from "./ui/animated-circular-progress-bar";

type ResultProps = {
  classification?: string,
  precision?: number
  setIsVisible: (visible: boolean) => void,
};
export default function Result({classification, precision ,setIsVisible}: ResultProps) {
  return (
    <div className="z-1000  absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-20 rounded-lg shadow-md border border-gray-200 py-8 ">
      <span className="absolute top-4 right-4 text-gray-500 cursor-pointer"
      onClick={() => setIsVisible(false)}
      >&times;</span>
      <h2 className="text-2xl font-semibold text-center">{classification !== undefined ? classification : "N/A"}</h2>
      <p className="text-center text-gray-500 text-extralight mb-10">Précision</p>
      <AnimatedCircularProgressBar
        value={precision !== undefined ? precision * 100 : 0}
        gaugePrimaryColor="rgba(62, 178, 255, 1)"
        gaugeSecondaryColor="rgba(0, 0, 0, 0.1)"
      />
    </div>
  );
}
