import React from 'react';
import GenreChart from './components/GenreChart';
import YearChart from './components/YearChart';

function App() {
    return (
        <div>
            <h1>豆瓣 Top200 电影可视化</h1>
            <GenreChart />
            <YearChart />
        </div>
    );
}

export default App;
