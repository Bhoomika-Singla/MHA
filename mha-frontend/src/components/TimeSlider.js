import React from "react";
import axios from 'axios';
import { format } from "date-fns";
import TimeRange from "react-timeline-range-slider";
import '../App.css';
import appContext from '../appContext'

import {
    selectedInterval,
    timelineInterval
} from "./datesSource";


class TimeSlider extends React.Component {
    static contextType = appContext
    state = { 
        error: false,
        selectedInterval,
        selectedButton: "Year",
        step: 31557600000,  // default step for year
        formatString: "yyyy",
        updatedData: this.context.data
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

    handleUpdateData=(data)=> {
        this.setState({updatedData:data});
        this.context.setData(this.state.updatedData);
    }

    sendIntervalData = () => {
        const { selectedButton, selectedInterval } = this.state;

        let intervalFormat = 'yyyy-MM-dd';
        let interval = selectedButton;
         if (selectedButton === 'Day')
            interval = 'Week';

        const startDate = format(selectedInterval[0], intervalFormat);
        const endDate = format(selectedInterval[1], intervalFormat);
        const intervalType = selectedButton === 'Day' ? 'Week' : selectedButton
        const intervalData = {
            interval: selectedButton,
            startDate,
            endDate,
            intervalType
        };

        console.log(intervalData);

        axios.get("https://mhaflask4-22-zesadgjgsa-uw.a.run.app/query", {params:{startDate:startDate , endDate:endDate, interval:interval, topCount:'top100'}})
        // axios.get("http://127.0.0.1:5000/query2", {params:{startDate:startDate , endDate:endDate,interval:intervalType.toLowerCase(),topCount:"top1"}})
            .then(response => {
                // Handle success
                this.handleUpdateData(response.data)
                console.log(response.data);
            })
            .catch(error => {
                // Handle error 
                console.error(error);
            });
        

        axios.get("https://mhaflask4-22-zesadgjgsa-uw.a.run.app/top_songs", {params:{startDate:startDate , endDate:endDate, songCount:'10'}})
            .then(response => {
                const topSongsData = response.data;
                this.props.handleTopSongsData(topSongsData);
            })
            .catch(error => {
                // Handle error
                console.error(error);
            });
        }  

    render() {
        const { selectedInterval, error, step, selectedButton, formatString } = this.state;
        return (
            <div className="timeslider-container">
                <div className="interval">
                    <span style={{color:"white"}}>Select interval by : </span>
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
                    <span style={{color:"white"}}>Selected Interval : </span>
                    <span className="interval-date" style={{color:"white"}}>
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
