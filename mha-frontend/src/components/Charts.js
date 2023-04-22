import React from 'react';
import { LineChart, Line, CartesianGrid, XAxis,YAxis,Tooltip,Legend} from 'recharts';
import appContext from '../appContext';

class BaseComponent extends React.Component {
    static contextType = appContext
    render() {
        const { category } = this.props;
        const {data} = this.context;
        return (
        <div style={{flex: 1,padding: 50}}>
            <LineChart width={1100} height={450} data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="week_number" stroke = "#ffffff" strokeWidth={3} label={{value:"Weeks", fill:"white", style: { fontWeight: 'bold' } }}/>
                <YAxis stroke = "#ffffff" strokeWidth={3}/>
                <Tooltip />
                <Legend wrapperStyle={{right: -30}} layout="vertical" verticalAlign="top" align="right"/>
                {category.map(c => (
                <Line type="monotone" key = {c.name} dataKey={'data.'+c.name.toLowerCase()} strokeWidth={3}  stroke={c.color} />
                ))}
            </LineChart>
        </div>
        );
    }
}

export default BaseComponent;