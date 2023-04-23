import React from 'react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,Radar,Legend} from 'recharts';
import appContext from '../appContext';

                    
class AnalyticChart extends React.Component{
  static contextType = appContext
  
  render(){
    const {data} = this.context;
    console.log("Data Averages:",data);
    console.log("Averages:",data.averages);
    const dataValues = Object.values(data.averages);
    const dataKeys = Object.keys(data.averages);
    const d = dataKeys.map((key, index) => ({ name: key, value: dataValues[index] }));
    return (
      <div className='averageChart'>
        <RadarChart outerRadius={250} width={1100} height={570} data={d}>
          <PolarGrid />
          <PolarAngleAxis dataKey="name"/>
          <PolarRadiusAxis angle={30} domain={[0, 0.75]}/>
          <Radar name="Average" dataKey="value" stroke="#479FD9" fill="#479FD9" fillOpacity={0.6}>
          </Radar>
          <Legend/>
        </RadarChart>
      </div>
    );
  }
}

export default AnalyticChart;