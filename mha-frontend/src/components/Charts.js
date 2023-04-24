import React from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import appContext from '../appContext';

class CustomTooltip extends React.Component {
    render() {
        const { active } = this.props;

        if (active) {
            const { payload } = this.props;
            if (payload) {
                return (
                    <div style={{ background: 'white', padding: '10px' }}>
                        <p style={{ margin: 0, color: payload[0].stroke }}>
                            {payload[0].name}: {payload[0].value}
                        </p>

                        <p style={{ margin: 0, color: payload[0].stroke }}>
                            date: {payload[0].payload.data.date}
                        </p>

                    </div>
                );
            }
        }

        return null;
    }
}

class BaseComponent extends React.Component {
    static contextType = appContext
    labValue = (selectedButton) => {
        return selectedButton.toUpperCase() + 'S';
    }
    render() {
        const { category } = this.props;
        const { data, selectedButton } = this.context;
        return (
            <div style={{ flex: 1, padding: 40 }}>
                <LineChart width={1100} height={450} data={data.result_data_array}>

                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey={selectedButton === 'year' ? 'data.' + selectedButton : selectedButton + '_number'} interval={selectedButton === 'week' ? 40 : 5} angle={-45} textAnchor="end" stroke="#ffffff" strokeWidth={3} label={{ value: this.labValue(selectedButton), dy: 14.5, fill: "white", style: { fontWeight: 'bold' } }} />
                    <YAxis stroke="#ffffff" strokeWidth={3} />
                    <Tooltip content={<CustomTooltip activeButton={selectedButton} />} />
                    <Legend wrapperStyle={{ right: -30 }} layout="vertical" verticalAlign="top" align="right" />
                    {category.map(c => (
                        <Line type="monotone" key={c.name} dataKey={'data.' + c.name.toLowerCase()} strokeWidth={3} stroke={c.color} />
                    ))}
                </LineChart>
            </div>
        );
    }
}

export default BaseComponent;
