import { AnimatedCircularProgressBar } from "./ui/animated-circular-progress-bar";

type ResultProps = {
  prediction?: string,
  precisionHam?: number,
  precisionSpam?: number,
  confidence? : number,
  setIsVisible: (visible: boolean) => void,
};
export default function Result({prediction, precisionHam, precisionSpam,confidence, setIsVisible}: ResultProps) {
  return (
    <div className="z-1000  absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-20 rounded-lg shadow-md border border-gray-200 py-8 ">
      <span className="absolute top-4 right-4 text-gray-500 cursor-pointer"
      onClick={() => setIsVisible(false)}
      >&times;</span>
      <h2 className="text-2xl font-semibold text-center">{precisionSpam>precisionHam ? "Spam" : "Ham"}</h2>
      <p className="text-center text-gray-500 text-extralight mt-4">Probabilité Ham</p>
      <AnimatedCircularProgressBar
        value={(precisionHam ?? 0) * 100 || 20}
        gaugePrimaryColor="rgba(62, 178, 255, 1)"
        gaugeSecondaryColor="rgba(0, 0, 0, 0.1)"
      />
      <p className="text-center text-gray-500 text-extralight mt-4">Probabilité Spam</p>
      <AnimatedCircularProgressBar
        value={(precisionSpam ?? 0) * 100 || 20}
        gaugePrimaryColor="rgba(255, 107, 107, 1)"
        gaugeSecondaryColor="rgba(0, 0, 0, 0.1)"
      />
      <p className="text-center text-gray-500 text-extralight mt-4">Pourcentage de confiance</p>
      <AnimatedCircularProgressBar
        value={(confidence ?? 0) * 100 || 20}
        gaugePrimaryColor="rgba(255, 107, 107, 1)"
        gaugeSecondaryColor="rgba(0, 0, 0, 0.1)"
      />
    </div>
  );
}
