import React from "react";
import { format } from "date-fns";
import TimeRange from "react-timeline-range-slider";
import './App.css';

import {
  selectedInterval,
  timelineInterval
} from "./datesSource";


class App extends React.Component {
  state = {
    error: false,
    selectedInterval
  };

  errorHandler = ({ error }) => this.setState({ error });

  onChangeCallback = (selectedInterval) => this.setState({ selectedInterval });

  render() {
    const { selectedInterval, error } = this.state;
    return (
      <div>
        <div class="app-header">
          <div class="header1">
            Music
          </div>
          <div class="header2">
            History
          </div>
        </div>
        <div>
          <div class="interval">
            <span>Select interval by : </span>
            <button class="interval-button" type="button">Year</button>
            <button class="interval-button" type="button">Month</button>
            <button class="interval-button" type="button">Day</button>
          </div>

          <div class="interval">
            <span>Selected Interval: </span>
            {selectedInterval.map((d, i) => (
              <span class="interval-date" key={i}>{format(d, "yyyy")}</span>
            ))}
          </div>

          <div>
            <TimeRange
              error={error}
              ticksNumber={25}
              selectedInterval={selectedInterval}
              timelineInterval={timelineInterval}
              onUpdateCallback={this.errorHandler}
              onChangeCallback={this.onChangeCallback}
              formatTick={ms => format(new Date(ms), 'yyyy')}
              step={2592000000}
            />
          </div>
        </div>
      </div>
    );
  }
}

export default App;
