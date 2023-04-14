import React from "react";
import './App.css';
import Header from "./Header";
import TimeSlider from "./TimeSlider";
import Binder from "./binder"

class App extends React.Component {

  render() {
    return (
      <div>
        <Header />
        <TimeSlider />
        <Binder />
      </div>
    );
  }
}

export default App;
