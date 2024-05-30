import React from "react";

import './BikeList.css'
import BikeListItem from '../components/BikeListItem'

const BikeList = () => {

    // TODO: implement fetching
    let bikes = [
        {
            name: "Lastenrad 1"
        },
        {
            name: "Lastenrad 2"
        },
    ]

    return (
        <>
            <li className="list">
                {bikes.map((bike, index) => (
                    <BikeListItem bike={bike} key={index}/>
                ))}
            </li>
        </>
    );
};
  
export default BikeList;