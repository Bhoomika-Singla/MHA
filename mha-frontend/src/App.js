import { useState } from "react";
import RangeSlider from "react-range-slider-input";
import "react-range-slider-input/dist/style.css";
import "./App.css";

export default function App() {
  const [value, setValue] = useState([2000, 2022]);

  return (
    <>
      
      <RangeSlider
        min={1950}
        max={2022}
        id="range-slider-gradient"
        className="margin-lg"
        step={1}
        defaultValue = {value}
      />

    </>
  );
}
