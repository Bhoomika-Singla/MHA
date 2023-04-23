import React from 'react';
import { LineChart, Line, CartesianGrid, XAxis,YAxis,Tooltip,Legend, Label} from 'recharts';
import appContext from '../appContext';

//TODO: Make changes to fetch data through API
// const data = 
// [
//     {
//         "data": {
//             "_id": "",
//             "acousticness": 0.17,
//             "danceability": 0.63,
//             "date": "2003-11-16",
//             "duration_ms": 236160.73,
//             "energy": 0.7,
//             "instrumentalness": 0.03,
//             "key": 4,
//             "liveness": 0.18,
//             "loudness": -6.68,
//             "mode": 1,
//             "speechiness": 0.11,
//             "tempo": 117.19,
//             "time_signature": 4,
//             "valence": 0.56
//             },
//         "week_number": 1
//     },
//     {
//         "data": {
//             "_id": "",
//             "acousticness": 0.17,
//             "danceability": 0.63,
//             "date": "2003-11-23",
//             "duration_ms": 233484.26,
//             "energy": 0.7,
//             "instrumentalness": 0.04,
//             "key": 4,
//             "liveness": 0.18,
//             "loudness": -6.67,
//             "mode": 0,
//             "speechiness": 0.11,
//             "tempo": 114.96,
//             "time_signature": 4,
//             "valence": 0.55
//         },
//         "week_number": 2
//     },
//     {
//         "data": {
//         "_id": "",
//         "acousticness": 0.18,
//         "danceability": 0.64,
//         "date": "2003-11-30",
//         "duration_ms": 234613.32,
//         "energy": 0.7,
//         "instrumentalness": 0.04,
//         "key": 4,
//         "liveness": 0.19,
//         "loudness": -6.66,
//         "mode": 1,
//         "speechiness": 0.12,
//         "tempo": 113.86,
//         "time_signature": 4,
//         "valence": 0.45
//     },
//     "week_number": 3
//     },
//     {
//         "data": {
//             "_id": "",
//             "acousticness": 0.17,
//             "danceability": 0.64,
//             "date": "2003-12-14",
//             "duration_ms": 232871.69,
//             "energy": 0.71,
//             "instrumentalness": 0.03,
//             "key": 4,
//             "liveness": 0.2,
//             "loudness": -6.49,
//             "mode": 1,
//             "speechiness": 0.1,
//             "tempo": 111.78,
//             "time_signature": 4,
//             "valence": 0.57
//         },
//         "week_number": 4
//     }
// ]

const symbolMapping = {
    0: '\ue260',
    1: '\ue261',
    2: '\ue262',
    3: '\ue263',
    4: '\ue264',
    5: '\ue265',
    6: '\ue266',
    7: '\ue267',
    8: '\ue268',
    9: '\ue269',
    sharp: '\ue262',
    flat: '\ue260',
  };

  
const CustomizedDot = (props) => {
  
  const { cx, cy, stroke, payload, value, category } = props;
  if(category.name === "Valence"){
    if (value> 0.5) {
      return (
        <svg x={cx - 10} y={cy - 10} width={20} height={20} fill="white" viewBox="0 0 1024 1024">
          <path d="M512 1009.984c-274.912 0-497.76-222.848-497.76-497.76s222.848-497.76 497.76-497.76c274.912 0 497.76 222.848 497.76 497.76s-222.848 497.76-497.76 497.76zM340.768 295.936c-39.488 0-71.52 32.8-71.52 73.248s32.032 73.248 71.52 73.248c39.488 0 71.52-32.8 71.52-73.248s-32.032-73.248-71.52-73.248zM686.176 296.704c-39.488 0-71.52 32.8-71.52 73.248s32.032 73.248 71.52 73.248c39.488 0 71.52-32.8 71.52-73.248s-32.032-73.248-71.52-73.248zM772.928 555.392c-18.752-8.864-40.928-0.576-49.632 18.528-40.224 88.576-120.256 143.552-208.832 143.552-85.952 0-164.864-52.64-205.952-137.376-9.184-18.912-31.648-26.592-50.08-17.28-18.464 9.408-21.216 21.472-15.936 32.64 52.8 111.424 155.232 186.784 269.76 186.784 117.984 0 217.12-70.944 269.76-186.784 8.672-19.136 9.568-31.2-9.12-40.096z" />
        </svg>
      );
    }
  
    return (
      <svg x={cx - 10} y={cy - 10} width={20} height={20} fill="red" viewBox="0 0 1024 1024">
        <path d="M517.12 53.248q95.232 0 179.2 36.352t145.92 98.304 98.304 145.92 36.352 179.2-36.352 179.2-98.304 145.92-145.92 98.304-179.2 36.352-179.2-36.352-145.92-98.304-98.304-145.92-36.352-179.2 36.352-179.2 98.304-145.92 145.92-98.304 179.2-36.352zM663.552 261.12q-15.36 0-28.16 6.656t-23.04 18.432-15.872 27.648-5.632 33.28q0 35.84 21.504 61.44t51.2 25.6 51.2-25.6 21.504-61.44q0-17.408-5.632-33.28t-15.872-27.648-23.04-18.432-28.16-6.656zM373.76 261.12q-29.696 0-50.688 25.088t-20.992 60.928 20.992 61.44 50.688 25.6 50.176-25.6 20.48-61.44-20.48-60.928-50.176-25.088zM520.192 602.112q-51.2 0-97.28 9.728t-82.944 27.648-62.464 41.472-35.84 51.2q-1.024 1.024-1.024 2.048-1.024 3.072-1.024 8.704t2.56 11.776 7.168 11.264 12.8 6.144q25.6-27.648 62.464-50.176 31.744-19.456 79.36-35.328t114.176-15.872q67.584 0 116.736 15.872t81.92 35.328q37.888 22.528 63.488 50.176 17.408-5.12 19.968-18.944t0.512-18.944-3.072-7.168-1.024-3.072q-26.624-55.296-100.352-88.576t-176.128-33.28z" />
      </svg>
    );
  }
};


class AllTimeViewCharts extends React.Component {
  static contextType = appContext

  labValue = (selectedButton) =>{
    return selectedButton.toUpperCase()+'S';
  }

  render() {
    const { category } = this.props;
   const {data,selectedButton} = this.context;

    return (
      <div style={{flex: 2,padding: 40,display: 'flex'}}>
        <LineChart width={1100} height={450} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={selectedButton+'_number'} angle={-45} textAnchor="end" stroke = "#ffffff" strokeWidth={3} label={{value:this.labValue(selectedButton),dy:14.5, fill:"white", style: { fontWeight: 'bold' } }}/>
            <YAxis stroke = "#ffffff" strokeWidth={3}/>
            <Label value="Loudness" position = "top" style={{fontSize: '24px', fill:'white',fontWeight: 'bold'}} />
            <Tooltip />
            <Legend wrapperStyle={{right: -30}} layout="vertical" verticalAlign="top" align="right"/>
            <Label value="Loudness" position="top" style={{ fontSize: '44px', fill: 'white', fontWeight: 'bold' }} />
            <Line type="monotone" key = {category.name} dataKey={'data.'+category.key.toLowerCase()} stroke={category.color} dot={<CustomizedDot category={category}/>} strokeWidth={3} />
            
        </LineChart> 
      </div>
    );
  }
}

export default AllTimeViewCharts;