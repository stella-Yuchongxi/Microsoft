import React, { useEffect } from 'react';
import * as echarts from 'echarts';
import axios from 'axios';

function GenreChart() {
    useEffect(() => {
        axios.get("http://localhost:5000/api/genre-count")
            .then(res => {
                const chartDom = document.getElementById('genre-chart');
                const myChart = echarts.init(chartDom);
                const option = {
                    title: { text: '电影类型分布', left: 'center' },
                    tooltip: { trigger: 'item' },
                    series: [{
                        name: '类型',
                        type: 'pie',
                        radius: '50%',
                        data: res.data
                    }]
                };
                myChart.setOption(option);
            });
    }, []);

    return <div id="genre-chart" style={{ width: '100%', height: 400 }} />;
}

export default GenreChart;
