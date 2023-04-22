import React from "react";
import './App.css';
import Header from "./components/Header";
import TimeSlider from "./components/TimeSlider";
import Binder from "./components/binder"
import TopSongsComponent from "./components/TopSongs";

class App extends React.Component {
  state = {
    topSongsData: null
  };

  handleTopSongsData = (data) => {
    this.setState({ topSongsData: data });
  };

  render() {
    const { topSongsData } = this.state;
    console.log(topSongsData)

    return (
      <div>
        <Header />
        <TimeSlider handleTopSongsData={this.handleTopSongsData} />
        <Binder />
        {topSongsData ? <TopSongsComponent topSongsData={topSongsData} /> : null}
      </div>
    );
  }
}

export default App;
