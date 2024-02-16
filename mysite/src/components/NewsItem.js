// components/NewsItem.js
import React from 'react';

const NewsItem = ({ news }) => {
    return (
        <div className="news-item">
            <h2>{news.title}</h2>
            <p>{news.description}</p>
            {/* Другие детали новости */}
        </div>
    );
};

export default NewsItem;
