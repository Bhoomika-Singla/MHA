import React from 'react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,Radar,Legend} from 'recharts';
import appContext from '../appContext';

const data = 
[
    {
        "data": {
            "_id": "",
            "acousticness": 0.17,
            "danceability": 0.63,
            "duration_min_decimal": 4.1,
            "energy": 0.7,
            "instrumentalness": 0.03,
            "liveness": 0.18,
            "loudness": -6.68,
            "speechiness": 0.11,
            "valence": 0.56
            },
        "week_number": 1
    }
]
                    
class AnalyticChart extends React.Component{
  static contextType = appContext
  
  
  render(){
    const dataValues = Object.values(data[0].data).slice(1);
    const dataKeys = Object.keys(data[0].data).slice(1);
    const d = dataKeys.map((key, index) => ({ name: key, value: dataValues[index] }));
    return (
      <div className='averageChart'>
        <RadarChart outerRadius={90} width={530} height={250} data={d}>
          <PolarGrid />
          <PolarAngleAxis dataKey="name"/>
          <PolarRadiusAxis angle={30} domain={[0, 2]}/>
          <Radar name="Average" dataKey="value" stroke="#479FD9" fill="#479FD9" fillOpacity={0.6}>
          </Radar>
          <Legend/>
        </RadarChart>
      </div>
    );
  }
}

export default AnalyticChart;