import React from "react";
import './App.css';
import Header from "./Header";
import TimeSlider from "./TimeSlider";

class App extends React.Component {

  render() {
    return (
      <div>
        <Header />
        <TimeSlider />
      </div>
    );
  }
}

export default App;
