import React from "react";
import axios from 'axios';
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

    onChangeCallback = (selectedInterval) => {
        this.setState({ selectedInterval }, () => {
            this.sendIntervalData();
        });
    }

    handleIntervalClick = (step, formatString, buttonName) => {
        this.setState({ step, formatString, selectedButton: buttonName }, () => {
            this.sendIntervalData();
        });
    };

    sendIntervalData = () => {
        const { selectedButton, selectedInterval } = this.state;

        let intervalFormat = 'yyyy-MM-dd';
        if (selectedButton === 'Year')
            intervalFormat = 'yyyy';
        else if (selectedButton === 'Month')
            intervalFormat = 'yyyy-MM';

        const startDate = format(selectedInterval[0], intervalFormat);
        const endDate = format(selectedInterval[1], intervalFormat);
        const intervalData = {
            interval: selectedButton,
            startDate,
            endDate
        };

        axios.post("/intervals", intervalData)
            .then(response => {
                // Handle success
                console.log(response.data);
            })
            .catch(error => {
                // Handle error
                console.error(error);
            });
    }

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
