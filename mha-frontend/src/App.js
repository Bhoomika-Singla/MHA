import React from "react";
import './App.css';
import Header from "./components/Header";
import TimeSlider from "./components/TimeSlider";
import Binder from "./components/binder"
import TopSongsComponent from "./components/TopSongs";
import appContext from './appContext'

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      topSongsData: null,
      data: {
      "data": {
          "_id": "",
          "acousticness": 0.17,
          "danceability": 0.63,
          "date": "2003-11-16",
          "duration_ms": 236160.73,
          "energy": 0.7,
          "instrumentalness": 0.03,
          "key": 4,
          "liveness": 0.18,
          "loudness": -6.68,
          "mode": 1,
          "speechiness": 0.11,
          "tempo": 117.19,
          "time_signature": 4,
          "valence": 0.56
          },
      "week_number": 1
    } };
    this.setData = this.setData.bind(this);
  }

  setData(data) {
    this.setState({ data });
  }

  handleTopSongsData = (data) => {
    this.setState({ topSongsData: data });
  };

  componentDidUpdate(prevProps, prevState) {
    // Check if topSongsData has changed
    if (prevState.topSongsData !== this.state.topSongsData) {
      this.handleTopSongsData(this.state.topSongsData);
    }
  }

  render() {
    const { topSongsData } = this.state;
    return (
      <appContext.Provider value={{data: this.state.data, setData: this.setData}}>
        <div>
        <Header />
        <TimeSlider handleTopSongsData={this.handleTopSongsData} />
        <Binder />
        {topSongsData ? <TopSongsComponent topSongsData={topSongsData} /> : null}
        </div>
      </appContext.Provider>
    );
  }
}

export default App;
