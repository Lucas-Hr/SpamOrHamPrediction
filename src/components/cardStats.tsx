import { AnimatedCircularProgressBar } from "./ui/animated-circular-progress-bar";

type CardStatsProps = {
    title? : string;
    color?: string;
    value?: number;
};
export default function CardStats({ title, color, value }: CardStatsProps) {
  return (
    <div className="flex flex-col gap-4 items-center py-8 px-10 rounded-lg shadow-md border border-gray-200 ">
      <h2 className="text-xl  text-center">{title}</h2>
      <AnimatedCircularProgressBar
      className="w-25"
      value={value !== undefined ? value * 100 : 0}
      gaugePrimaryColor={color || "rgb(79 70 229)"}
      gaugeSecondaryColor="rgba(0, 0, 0, 0.1)"
    />
    </div>
  );
}
