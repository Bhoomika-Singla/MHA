import React from "react";
import { format } from "date-fns";
import TimeRange from "react-timeline-range-slider";
import './App.css';

import {
    selectedInterval,
    timelineInterval
} from "./datesSource";


class TimeSlider extends React.Component {
    state = {
        error: false,
        selectedInterval,
        selectedButton: "Year",
        step: 31557600000,  // default step for year
        formatString: "yyyy",
    };

    errorHandler = ({ error }) => this.setState({ error });

    onChangeCallback = (selectedInterval) => this.setState({ selectedInterval });

    handleIntervalClick = (step, formatString, buttonName) => {
        this.setState({ step, formatString, selectedButton: buttonName });
    };

    render() {
        const { selectedInterval, error, step, selectedButton, formatString } = this.state;
        return (
            <div>
                <div class="interval">
                    <span>Select interval by : </span>
                    <button
                        className={`interval-button ${selectedButton === "Day" ? "selected" : ""}`}
                        type="button"
                        onClick={() =>
                            this.handleIntervalClick(86400000, " dd MMM yyyy", "Day"
                            )
                        }
                    >Day</button>

                    <button
                        className={`interval-button ${selectedButton === "Month" ? "selected" : ""}`}
                        type="button"
                        onClick={() =>
                            this.handleIntervalClick(2629800000, "MMM yyyy", "Month"
                            )
                        }
                    >Month</button>

                    <button
                        className={`interval-button ${selectedButton === "Year" ? "selected" : ""}`}
                        type="button"
                        onClick={() =>
                            this.handleIntervalClick(31557600000, "yyyy", "Year"
                            )
                        }
                    >Year</button>
                </div>

                <div className="interval">
                    <span>Selected Interval : </span>
                    <span className="interval-date">
                        {selectedInterval
                            .map((d) => format(d, formatString))
                            .join(" - ")}
                    </span>
                </div>

                <div>
                    <TimeRange
                        error={error}
                        ticksNumber={25}
                        selectedInterval={selectedInterval}
                        timelineInterval={timelineInterval}
                        onUpdateCallback={this.errorHandler}
                        onChangeCallback={this.onChangeCallback}
                        formatTick={(ms) => format(new Date(ms), formatString)}
                        step={step}
                    />
                </div>
            </div>
        );
    }
}

export default TimeSlider;
