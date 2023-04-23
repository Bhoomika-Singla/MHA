import React from 'react';
import { BarChart, Bar, CartesianGrid, XAxis,YAxis,Tooltip,Legend} from 'recharts';
import appContext from '../appContext';

class TimeCharts extends React.Component {
    static contextType = appContext
  render() {
    const { category } = this.props;
    const {data} = this.context;
    return (
      <div style={{flex: 1,padding: 40}}>
        <BarChart width={1100} height={450} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="week_number" stroke = "#ffffff" strokeWidth={3} label={{value:"Weeks", fill:"white", style: { fontWeight: 'bold' } }}/>
            <YAxis stroke = "#ffffff" strokeWidth={3}/>
            <Tooltip />
            <Legend wrapperStyle={{right: -30}} layout="vertical" verticalAlign="top" align="right"/>
            
            <Bar type="monotone" dataKey={'data.'+category.key.toLowerCase()} strokeWidth={3}  stroke={category.color} fill={category.fill} />
            
        </BarChart>
            {/* <button class="dropbtn" onClick={openDropDown}>Unit</button> */}
        </div>
    );
  }
}

export default TimeCharts;