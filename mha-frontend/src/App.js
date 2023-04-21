import React from "react";
import './App.css';
import Header from "./components/Header";
import TimeSlider from "./components/TimeSlider";
import Binder from "./components/binder"

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
