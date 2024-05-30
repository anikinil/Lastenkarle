import React from "react";

import './BikeListItem.css'

const BikeListItem = ({bike, index}) => {

    return (
        <div className="bike-list-item" key={index}>
            <p>{bike.name}</p>
        </div>
    );
};
  
export default BikeListItem;