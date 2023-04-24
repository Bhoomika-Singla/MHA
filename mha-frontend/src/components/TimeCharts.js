import React from 'react';
import { BarChart, Bar, CartesianGrid, XAxis,YAxis,Tooltip,Legend} from 'recharts';
import appContext from '../appContext';

class TimeCharts extends React.Component {
  static contextType = appContext
  labValue = (selectedButton) =>{
    return selectedButton.toUpperCase()+'S';
  }
  
  render() {
    const { category } = this.props;
    const {data,selectedButton} = this.context;
    return (
      <div style={{flex: 1,padding: 40}}>
        <BarChart width={1100} height={450} data={data.result_data_array}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={selectedButton ==='year' ? 'data.'+selectedButton :selectedButton+'_number'} interval={selectedButton ==='week' ? 40 : 5} angle={-45} textAnchor="end" stroke = "#ffffff" strokeWidth={3} label={{value:this.labValue(selectedButton),dy:14.5,fill:"white", style: { fontWeight: 'bold' } }}/>
            <YAxis stroke = "#ffffff" strokeWidth={3}/>
            <Tooltip />
            <Legend wrapperStyle={{right: -30}} layout="vertical" verticalAlign="top" align="right"/>

            <Bar type="monotone" dataKey={'data.'+category.key.toLowerCase()} strokeWidth={3}  stroke={category.color} fill={category.fill} />
            
        </BarChart>
        </div>
    );
  }
}

export default TimeCharts;