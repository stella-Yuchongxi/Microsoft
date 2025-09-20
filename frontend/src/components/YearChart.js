import React, { useEffect } from 'react';
import * as echarts from 'echarts';
import axios from 'axios';

function YearChart() {
    useEffect(() => {
        axios.get("http://localhost:5000/api/year-count")
            .then(res => {
                const data = res.data;
                const chartDom = document.getElementById('year-chart');
                const myChart = echarts.init(chartDom);
                const option = {
                    title: { text: '上映年份趋势', left: 'center' },
                    tooltip: { trigger: 'axis' },
                    xAxis: { type: 'category', data: data.map(d => d.year) },
                    yAxis: { type: 'value' },
                    series: [{
                        data: data.map(d => d.count),
                        type: 'line'
                    }]
                };
                myChart.setOption(option);
            });
    }, []);

    return <div id="year-chart" style={{ width: '100%', height: 400 }} />;
}

export default YearChart;
